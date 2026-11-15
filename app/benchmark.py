"""Experimento reproduzível com dados idênticos para AVL, BST e busca linear."""
import random
from time import perf_counter
from app.structures.avl import AVL


class BST:
    def __init__(self):
        self.root = None
        self.height = 0
        self.comparisons = 0

    def insert(self, value):
        if self.root is None:
            self.root = [value, None, None]
            self.height = 1
            return
        node, depth = self.root, 1
        while True:
            self.comparisons += 1
            if value == node[0]:
                return
            direction = 1 if value < node[0] else 2
            depth += 1
            if node[direction] is None:
                node[direction] = [value, None, None]
                self.height = max(self.height, depth)
                return
            node = node[direction]

    def search(self, value):
        node, visited = self.root, 0
        while node:
            visited += 1
            if node[0] == value:
                return True, visited
            node = node[1 if value < node[0] else 2]
        return False, visited


def benchmark(size=1000, scenario='random'):
    if type(size) is not int or size not in (100, 1000, 5000):
        raise ValueError('Escolha 100, 1000 ou 5000 elementos.')
    if scenario not in ('random', 'sorted', 'reversed', 'almost'):
        raise ValueError('Cenário inválido.')
    rng = random.Random(42)
    values = list(range(size))
    if scenario == 'random':
        rng.shuffle(values)
    elif scenario == 'reversed':
        values.reverse()
    elif scenario == 'almost':
        for _ in range(max(1, size // 100)):
            i, j = rng.randrange(size), rng.randrange(size)
            values[i], values[j] = values[j], values[i]
    targets = rng.sample(range(size), 100) + [-1, size]
    rows = []
    reference = [value in values for value in targets]
    for name in ('AVL', 'BST', 'Sequencial'):
        started = perf_counter()
        if name == 'AVL':
            tree = AVL()
            for value in values:
                tree.insert((value, 0))
            tree_height, comparisons, rotations = tree.root.height, tree.comparisons, tree.rotations
        elif name == 'BST':
            tree = BST()
            for value in values:
                tree.insert(value)
            tree_height, comparisons, rotations = tree.height, tree.comparisons, 0
        else:
            tree = list(values)
            tree_height, comparisons, rotations = None, 0, 0
        build_ms = (perf_counter() - started) * 1000
        started, visits, answers = perf_counter(), 0, []
        for target in targets:
            if name == 'AVL':
                path, found = tree.trace((target, 0))
                visited = len(path)
            elif name == 'BST':
                found, visited = tree.search(target)
            else:
                found, visited = False, 0
                for value in tree:
                    visited += 1
                    if value == target:
                        found = True
                        break
            answers.append(found)
            visits += visited
        search_ms = (perf_counter() - started) * 1000
        if answers != reference:
            raise RuntimeError('Resultados das estruturas divergiram.')
        rows.append(dict(name=name, height=tree_height, rotations=rotations, buildComparisons=comparisons,
                         buildMs=round(build_ms, 3), searchMs=round(search_ms, 3),
                         searchVisits=visits, averageVisits=round(visits / len(targets), 2)))
    return dict(size=size, scenario=scenario, seed=42, queries=len(targets), hits=sum(reference),
                rows=rows, verified=True)
