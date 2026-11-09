from app.structures.avl import AVL


def experiment(values):
    if (not isinstance(values, list) or len(values) > 31
            or any(type(v) is not int or abs(v) > 9999 for v in values)):
        raise ValueError('Informe até 31 números inteiros entre -9999 e 9999.')
    tree, steps = AVL(), []
    for value in values:
        before = tree.rotations
        tree.insert((value, 0))
        steps.append(dict(value=value, rotations=tree.rotations - before, tree=tree.snapshot()))
    ordered, visited = tree.range((-10000, 0), (10000, 0))
    return dict(steps=steps, ordered=[key[0] for key in ordered], visited=visited,
                rotations=tree.rotations, height=tree.root.height if tree.root else 0)
