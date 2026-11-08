from datetime import date, timedelta


def seed():
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
    return [dict(id=i, name=n, description=d, location=l,
                 deadline=(date.today() + timedelta(days=days)).isoformat(), status='guardado')
            for i, (n, d, l, days) in enumerate(examples, 1)]
