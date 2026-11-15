from app.structures.avl import AVL
from collections import deque


def experiment(values, removals=None, target=None, position=1):
    removals = [] if removals is None else removals
    for sequence in (values, removals):
        if (not isinstance(sequence, list) or len(sequence) > 31
                or any(type(v) is not int or abs(v) > 9999 for v in sequence)):
            raise ValueError('Informe até 31 números inteiros entre -9999 e 9999 em cada sequência.')
    if target is not None and (type(target) is not int or abs(target) > 9999):
        raise ValueError('Busca deve ser um inteiro entre -9999 e 9999.')
    if type(position) is not int or not 1 <= position <= 31:
        raise ValueError('A posição deve estar entre 1 e 31.')
    tree, steps = AVL(), []
    for action, sequence in [('inserir', values), ('remover', removals)]:
        for value in sequence:
            before = tree.rotations
            existed = tree.trace((value, 0))[1]
            (tree.insert if action == 'inserir' else tree.remove)((value, 0))
            path, found = tree.trace((target, 0)) if target is not None else ([], False)
            steps.append(dict(value=value, action=action, changed=not existed if action == 'inserir' else existed,
                              rotations=tree.rotations - before, tree=tree.snapshot(),
                              path=[key[0] for key in path], found=found))
    ordered, visited = tree.range((-10000, 0), (10000, 0))
    traversals = {'preorder': [], 'postorder': [], 'breadth': []}
    def dfs(node):
        if node:
            traversals['preorder'].append(node.key[0])
            dfs(node.left)
            dfs(node.right)
            traversals['postorder'].append(node.key[0])
    dfs(tree.root)
    queue = deque([tree.root] if tree.root else [])
    leaves = 0
    while queue:
        node = queue.popleft()
        traversals['breadth'].append(node.key[0])
        leaves += int(not node.left and not node.right)
        queue.extend(child for child in (node.left, node.right) if child)
    count = tree.root.size if tree.root else 0
    return dict(steps=steps, ordered=[key[0] for key in ordered], visited=visited,
                rotations=tree.rotations, height=tree.root.height if tree.root else 0,
                traversals=traversals, count=count, leaves=leaves,
                median=tree.select((count - 1) // 2)[0] if count else None,
                rank=tree.rank((target, 0)) if target is not None else None, target=target,
                position=position, selected=tree.select(position - 1)[0] if position <= count else None)
