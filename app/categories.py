"""Categorias do balcão e inferência compatível com registros antigos."""
from app.normalization import normalize

CATEGORIES = ('Garrafas', 'Calculadoras', 'Óculos', 'Cadernos', 'Chaves', 'Fones',
              'Guarda-chuvas', 'Estojos', 'Mochilas', 'Carregadores', 'Documentos', 'Roupas')
PREFIXES = ('garrafa', 'calculadora', 'oculos', 'caderno', 'chave', 'fone',
            'guarda-chuva', 'estojo', 'mochila', 'carregador', 'documento', 'roupa')


def infer_category(name):
    text = normalize(name)
    return next((category for prefix, category in zip(PREFIXES, CATEGORIES) if text.startswith(prefix)), 'Outros')
