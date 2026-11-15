import unittest
from app.normalization import normalize
from app.validation import validate
from test_service import PAYLOAD


class ValidationTests(unittest.TestCase):
    def test_normalization(self):
        self.assertEqual(normalize('  ÓCULOS Ç  '), 'oculos c')

    def test_clean_fields(self):
        self.assertEqual(validate(dict(PAYLOAD, name='  Caneta  ', extra='ignorado')),
                         dict(PAYLOAD, name='Caneta', category='Outros'))

    def test_deadline_type(self):
        for value in (None, 20261115, '', '15/11/2026'):
            with self.subTest(value=value), self.assertRaises(ValueError):
                validate(dict(PAYLOAD, deadline=value))
