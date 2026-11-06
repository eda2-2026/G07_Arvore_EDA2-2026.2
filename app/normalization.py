import unicodedata


def normalize(text):
    """Busca independente de caixa e acentos, preservando os dados originais."""
    return ''.join(c for c in unicodedata.normalize('NFD', text.casefold())
                   if unicodedata.category(c) != 'Mn').strip()
