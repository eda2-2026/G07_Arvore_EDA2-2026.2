import csv
import io
import unittest
from app.export import export_csv


class ExportTests(unittest.TestCase):
    def test_csv_escaping_accents_and_formula_neutralization(self):
        items = [dict(id=i, name=name, description='Acentuação; "aspas"\ne linha',
                      location='Laboratório', deadline='2026-11-15', status='guardado')
                 for i, name in enumerate(['Óculos', '=1+1', '+SOMA(1)', '-2+2', '@teste', '  =1', '\ttexto'], 1)]
        rows = list(csv.reader(io.StringIO(export_csv(items).decode('utf-8-sig')), delimiter=';'))
        self.assertEqual(len(rows), 8)
        self.assertEqual(rows[1][1], 'Óculos')
        self.assertEqual(rows[1][2], items[0]['description'])
        for row in rows[2:]:
            self.assertTrue(row[1].startswith("'"))

    def test_empty_export_has_header(self):
        self.assertEqual(len(export_csv([]).decode('utf-8-sig').splitlines()), 1)
