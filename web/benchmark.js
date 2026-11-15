import {request, element} from './api.js';

document.querySelector('#benchmark-form').addEventListener('submit', async event => {
  event.preventDefault();
  const button = document.querySelector('#benchmark-run');
  const status = document.querySelector('#benchmark-status');
  button.disabled = true; status.textContent = 'Construindo e consultando as três estruturas…';
  try {
    const data = await request('/api/benchmark', {size: Number(document.querySelector('#benchmark-size').value),
      scenario: document.querySelector('#benchmark-scenario').value});
    document.querySelector('#benchmark-results').replaceChildren(...data.rows.map(row => {
      const tr = element('tr');
      for (const value of [row.name, row.height ?? '—', row.rotations, row.buildComparisons,
        row.buildMs, row.searchMs, row.averageVisits]) tr.append(element('td', String(value)));
      return tr;
    }));
    const maximum = Math.max(...data.rows.map(row => row.averageVisits));
    document.querySelector('#benchmark-bars').replaceChildren(...data.rows.map(row => {
      const line = element('div', undefined, 'benchmark-bar');
      const bar = element('span', `${row.name} · ${row.averageVisits} visitas/busca`);
      bar.style.width = `${Math.max(12, row.averageVisits / maximum * 100)}%`;
      line.append(bar); return line;
    }));
    status.textContent = `${data.size} elementos · ${data.queries} consultas · resultados idênticos verificados · semente ${data.seed}. Gráfico: média de valores examinados por busca (menor é melhor).`;
  } catch (error) { status.textContent = error.message; }
  finally { button.disabled = false; }
});
