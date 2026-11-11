import {request, notice} from './api.js';
import {drawTree} from './tree.js';

let result = null, index = 0, version = 0;
function render() {
  const step = result.steps[index];
  drawTree(document.querySelector('#lab-tree'), step?.tree, true);
  document.querySelector('#step-label').textContent = step
    ? `Passo ${index + 1}/${result.steps.length} · inserir ${step.value} · ${step.rotations} rotação(ões)` : 'Árvore vazia';
  document.querySelector('#prev').disabled = index === 0;
  document.querySelector('#next').disabled = index >= result.steps.length - 1;
  document.querySelector('#lab-summary').textContent = `Resultado final — Em ordem: ${result.ordered.join(' → ')}. Altura: ${result.height}. Rotações: ${result.rotations}. Duplicatas são ignoradas.`;
}
async function run(event) {
  event?.preventDefault();
  const requestVersion = ++version;
  const raw = document.querySelector('#sequence').value.trim();
  const tokens = raw.split(',').map(x => x.trim());
  if (!raw || tokens.some(x => !/^-?\d+$/.test(x))) {
    notice('Separe os números inteiros por vírgulas.', true); return;
  }
  try {
    const response = await request('/api/lab', {values: tokens.map(Number)});
    if (requestVersion !== version) return;
    result = response;
    index = 0; render(); notice('Use Anterior e Próximo para acompanhar as inserções.');
  } catch (error) { if (requestVersion === version) notice(error.message, true); }
}
document.querySelector('#lab-form').addEventListener('submit', run);
document.querySelectorAll('[data-values]').forEach(button => button.addEventListener('click', () => {
  document.querySelector('#sequence').value = button.dataset.values; run();
}));
document.querySelector('#prev').addEventListener('click', () => { if (result && index > 0) { index--; render(); } });
document.querySelector('#next').addEventListener('click', () => { if (result && index < result.steps.length - 1) { index++; render(); } });
document.querySelector('#prev').disabled = true;
document.querySelector('#next').disabled = true;
