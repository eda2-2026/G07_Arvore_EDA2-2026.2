"""AVL com chaves compostas (prazo, id), remoção e consulta por intervalo."""
from dataclasses import dataclass


@dataclass
class Node:
    key: tuple
    left: object = None
    right: object = None
    height: int = 1


def height(node):
    return node.height if node else 0


class AVL:
    def __init__(self):
        self.root = None
        self.rotations = 0

    def _update(self, node):
        node.height = 1 + max(height(node.left), height(node.right))

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

    def snapshot(self):
        def visit(node):
            if node is None:
                return None
            return dict(key=list(node.key), height=node.height,
                        balance=height(node.left) - height(node.right),
                        left=visit(node.left), right=visit(node.right))
        return visit(self.root)
