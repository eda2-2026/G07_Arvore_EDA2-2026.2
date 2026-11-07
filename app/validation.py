from datetime import date
from app.structures.locations import descendants


def validate(payload):
    if not isinstance(payload, dict):
        raise ValueError('Envie um objeto JSON.')
    result = {}
    for field, limit in [('name', 80), ('description', 300), ('location', 50)]:
        value = payload.get(field)
        if not isinstance(value, str) or not value.strip() or len(value.strip()) > limit:
            raise ValueError(f'Campo {field}: informe entre 1 e {limit} caracteres.')
        result[field] = value.strip()
    descendants(result['location'])
    try:
        result['deadline'] = date.fromisoformat(payload['deadline']).isoformat()
    except (ValueError, TypeError, KeyError):
        raise ValueError('Informe um prazo válido (AAAA-MM-DD).') from None
    return result
