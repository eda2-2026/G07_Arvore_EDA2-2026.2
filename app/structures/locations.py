"""Árvore n-ária: percurso DFS para recuperar uma subárvore de locais."""
LOCATIONS = {
    'Campus': {
        'Bloco A': {'Sala A101': {}, 'Laboratório': {}},
        'Bloco B': {'Sala B201': {}, 'Auditório': {}},
        'Biblioteca': {'Sala de leitura': {}},
        'Convivência': {'Cantina': {}, 'Quadra': {}}
    }
}


def descendants(name):
    def find(tree):
        for label, children in tree.items():
            if label == name:
                return children
            found = find(children)
            if found is not None:
                return found
        return None
    children = find(LOCATIONS)
    if children is None:
        raise ValueError('Local inválido.')
    result, stack = {name}, [children]
    while stack:
        for label, nested in stack.pop().items():
            result.add(label)
            stack.append(nested)
    return result
