import math
import random
import unittest
from app.structures.avl import AVL


class AVLTests(unittest.TestCase):
    def verify(self, tree, expected):
        def visit(node, low=None, high=None):
            if node is None:
                return 0
            if low is not None:
                self.assertGreater(node.key, low)
            if high is not None:
                self.assertLess(node.key, high)
            left = visit(node.left, low, node.key)
            right = visit(node.right, node.key, high)
            self.assertLessEqual(abs(left-right), 1)
            self.assertEqual(node.height, max(left, right) + 1)
            return node.height
        visit(tree.root)
        values, _ = tree.range((-999999, 0), (999999, 0))
        self.assertEqual([x[0] for x in values], sorted(expected))

    def test_four_rotations(self):
        for values in ([30, 20, 10], [10, 20, 30], [30, 10, 20], [10, 30, 20]):
            with self.subTest(values=values):
                tree = AVL()
                for value in values:
                    tree.insert((value, 0))
                self.verify(tree, values)
                self.assertEqual(tree.root.key, (20, 0))

    def test_random_operations_against_set(self):
        rng, tree, expected = random.Random(42), AVL(), set()
        for _ in range(2500):
            value = rng.randrange(200)
            if rng.random() < .55:
                tree.insert((value, 0)); expected.add(value)
            else:
                tree.remove((value, 0)); expected.discard(value)
            self.verify(tree, expected)

    def test_sorted_input_and_range_pruning(self):
        tree = AVL()
        for value in range(1000):
            tree.insert((value, 0))
        self.verify(tree, range(1000))
        self.assertLessEqual(tree.root.height, 2 * math.log2(1001))
        keys, visited = tree.range((500, 0), (505, 0))
        self.assertEqual(keys, [(v, 0) for v in range(500, 506)])
        self.assertLess(visited, 30)

    def test_delete_all_and_duplicates(self):
        tree = AVL()
        for value in [3, 1, 2, 5, 4, 3]:
            tree.insert((value, 0))
        self.verify(tree, {1, 2, 3, 4, 5})
        for value in [3, 1, 5, 2, 4, 999]:
            tree.remove((value, 0))
        self.verify(tree, set())
        self.assertIsNone(tree.snapshot())

    def test_compound_keys_and_interval_boundaries(self):
        tree = AVL()
        for key in [('2026-11-15', 2), ('2026-11-15', 1), ('2026-11-16', 3)]:
            tree.insert(key)
        keys, _ = tree.range(('', 0), ('2026-11-15', float('inf')))
        self.assertEqual(keys, [('2026-11-15', 1), ('2026-11-15', 2)])
