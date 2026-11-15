import {request, notice, element} from './api.js';
import {drawTree} from './tree.js';
import './benchmark.js';

let result = null, index = 0, version = 0;
function render() {
  const step = result.steps[index];
  drawTree(document.querySelector('#lab-tree'), step?.tree, true, {path: step?.path || [], target: result.target});
  document.querySelector('#step-label').textContent = step
    ? `Passo ${index + 1}/${result.steps.length} · ${step.action} ${step.value} · ${step.rotations} rotação(ões)${step.changed ? '' : ' · sem alteração'}` : 'Árvore vazia';
  document.querySelector('#prev').disabled = index === 0;
  document.querySelector('#next').disabled = index >= result.steps.length - 1;
  document.querySelector('#lab-summary').textContent = `Resultado final — Em ordem: ${result.ordered.join(' → ')}. Altura: ${result.height}. Rotações: ${result.rotations}. Nós: ${result.count}. Folhas: ${result.leaves}. Mediana inferior: ${result.median ?? '—'}. Posição ${result.position}: ${result.selected ?? 'fora da árvore'}. ${result.target !== null ? `Menores que ${result.target}: ${result.rank}. Busca neste passo: ${step?.found ? 'encontrado' : 'não encontrado'}.` : ''} Duplicatas são ignoradas.`;
  document.querySelector('#traversals').replaceChildren(...[
    ['Pré-ordem · raiz / esquerda / direita', result.traversals.preorder],
    ['Pós-ordem · esquerda / direita / raiz', result.traversals.postorder],
    ['Em largura · BFS com fila', result.traversals.breadth]
  ].map(([label, values]) => {
    const block = element('div'); block.append(element('strong', label), element('p', values.join(' → ') || 'Árvore vazia')); return block;
  }));
}
async function run(event) {
  event?.preventDefault();
  const requestVersion = ++version;
  const raw = document.querySelector('#sequence').value.trim();
  const tokens = raw.split(',').map(x => x.trim());
  const removalRaw = document.querySelector('#removals').value.trim();
  const removalTokens = removalRaw ? removalRaw.split(',').map(x => x.trim()) : [];
  if (!raw || [...tokens, ...removalTokens].some(x => !/^-?\d+$/.test(x))) {
    notice('Separe os números inteiros por vírgulas.', true); return;
  }
  try {
    const search = document.querySelector('#tree-target').value.trim();
    const response = await request('/api/lab', {values: tokens.map(Number), removals: removalTokens.map(Number),
      target: search === '' ? null : Number(search), position: Number(document.querySelector('#tree-position').value || 1)});
    if (requestVersion !== version) return;
    result = response;
    index = 0; render(); notice('Use Anterior e Próximo para acompanhar inserções, remoções e o caminho de busca.');
  } catch (error) { if (requestVersion === version) notice(error.message, true); }
}
document.querySelector('#lab-form').addEventListener('submit', run);
document.querySelectorAll('[data-values]').forEach(button => button.addEventListener('click', () => {
  document.querySelector('#removals').value = '';
  document.querySelector('#sequence').value = button.dataset.values; run();
}));
document.querySelector('#removal-example').addEventListener('click', () => {
  document.querySelector('#sequence').value = '9,5,10,0,6,11,-1,1,2';
  document.querySelector('#removals').value = '10';
  document.querySelector('#tree-target').value = '6';
  run();
});
document.querySelector('#lab-zoom').addEventListener('input', event => {
  document.querySelector('#lab-tree').style.zoom = `${event.target.value}%`;
});
document.querySelector('#prev').addEventListener('click', () => { if (result && index > 0) { index--; render(); } });
document.querySelector('#next').addEventListener('click', () => { if (result && index < result.steps.length - 1) { index++; render(); } });
document.querySelector('#prev').disabled = true;
document.querySelector('#next').disabled = true;
