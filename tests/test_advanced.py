from collections import Counter
from datetime import date
import json
import math
from pathlib import Path
import random
import tempfile
import unittest
from app.seed import seed
from app.categories import CATEGORIES
from app.structures.locations import LOCATION_INDEX
from app.structures.avl import AVL
from app.storage import Storage
from app.service import Service
from app.lab import experiment
from app.benchmark import benchmark


class AdvancedTests(unittest.TestCase):
    def test_full_dataset_is_reproducible_and_balanced_by_category(self):
        items = seed(today=date(2026, 11, 15))
        self.assertEqual(items, seed(today=date(2026, 11, 15)))
        self.assertEqual(len(items), 12000)
        self.assertEqual(Counter(x['category'] for x in items), {category: 1000 for category in CATEGORIES})
        self.assertEqual(len({x['id'] for x in items}), 12000)
        self.assertEqual(Counter(x['status'] for x in items), {'guardado': 9000, 'devolvido': 3000})
        self.assertEqual(len(LOCATION_INDEX), 1132)
        self.assertTrue(all(x['location'] in LOCATION_INDEX for x in items))

    def test_population_preserves_existing_items_and_is_idempotent(self):
        with tempfile.TemporaryDirectory() as directory:
            store = Storage(Path(directory) / 'items.json', demo=True)
            original = [dict(x) for x in store.items]
            self.assertEqual(store.populate(), 11991)
            self.assertEqual(store.items[:9], original)
            self.assertEqual(store.populate(), 0)
            loaded = Storage(store.path)
            self.assertEqual(Counter(x['category'] for x in loaded.items), {category: 1000 for category in CATEGORIES})

    def test_large_pagination_category_and_bounded_snapshot(self):
        with tempfile.TemporaryDirectory() as directory:
            service = Service(Storage(Path(directory) / 'items.json'))
            result = service.listing(page=1)
            self.assertEqual(len(result['items']), 24)
            self.assertEqual(result['total'], 9000)
            self.assertEqual(result['pagination']['pages'], 375)
            def count(node):
                return 0 if node is None else 1 + count(node['left']) + count(node['right'])
            self.assertLessEqual(count(result['tree']), 31)
            self.assertEqual(result['tree']['size'], 9000)
            self.assertLessEqual(result['metrics']['height'], 2 * math.log2(9001))
            second = service.listing(page=2)
            self.assertFalse({x['id'] for x in result['items']} & {x['id'] for x in second['items']})
            for category in CATEGORIES:
                filtered = service.listing(category=category, status='todos', page=999999)
                self.assertEqual(filtered['total'], 1000)
                self.assertTrue(all(x['category'] == category for x in filtered['items']))
            for args in (dict(page=0), dict(page_size=101, page=1), dict(depth=8), dict(category='x')):
                with self.assertRaises(ValueError):
                    service.listing(**args)

    def test_legacy_records_receive_inferred_category(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'items.json'
            records = seed(demo=True)
            for item in records:
                item.pop('category')
            path.write_text(json.dumps(records), encoding='utf-8')
            loaded = Storage(path)
            self.assertEqual(loaded.items[0]['category'], 'Garrafas')
            self.assertEqual(loaded.items[2]['category'], 'Óculos')

    def test_order_statistics_after_random_insertions_and_removals(self):
        tree, expected, rng = AVL(), set(), random.Random(9)
        for _ in range(500):
            value = rng.randrange(100)
            if rng.random() < .6:
                tree.insert((value, 0)); expected.add(value)
            else:
                tree.remove((value, 0)); expected.discard(value)
            values = sorted(expected)
            self.assertEqual(tree.root.size if tree.root else 0, len(values))
            for index, key in enumerate(values):
                self.assertEqual(tree.select(index), (key, 0))
                self.assertEqual(tree.rank((key, 0)), index)
            self.assertEqual(tree.rank((200, 0)), len(values))
        for index in (-1, len(expected), True):
            with self.assertRaises(ValueError):
                tree.select(index)

    def test_lab_removal_paths_and_traversals(self):
        result = experiment([30, 10, 20, 40], [10, 999], target=40, position=2)
        self.assertEqual(result['ordered'], [20, 30, 40])
        self.assertEqual(result['median'], 30)
        self.assertEqual(result['selected'], 30)
        self.assertEqual(result['rank'], 2)
        self.assertEqual(result['steps'][-1]['path'][-1], 40)
        self.assertTrue(result['steps'][-1]['found'])
        self.assertFalse(result['steps'][-1]['changed'])
        for traversal in result['traversals'].values():
            self.assertEqual(sorted(traversal), result['ordered'])
        self.assertEqual(experiment([1], [1])['count'], 0)
        for kwargs in (dict(target=True), dict(position=0), dict(removals=[1.2])):
            with self.assertRaises(ValueError):
                experiment([1], **kwargs)

    def test_benchmark_scenarios_share_answers_and_expose_bst_degradation(self):
        for scenario in ('random', 'sorted', 'reversed', 'almost'):
            result = benchmark(100, scenario)
            self.assertTrue(result['verified'])
            self.assertEqual(result['hits'], 100)
            self.assertEqual(result['queries'], 102)
            self.assertEqual(len(result['rows']), 3)
            if scenario in ('sorted', 'reversed'):
                avl, bst, linear = result['rows']
                self.assertEqual(bst['height'], 100)
                self.assertEqual(bst['buildComparisons'], 4950)
                self.assertLess(avl['height'], 10)
                self.assertLess(avl['searchVisits'], linear['searchVisits'])
        for args in ((101, 'random'), (True, 'random'), (100, 'invalid')):
            with self.assertRaises(ValueError):
                benchmark(*args)
