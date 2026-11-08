"""Exportação dos resultados, compatível com planilhas e acentos em UTF-8."""
import csv
import io


def export_csv(items):
    output = io.StringIO(newline='')
    writer = csv.writer(output, delimiter=';')
    writer.writerow(['ID', 'Nome', 'Descrição', 'Local', 'Prazo', 'Situação'])
    for item in items:
        values = [item[key] for key in ('id', 'name', 'description', 'location', 'deadline', 'status')]
        # Impede que nomes e descrições sejam interpretados como fórmulas.
        writer.writerow(["'" + value if isinstance(value, str) and (value.lstrip().startswith(('=', '+', '-', '@')) or value.startswith(('\t', '\r', '\n')))
                         else value for value in values])
    return ('\ufeff' + output.getvalue()).encode('utf-8')
