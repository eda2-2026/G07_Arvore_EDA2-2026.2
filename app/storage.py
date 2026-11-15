import json
import os
from collections import Counter
from pathlib import Path
from app.seed import seed
from app.validation import validate
from app.categories import infer_category
from app.categories import CATEGORIES


class Storage:
    def __init__(self, path, demo=False):
        self.path = Path(path)
        if self.path.exists():
            self.items = json.loads(self.path.read_text(encoding='utf-8'))
            if not isinstance(self.items, list):
                raise ValueError('Arquivo de dados deve conter uma lista.')
            ids = set()
            for item in self.items:
                validate(item)
                item.setdefault('category', infer_category(item['name']))
                if (type(item.get('id')) is not int or item['id'] < 1
                        or item['id'] in ids or item.get('status') not in ('guardado', 'devolvido')):
                    raise ValueError('Arquivo de dados contém identificador ou situação inválida.')
                ids.add(item['id'])
        else:
            self.items = seed(demo=demo)
            self.save(self.items)

    def save(self, items):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.path.with_suffix('.tmp')
        temporary.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding='utf-8')
        os.replace(temporary, self.path)
        self.items = items

    def populate(self):
        """Completa mil objetos por categoria, preservando cadastros existentes."""
        counts = Counter(item['category'] for item in self.items)
        missing = {category: max(0, 1000 - counts[category]) for category in CATEGORIES}
        items = list(self.items)
        ident = max((item['id'] for item in items), default=0)
        added = 0
        for candidate in seed():
            if missing[candidate['category']]:
                ident += 1
                items.append(dict(candidate, id=ident))
                missing[candidate['category']] -= 1
                added += 1
        if added:
            self.save(items)
        return added
