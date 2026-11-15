import unittest
from app.structures.trie import Trie
from app.structures.locations import descendants
from app.lab import experiment


class StructureTests(unittest.TestCase):
    def test_trie_removal_preserves_shared_paths(self):
        trie = Trie()
        for text, ident in [('Óculos', 1), ('oculos', 2), ('Ocarina', 3), ('Oc', 4)]:
            trie.insert(text, ident)
        trie.remove('ÓCULOS', 1)
        self.assertEqual(trie.prefix('ocu')[0], {2})
        trie.remove('oculos', 2)
        self.assertEqual(trie.prefix('ocu')[0], set())
        self.assertEqual(trie.prefix('oc')[0], {3, 4})
        trie.remove('Oc', 4)
        trie.remove('inexistente', 999)
        self.assertEqual(trie.prefix('oc')[0], {3})
        trie.remove('Ocarina', 3)
        self.assertEqual(trie.root, {'children': {}, 'ids': set()})

    def test_prefix_accents_duplicates_and_empty(self):
        trie = Trie()
        for name, ident in [('Óculos', 1), ('Ocarina', 2), ('Garrafa', 3), ('Garrafa', 4)]:
            trie.insert(name, ident)
        self.assertEqual(trie.prefix('ÓC')[0], {1, 2})
        self.assertEqual(trie.prefix('gar')[0], {3, 4})
        self.assertEqual(trie.prefix('')[0], {1, 2, 3, 4})
        self.assertEqual(trie.prefix('xyz')[0], set())

    def test_location_subtrees(self):
        self.assertEqual(descendants('Bloco A'), {'Bloco A', 'Sala A101', 'Laboratório'})
        self.assertEqual(descendants('Quadra'), {'Quadra'})
        self.assertEqual(len(descendants('Campus')), 1132)
        with self.assertRaises(ValueError):
            descendants('Inexistente')

    def test_lab_steps_and_limits(self):
        result = experiment([30, 10, 20])
        self.assertEqual(result['ordered'], [10, 20, 30])
        self.assertEqual(result['rotations'], 2)
        self.assertEqual(result['steps'][-1]['tree']['key'][0], 20)
        self.assertEqual(result['steps'][0]['tree']['key'][0], 30)
        self.assertEqual(experiment([2, 2])['ordered'], [2])
        self.assertEqual(experiment([])['height'], 0)
        for invalid in (None, '1', [True], [1.5], [10000], list(range(32))):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                experiment(invalid)
