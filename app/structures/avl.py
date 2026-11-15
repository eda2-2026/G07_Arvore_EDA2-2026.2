"""AVL com chaves compostas (prazo, id), remoção e consulta por intervalo."""
from dataclasses import dataclass


@dataclass
class Node:
    key: tuple
    left: object = None
    right: object = None
    height: int = 1
    size: int = 1


def height(node):
    return node.height if node else 0


class AVL:
    def __init__(self):
        self.root = None
        self.rotations = 0
        self.comparisons = 0

    def _update(self, node):
        node.height = 1 + max(height(node.left), height(node.right))
        node.size = 1 + (node.left.size if node.left else 0) + (node.right.size if node.right else 0)

    def _rotate(self, node, left):
        pivot = node.right if left else node.left
        if left:
            node.right, pivot.left = pivot.left, node
        else:
            node.left, pivot.right = pivot.right, node
        self._update(node)
        self._update(pivot)
        self.rotations += 1
        return pivot

    def _balance(self, node):
        self._update(node)
        balance = height(node.left) - height(node.right)
        if balance > 1:
            if height(node.left.left) < height(node.left.right):
                node.left = self._rotate(node.left, True)
            return self._rotate(node, False)
        if balance < -1:
            if height(node.right.right) < height(node.right.left):
                node.right = self._rotate(node.right, False)
            return self._rotate(node, True)
        return node

    def insert(self, key):
        def visit(node):
            if node is None:
                return Node(key)
            self.comparisons += 1
            if key < node.key:
                node.left = visit(node.left)
            elif key > node.key:
                node.right = visit(node.right)
            else:
                return node
            return self._balance(node)
        self.root = visit(self.root)

    def remove(self, key):
        def visit(node, target):
            if node is None:
                return None
            if target < node.key:
                node.left = visit(node.left, target)
            elif target > node.key:
                node.right = visit(node.right, target)
            else:
                if node.left is None:
                    return node.right
                if node.right is None:
                    return node.left
                successor = node.right
                while successor.left:
                    successor = successor.left
                node.key = successor.key
                node.right = visit(node.right, successor.key)
            return self._balance(node)
        self.root = visit(self.root, key)

    def range(self, low, high):
        result, visited = [], 0
        def visit(node):
            nonlocal visited
            if node is None:
                return
            visited += 1
            if node.key > low:
                visit(node.left)
            if low <= node.key <= high:
                result.append(node.key)
            if node.key < high:
                visit(node.right)
        visit(self.root)
        return result, visited

    def trace(self, key):
        path, node = [], self.root
        while node:
            path.append(node.key)
            if key == node.key:
                return path, True
            node = node.left if key < node.key else node.right
        return path, False

    def select(self, index):
        """Retorna a chave de posição zero-based em O(log n), usando tamanhos."""
        if type(index) is not int or index < 0 or not self.root or index >= self.root.size:
            raise ValueError('Posição fora da árvore.')
        node = self.root
        while node:
            left = node.left.size if node.left else 0
            if index == left:
                return node.key
            if index < left:
                node = node.left
            else:
                index -= left + 1
                node = node.right

    def rank(self, key):
        """Quantidade de chaves estritamente menores que key, em O(log n)."""
        rank, node = 0, self.root
        while node:
            if key <= node.key:
                node = node.left
            else:
                rank += 1 + (node.left.size if node.left else 0)
                node = node.right
        return rank

    def snapshot(self, max_depth=None):
        def visit(node, depth=0):
            if node is None:
                return None
            truncated = max_depth is not None and depth >= max_depth - 1
            return dict(key=list(node.key), height=node.height,
                        size=node.size, truncated=bool(truncated and (node.left or node.right)),
                        balance=height(node.left) - height(node.right),
                        left=None if truncated else visit(node.left, depth + 1),
                        right=None if truncated else visit(node.right, depth + 1))
        return visit(self.root)
