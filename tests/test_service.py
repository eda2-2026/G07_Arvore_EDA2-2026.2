import json
import tempfile
import random
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from unittest.mock import patch
from app.service import Service
from app.storage import Storage
from app.normalization import normalize
from app.structures.locations import descendants

PAYLOAD = dict(name='Óculos azul', description='Estojo azul.', location='Laboratório', deadline='2026-11-15')


class ServiceTests(unittest.TestCase):
    def test_edit_updates_existing_indexes_and_preserves_status(self):
        item = self.service.create(PAYLOAD)
        avl, trie = self.service.avl, self.service.trie
        edited = self.service.edit(item['id'], dict(PAYLOAD, name='Mochila roxa', deadline='2026-11-20', location='Cantina'))
        self.assertEqual(edited['id'], item['id'])
        self.assertIs(self.service.avl, avl)
        self.assertIs(self.service.trie, trie)
        self.assertEqual(self.service.listing(prefix='oculos az')['items'], [])
        self.assertEqual(self.service.listing(prefix='moch', until='2026-11-19')['items'], [])
        self.assertEqual(self.service.listing(prefix='moch', location='Convivência')['items'], [edited])
        self.service.change(item['id'], 'return')
        self.service.edit(item['id'], dict(PAYLOAD, name='Mochila atualizada'))
        self.assertEqual(self.service.listing(prefix='moch', status='devolvido')['items'][0]['status'], 'devolvido')
        self.assertEqual(self.service.listing(prefix='moch')['items'], [])
        self.assertEqual(Service(Storage(self.path)).listing(status='todos')['items'],
                         self.service.listing(status='todos')['items'])

    def test_failed_edit_and_delete_preserve_indexes(self):
        item = self.service.create(PAYLOAD)
        before = self.service.listing(status='todos')
        with patch('app.storage.os.replace', side_effect=OSError('disco indisponível')):
            for operation in (lambda: self.service.edit(item['id'], dict(PAYLOAD, name='Outro')),
                              lambda: self.service.change(item['id'], 'delete'),
                              lambda: self.service.change(item['id'], 'return')):
                with self.assertRaises(OSError):
                    operation()
                self.assertEqual(self.service.listing(status='todos'), before)

    def test_random_mutations_match_rebuilt_indexes(self):
        rng = random.Random(104)
        for step in range(150):
            ids = list(self.service.by_id)
            action = rng.choice(['create', 'edit', 'return', 'delete']) if ids else 'create'
            payload = dict(PAYLOAD, name=rng.choice(['Óculos', 'Garrafa', 'Caderno']) + str(step % 4),
                           deadline=f'2026-11-{rng.randrange(1,29):02d}', location=rng.choice(['Cantina', 'Laboratório']))
            if action == 'create':
                self.service.create(payload)
            elif action == 'edit':
                self.service.edit(rng.choice(ids), payload)
            else:
                self.service.change(rng.choice(ids), action)
            rebuilt = Service(Storage(self.path))
            for status in ('guardado', 'devolvido', 'todos'):
                for prefix in ('', 'ocu', 'gar'):
                    self.assertEqual(self.service.listing(prefix=prefix, status=status)['items'],
                                     rebuilt.listing(prefix=prefix, status=status)['items'])
            self.assertEqual(self.service.avl.range(('', 0), ('9999-12-31', float('inf')))[0],
                             rebuilt.avl.range(('', 0), ('9999-12-31', float('inf')))[0])

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'items.json'
        self.service = Service(Storage(self.path))

    def test_crud_and_persistence(self):
        item = self.service.create(PAYLOAD)
        result = self.service.listing(prefix='OCULOS AZ', location='Bloco A', until='2026-11-15')
        self.assertEqual([x['id'] for x in result['items']], [item['id']])
        self.service.change(item['id'], 'return')
        self.assertEqual(self.service.listing(prefix='oculos az')['items'], [])
        self.assertEqual(len(self.service.listing(prefix='oculos az', status='devolvido')['items']), 1)
        loaded = Service(Storage(self.path))
        self.assertEqual(loaded.by_id[item['id']]['status'], 'devolvido')
        loaded.change(item['id'], 'delete')
        self.assertNotIn(item['id'], Service(Storage(self.path)).by_id)

    def test_invalid_payloads_and_filters(self):
        for invalid in (None, [], {}, dict(PAYLOAD, name=' '), dict(PAYLOAD, name=3),
                        dict(PAYLOAD, description='x'*301), dict(PAYLOAD, deadline='2026-02-30'),
                        dict(PAYLOAD, location='Nada')):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                self.service.create(invalid)
        for query in (dict(status='x'), dict(until='x'), dict(location='x')):
            with self.assertRaises(ValueError):
                self.service.listing(**query)
        with self.assertRaises(KeyError):
            self.service.change(9999, 'delete')

    def test_concurrent_creates_and_order(self):
        with ThreadPoolExecutor(max_workers=8) as pool:
            created = list(pool.map(lambda _: self.service.create(PAYLOAD), range(24)))
        self.assertEqual(len({x['id'] for x in created}), 24)
        items = self.service.listing()['items']
        self.assertEqual([(x['deadline'], x['id']) for x in items], sorted((x['deadline'], x['id']) for x in items))
        self.assertEqual(len(Storage(self.path).items), 33)

    def test_failed_write_keeps_memory_and_disk(self):
        before = self.path.read_bytes()
        with patch('app.storage.os.replace', side_effect=OSError('disco indisponível')):
            with self.assertRaises(OSError):
                self.service.create(PAYLOAD)
        self.assertEqual(self.path.read_bytes(), before)
        self.assertEqual(len(self.service.by_id), 9)

    def test_corrupt_data_is_not_overwritten(self):
        self.path.write_text('[{"id": 1}]', encoding='utf-8')
        with self.assertRaises(ValueError):
            Storage(self.path)
        self.assertEqual(json.loads(self.path.read_text()), [{'id': 1}])

    def test_filters_against_linear_reference(self):
        created = [self.service.create(dict(PAYLOAD, name=name, location=location, deadline=deadline))
                   for name, location, deadline in [
                       ('Garrafa vermelha', 'Sala A101', '2026-11-14'),
                       ('Óculos preto', 'Cantina', '2026-11-15'),
                       ('Caderno', 'Laboratório', '2026-11-16')]]
        self.service.change(created[1]['id'], 'return')
        for prefix in ('', 'gar', 'OCU', 'zzzz'):
            for location in ('Campus', 'Bloco A', 'Cantina'):
                for status in ('guardado', 'devolvido', 'todos'):
                    for until in ('2026-11-15', '9999-12-31'):
                        with self.subTest(prefix=prefix, location=location, status=status, until=until):
                            expected = sorted((dict(x) for x in self.service.storage.items
                                if normalize(x['name']).startswith(normalize(prefix))
                                and x['location'] in descendants(location)
                                and x['deadline'] <= until
                                and (status == 'todos' or x['status'] == status)),
                                key=lambda x: (x['deadline'], x['id']))
                            self.assertEqual(self.service.listing(prefix, location, until, status)['items'], expected)
