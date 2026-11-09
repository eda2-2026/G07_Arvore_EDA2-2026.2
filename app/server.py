import argparse
import json
import mimetypes
from contextlib import ExitStack
from tempfile import TemporaryDirectory
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit, parse_qs, unquote
from app.storage import Storage
from app.service import Service
from app.lab import experiment
from app.export import export_csv

ROOT = Path(__file__).resolve().parent.parent


def make_server(port=8000, data_path=None):
    service = Service(Storage(data_path or ROOT / 'data' / 'objetos.json'))

    class Handler(BaseHTTPRequestHandler):
        def send_bytes(self, code, data, content_type, attachment=None):
            self.send_response(code)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', str(len(data)))
            self.send_header('Cache-Control', 'no-store')
            self.send_header('X-Content-Type-Options', 'nosniff')
            if attachment:
                self.send_header('Content-Disposition', f'attachment; filename="{attachment}"')
            self.end_headers()
            self.wfile.write(data)

        def reply(self, code, payload):
            data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
            self.send_bytes(code, data, 'application/json; charset=utf-8')

        def body(self):
            size = int(self.headers.get('Content-Length', '0'))
            if not 0 < size <= 16384:
                raise ValueError('Corpo JSON ausente ou maior que 16 KB.')
            try:
                return json.loads(self.rfile.read(size))
            except (UnicodeError, json.JSONDecodeError):
                raise ValueError('JSON inválido.') from None

        def do_GET(self):
            parsed = urlsplit(self.path)
            if parsed.path in ('/api/items', '/api/export'):
                params = parse_qs(parsed.query, keep_blank_values=True)
                try:
                    result = service.listing(**{k: v[-1] for k, v in params.items()})
                    if parsed.path == '/api/export':
                        self.send_bytes(200, export_csv(result['items']), 'text/csv; charset=utf-8', 'reencontra.csv')
                    else:
                        self.reply(200, result)
                except (ValueError, TypeError) as exc:
                    self.reply(400, dict(error=str(exc)))
                return
            try:
                path = (ROOT / 'web' / (unquote(parsed.path).lstrip('/') or 'index.html')).resolve()
            except (ValueError, OSError):
                self.reply(404, dict(error='Página não encontrada.'))
                return
            if not path.is_relative_to(ROOT / 'web') or not path.is_file():
                self.reply(404, dict(error='Página não encontrada.'))
                return
            data = path.read_bytes()
            content_type = 'text/javascript' if path.suffix == '.js' else mimetypes.guess_type(path)[0] or 'application/octet-stream'
            self.send_bytes(200, data, content_type + '; charset=utf-8')

        def do_POST(self):
            try:
                path = urlsplit(self.path).path
                if path == '/api/items':
                    self.reply(201, service.create(self.body()))
                elif path == '/api/lab':
                    payload = self.body()
                    if not isinstance(payload, dict):
                        raise ValueError('Envie um objeto JSON.')
                    self.reply(200, experiment(payload.get('values')))
                else:
                    parts = path.strip('/').split('/')
                    if len(parts) != 4 or parts[:2] != ['api', 'items'] or parts[3] not in ('return', 'delete', 'edit'):
                        self.reply(404, dict(error='Operação não encontrada.'))
                        return
                    if parts[3] == 'edit':
                        self.reply(200, service.edit(int(parts[2]), self.body()))
                    else:
                        self.reply(200, service.change(int(parts[2]), parts[3]))
            except KeyError:
                self.reply(404, dict(error='Objeto não encontrado.'))
            except (ValueError, TypeError) as exc:
                self.reply(400, dict(error=str(exc)))
            except OSError:
                self.reply(500, dict(error='Não foi possível gravar os dados.'))

    server = ThreadingHTTPServer(('127.0.0.1', port), Handler)
    server.daemon_threads = True
    return server


def main():
    parser = argparse.ArgumentParser(description='Reencontra — achados e perdidos')
    parser.add_argument('--port', type=int, default=8000)
    parser.add_argument('--demo', action='store_true', help='Usa dados temporários novos sem alterar a base salva.')
    args = parser.parse_args()
    with ExitStack() as stack:
        data_path = None
        if args.demo:
            directory = stack.enter_context(TemporaryDirectory(prefix='reencontra-demo-'))
            data_path = Path(directory) / 'objetos.json'
        try:
            server = make_server(args.port, data_path)
        except (OSError, ValueError) as exc:
            parser.exit(1, f'Não foi possível iniciar: {exc}\n')
        print(f'Reencontra: http://localhost:{server.server_port} — Ctrl+C para encerrar', flush=True)
        if args.demo:
            print('Modo apresentação: dados temporários; sua base salva permanece intacta.', flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            server.server_close()
