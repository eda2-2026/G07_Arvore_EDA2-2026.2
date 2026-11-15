from datetime import date
from threading import RLock
from app.structures.avl import AVL
from app.structures.trie import Trie
from app.structures.locations import LOCATIONS, descendants
from app.validation import validate
from app.categories import CATEGORIES


class Service:
    def __init__(self, storage):
        self.storage = storage
        self.lock = RLock()
        self.reindex()

    def reindex(self):
        self.by_id = {item['id']: item for item in self.storage.items}
        self.avl, self.trie = AVL(), Trie()
        for item in self.storage.items:
            self.trie.insert(item['name'], item['id'])
            if item['status'] == 'guardado':
                self.avl.insert((item['deadline'], item['id']))

    def _save_change(self, items, previous=None, current=None):
        """Atualiza os índices somente depois de a gravação ser bem-sucedida."""
        self.storage.save(items)
        if previous:
            self.trie.remove(previous['name'], previous['id'])
            if previous['status'] == 'guardado':
                self.avl.remove((previous['deadline'], previous['id']))
            self.by_id.pop(previous['id'])
        if current:
            self.by_id[current['id']] = current
            self.trie.insert(current['name'], current['id'])
            if current['status'] == 'guardado':
                self.avl.insert((current['deadline'], current['id']))

    def listing(self, prefix='', location='Campus', until='9999-12-31', status='guardado',
                category='', page=None, page_size=24, depth=5):
        with self.lock:
            if status not in ('guardado', 'devolvido', 'todos'):
                raise ValueError('Situação inválida.')
            until = date.fromisoformat(until).isoformat()
            if category and category not in (*CATEGORIES, 'Outros'):
                raise ValueError('Categoria inválida.')
            depth = int(depth)
            if not 1 <= depth <= 7:
                raise ValueError('A profundidade visual deve estar entre 1 e 7.')
            places = descendants(location)
            ids, trie_visits = self.trie.prefix(prefix)
            if status == 'guardado':
                keys, avl_visits = self.avl.range(('', 0), (until, float('inf')))
                candidates = [self.by_id[key[1]] for key in keys]
            else:
                avl_visits = 0
                candidates = sorted(self.by_id.values(), key=lambda x: (x['deadline'], x['id']))
            items = [dict(x) for x in candidates if x['id'] in ids and x['location'] in places
                     and x['deadline'] <= until and (status == 'todos' or x['status'] == status)
                     and (not category or x['category'] == category)]
            total = len(items)
            pages, current_page = 1, 1
            if page is not None:
                current_page, page_size = int(page), int(page_size)
                if current_page < 1 or not 1 <= page_size <= 100:
                    raise ValueError('Página deve ser positiva e tamanho entre 1 e 100.')
                pages = max(1, (total + page_size - 1) // page_size)
                current_page = min(current_page, pages)
                start = (current_page - 1) * page_size
                items = items[start:start + page_size]
            count = self.avl.root.size if self.avl.root else 0
            median = self.by_id[self.avl.select((count - 1) // 2)[1]] if count else None
            return dict(items=items, total=total, pagination=dict(page=current_page, pages=pages, pageSize=page_size),
                        categories=CATEGORIES, summary=dict(total=len(self.by_id), guardados=count,
                        devolvidos=len(self.by_id) - count, medianDeadline=median['deadline'] if median else None),
                        metrics=dict(avlVisited=avl_visits, trieVisited=trie_visits,
                        height=self.avl.root.height if self.avl.root else 0,
                        rotations=self.avl.rotations), tree=self.avl.snapshot(depth), locations=LOCATIONS)

    def create(self, payload):
        clean = validate(payload)
        with self.lock:
            item = dict(clean, id=max(self.by_id, default=0) + 1, status='guardado')
            self._save_change([*self.storage.items, item], current=item)
            return dict(item)

    def edit(self, item_id, payload):
        clean = validate(payload)
        with self.lock:
            if item_id not in self.by_id:
                raise KeyError('Objeto não encontrado.')
            previous = self.by_id[item_id]
            item = dict(clean, id=item_id, status=previous['status'])
            items = [item if x['id'] == item_id else x for x in self.storage.items]
            self._save_change(items, previous, item)
            return dict(item)

    def change(self, item_id, action):
        with self.lock:
            if item_id not in self.by_id:
                raise KeyError('Objeto não encontrado.')
            if action not in ('return', 'delete'):
                raise ValueError('Operação inválida.')
            items = [dict(x) for x in self.storage.items]
            if action == 'delete':
                items = [x for x in items if x['id'] != item_id]
            else:
                for item in items:
                    if item['id'] == item_id:
                        item['status'] = 'devolvido'
            current = next((x for x in items if x['id'] == item_id), None)
            self._save_change(items, self.by_id[item_id], current)
            return dict(ok=True)
