import json
import os
from pathlib import Path
from app.seed import seed
from app.validation import validate


class Storage:
    def __init__(self, path):
        self.path = Path(path)
        if self.path.exists():
            self.items = json.loads(self.path.read_text(encoding='utf-8'))
            if not isinstance(self.items, list):
                raise ValueError('Arquivo de dados deve conter uma lista.')
            ids = set()
            for item in self.items:
                validate(item)
                if (type(item.get('id')) is not int or item['id'] < 1
                        or item['id'] in ids or item.get('status') not in ('guardado', 'devolvido')):
                    raise ValueError('Arquivo de dados contém identificador ou situação inválida.')
                ids.add(item['id'])
        else:
            self.items = seed()
            self.save(self.items)

    def save(self, items):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.path.with_suffix('.tmp')
        temporary.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding='utf-8')
        os.replace(temporary, self.path)
        self.items = items
