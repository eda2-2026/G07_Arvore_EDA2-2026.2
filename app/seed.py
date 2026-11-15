from datetime import date, timedelta
import random
from app.categories import CATEGORIES, infer_category
from app.structures.locations import LOCATION_INDEX


def seed(demo=False, per_category=1000, today=None):
    today = today or date.today()
    examples = [
        ('Garrafa azul', 'Garrafa térmica encontrada após a aula.', 'Sala A101', 3),
        ('Calculadora científica', 'Modelo escolar com capa cinza.', 'Laboratório', 7),
        ('Óculos de grau', 'Armação preta em estojo marrom.', 'Sala de leitura', 1),
        ('Caderno verde', 'Caderno sem identificação na capa.', 'Cantina', 5),
        ('Chaveiro vermelho', 'Duas chaves e um pingente.', 'Quadra', -1),
        ('Fone de ouvido', 'Fone com fio e estojo branco.', 'Auditório', 10),
        ('Guarda-chuva', 'Modelo preto dobrável.', 'Sala B201', 2),
        ('Garrafa inox', 'Garrafa pequena sem tampa.', 'Biblioteca', 4),
        ('Estojo amarelo', 'Lápis e canetas no interior.', 'Bloco A', 6),
    ]
    if demo:
        return [dict(id=i, name=n, description=d, location=l, category=infer_category(n),
                     deadline=(today + timedelta(days=days)).isoformat(), status='guardado')
                for i, (n, d, l, days) in enumerate(examples, 1)]
    rng = random.Random(20262)
    nouns = ['Garrafa térmica', 'Calculadora científica', 'Óculos de grau', 'Caderno universitário',
             'Chaveiro', 'Fone de ouvido', 'Guarda-chuva dobrável', 'Estojo escolar',
             'Mochila', 'Carregador USB', 'Documento acadêmico', 'Roupa esportiva']
    colors = ['azul', 'preto', 'verde', 'cinza', 'vermelho', 'branco', 'bege', 'vinho']
    details = ['com etiqueta de identificação em branco', 'com pequenas marcas de uso',
               'em bom estado de conservação', 'com alça de tecido', 'com detalhe listrado']
    places = [name for name, children in LOCATION_INDEX.items() if not children]
    items = []
    for category, noun in zip(CATEGORIES, nouns):
        for number in range(per_category):
            ident = len(items) + 1
            items.append(dict(id=ident, name=f'{noun} {rng.choice(colors)}', category=category,
                              description=f'{noun} {rng.choice(details)}. Registro de balcão {ident:05d}; encontrado após atividade no campus.',
                              location=rng.choice(places), deadline=(today + timedelta(days=rng.randrange(-45, 91))).isoformat(),
                              status='devolvido' if number % 4 == 0 else 'guardado'))
    return items
