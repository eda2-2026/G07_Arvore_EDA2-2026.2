import json
import tempfile
import threading
import unittest
from contextlib import redirect_stdout
import io
from unittest.mock import patch
from app import server as server_module
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import HTTPError
from app.server import make_server
from test_service import PAYLOAD


class HTTPTests(unittest.TestCase):
    def test_demo_mode_cleans_temporary_data_and_preserves_normal_base(self):
        original = server_module.ROOT / 'data' / 'objetos.json'
        before = original.read_bytes() if original.exists() else None
        created = []
        real_make = server_module.make_server
        def capture(port, data_path):
            created.append(Path(data_path))
            result = real_make(port, data_path)
            self.assertEqual(len(json.loads(Path(data_path).read_text(encoding='utf-8'))), 9)
            return result
        with patch('sys.argv', ['iniciar.py', '--demo', '--port', '0']), redirect_stdout(io.StringIO()), \
                patch.object(server_module, 'make_server', side_effect=capture), \
                patch.object(server_module.ThreadingHTTPServer, 'serve_forever', side_effect=KeyboardInterrupt):
            server_module.main()
        self.assertEqual(len(created), 1)
        self.assertFalse(created[0].parent.exists())
        self.assertEqual(original.read_bytes() if original.exists() else None, before)

    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.server = make_server(0, Path(cls.temp.name) / 'items.json')
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.url = f'http://127.0.0.1:{cls.server.server_port}'

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown(); cls.server.server_close(); cls.thread.join(); cls.temp.cleanup()

    def call(self, path, data=None, raw=None):
        body = raw if raw is not None else json.dumps(data).encode() if data is not None else None
        request = Request(self.url + path, data=body, headers={'Content-Type': 'application/json'})
        try:
            response = urlopen(request, timeout=5)
        except HTTPError as error:
            response = error
        with response:
            return response.status, response.read(), response.headers

    def test_assets(self):
        for path in ('/', '/styles.css', '/app.js', '/api.js', '/tree.js', '/lab.js', '/favicon.svg'):
            with self.subTest(path=path):
                status, body, headers = self.call(path)
                self.assertEqual(status, 200)
                self.assertTrue(body)
                self.assertEqual(int(headers['Content-Length']), len(body))

    def test_api_roundtrip(self):
        status, body, _ = self.call('/api/items', PAYLOAD)
        self.assertEqual(status, 201)
        ident = json.loads(body)['id']
        self.assertEqual(self.call(f'/api/items/{ident}/return', {})[0], 200)
        self.assertEqual(self.call(f'/api/items/{ident}/delete', {})[0], 200)
        self.assertEqual(self.call(f'/api/items/{ident}/delete', {})[0], 404)

    def test_validation_and_paths(self):
        for path, payload in [('/api/items', []), ('/api/items', {}), ('/api/lab', []),
                              ('/api/lab', {'values': [True]}), ('/api/lab', {'values': list(range(32))})]:
            self.assertEqual(self.call(path, payload)[0], 400)
        self.assertEqual(self.call('/api/items', raw=b'{')[0], 400)
        self.assertEqual(self.call('/api/items', raw=b'x'*17000)[0], 400)
        self.assertEqual(self.call('/api/items?status=invalid')[0], 400)
        self.assertEqual(self.call('/api/items?until=')[0], 400)
        self.assertEqual(self.call('/api/items?unknown=value')[0], 400)
        for path in ('/../app/server.py', '/%2e%2e/app/server.py', '/missing', '/api/nope'):
            self.assertEqual(self.call(path)[0], 404)
        self.assertEqual(self.call('/api/nope', {})[0], 404)

    def test_lab(self):
        status, body, _ = self.call('/api/lab', {'values': [3, 2, 1]})
        self.assertEqual(status, 200)
        self.assertEqual(json.loads(body)['ordered'], [1, 2, 3])

    def test_edit_and_export(self):
        _, body, _ = self.call('/api/items', dict(PAYLOAD, name='Exportação exclusiva'))
        ident = json.loads(body)['id']
        updated = dict(PAYLOAD, name='=Exportação; "teste"')
        status, body, _ = self.call(f'/api/items/{ident}/edit', updated)
        self.assertEqual(status, 200)
        self.assertEqual(json.loads(body)['name'], updated['name'])
        status, body, headers = self.call('/api/export?prefix=%3DExporta')
        self.assertEqual(status, 200)
        self.assertTrue(body.startswith(b'\xef\xbb\xbf'))
        self.assertIn('attachment', headers['Content-Disposition'])
        self.assertIn("'=Exporta", body.decode('utf-8-sig'))
        self.assertEqual(self.call('/api/export?status=x')[0], 400)
        self.assertEqual(self.call(f'/api/items/{ident}/edit', {})[0], 400)
        self.assertEqual(self.call('/api/items/999999/edit', PAYLOAD)[0], 404)
        self.call(f'/api/items/{ident}/delete', {})

    def test_javascript_mime_and_invalid_paths(self):
        self.assertIn('javascript', self.call('/app.js')[2]['Content-Type'])
        self.assertEqual(self.call('/%00')[0], 404)
        self.assertEqual(self.call('/api/items/invalid/edit', PAYLOAD)[0], 400)
