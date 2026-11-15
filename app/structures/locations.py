"""Árvore n-ária: percurso DFS para recuperar uma subárvore de locais."""
LOCATIONS = {
    'Campus': {
        'Bloco A': {'Sala A101': {}, 'Laboratório': {}},
        'Bloco B': {'Sala B201': {}, 'Auditório': {}},
        'Biblioteca': {'Sala de leitura': {}},
        'Convivência': {'Cantina': {}, 'Quadra': {}}
    }
}

# 1.000 salas adicionais em 20 setores e 100 prédios; nomes são únicos.
for sector in range(1, 21):
    LOCATIONS['Campus'][f'Setor {sector:02d}'] = {
        f'Prédio {sector:02d}-{building}': {
            f'Sala {sector:02d}-{building}-{room:02d}': {} for room in range(1, 11)
        } for building in range(1, 6)
    }


def _index(tree):
    result = {}
    for label, children in tree.items():
        result[label] = children
        result.update(_index(children))
    return result


LOCATION_INDEX = _index(LOCATIONS)


def descendants(name):
    children = LOCATION_INDEX.get(name)
    if children is None:
        raise ValueError('Local inválido.')
    result, stack = {name}, [children]
    while stack:
        for label, nested in stack.pop().items():
            result.add(label)
            stack.append(nested)
    return result
