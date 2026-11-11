import {request, notice, element} from './api.js';
import {drawTree} from './tree.js';
import './lab.js';

let selectedLocation = 'Campus', version = 0, locationReady = false, editingId = null;
const dialog = document.querySelector('#item-dialog');
const form = document.querySelector('#item-form');
const dateLabel = value => value.split('-').reverse().join('/');

function locations(tree) {
  const list = element('ul', undefined, 'locations-list');
  for (const [label, children] of Object.entries(tree)) {
    const li = element('li'), button = element('button', label);
    button.dataset.location = label;
    button.classList.toggle('selected', label === selectedLocation);
    button.addEventListener('click', () => {
      selectedLocation = label;
      document.querySelectorAll('[data-location]').forEach(b => b.classList.toggle('selected', b.dataset.location === label));
      load();
    });
    const option = element('option', label); option.value = label;
    document.querySelector('#form-location').append(option);
    li.append(button);
    if (Object.keys(children).length) li.append(locations(children));
    list.append(li);
  }
  return list;
}

function card(item) {
  const article = element('article', undefined, 'item');
  const top = element('div', undefined, 'item-top');
  top.append(element('span', '↳', 'item-icon'));
  const today = new Date();
  const localDate = `${today.getFullYear()}-${String(today.getMonth()+1).padStart(2,'0')}-${String(today.getDate()).padStart(2,'0')}`;
  const late = item.deadline < localDate && item.status === 'guardado';
  top.append(element('span', item.status === 'devolvido' ? 'Devolvido' : late ? 'Prazo vencido' : 'Guardado', `pill ${late ? 'late' : item.status === 'devolvido' ? 'returned' : ''}`));
  article.append(top, element('h3', item.name), element('p', item.description),
    element('p', `⌖ ${item.location}`), element('p', `Retirada até ${dateLabel(item.deadline)} · #${item.id}`));
  const actions = element('div', undefined, 'item-actions');
  const edit = element('button', 'Editar');
  edit.addEventListener('click', () => openForm(item)); actions.append(edit);
  if (item.status === 'guardado') {
    const returned = element('button', '✓ Registrar devolução');
    returned.addEventListener('click', () => mutate(item, 'return', returned)); actions.append(returned);
  }
  const remove = element('button', 'Excluir', 'delete');
  remove.addEventListener('click', () => mutate(item, 'delete', remove)); actions.append(remove);
  article.append(actions); return article;
}

async function mutate(item, action, button) {
  if (!confirm(`${action === 'delete' ? 'Excluir' : 'Registrar a devolução de'} “${item.name}”?`)) return;
  button.disabled = true;
  try {
    await request(`/api/items/${item.id}/${action}`, {});
    await load(); notice(action === 'delete' ? 'Objeto excluído.' : 'Devolução registrada.');
  } catch (error) { notice(error.message, true); }
  finally { button.disabled = false; }
}

async function load() {
  const requestVersion = ++version;
  const params = new URLSearchParams({prefix: document.querySelector('#search').value,
    location: selectedLocation, until: document.querySelector('#until').value || '9999-12-31',
    status: document.querySelector('#status').value});
  document.querySelector('#result-count').textContent = 'Buscando objetos…';
  try {
    const data = await request(`/api/items?${params}`);
    if (requestVersion !== version) return;
    document.querySelector('#export-csv').href = `/api/export?${params}`;
    if (!locationReady) {
      document.querySelector('#locations').append(locations(data.locations)); locationReady = true;
    }
    const target = document.querySelector('#items');
    target.replaceChildren(...data.items.map(card));
    if (!data.items.length) target.append(element('div', 'Nenhum objeto encontrado. Ajuste os filtros ou registre um objeto.', 'empty'));
    document.querySelector('#result-count').textContent = `${data.items.length} objeto(s) · ${selectedLocation} · por prazo de retirada`;
    const metrics = [['Resultados do filtro', data.items.length], ['Altura da AVL', data.metrics.height],
      ['Nós visitados · AVL', data.metrics.avlVisited], ['Nós visitados · Trie', data.metrics.trieVisited]];
    document.querySelector('#stats').replaceChildren(...metrics.map(([label, value]) => {
      const stat = element('div', undefined, 'stat'); stat.append(element('strong', value), element('span', label)); return stat;
    }));
    drawTree(document.querySelector('#live-tree'), data.tree);
  } catch (error) {
    if (requestVersion === version) { notice(error.message, true); document.querySelector('#result-count').textContent = 'Busca indisponível. Tente novamente.'; }
  }
}

document.querySelectorAll('[data-panel]').forEach(button => button.addEventListener('click', () => {
  document.querySelectorAll('[data-panel]').forEach(b => {
    b.classList.toggle('active', b === button); b.setAttribute('aria-selected', String(b === button));
    document.querySelector(`#${b.dataset.panel}`).hidden = b !== button;
  });
}));
let debounce;
document.querySelector('#filters').addEventListener('submit', e => e.preventDefault());
document.querySelector('#filters').addEventListener('input', () => { clearTimeout(debounce); debounce = setTimeout(load, 180); });
document.querySelector('#filters').addEventListener('reset', () => {
  selectedLocation = 'Campus';
  document.querySelectorAll('[data-location]').forEach(b => b.classList.toggle('selected', b.dataset.location === 'Campus'));
  setTimeout(load, 0);
});
function openForm(item = null) {
  form.reset(); editingId = item?.id ?? null;
  document.querySelector('#dialog-title').textContent = item ? 'Editar objeto' : 'Registrar objeto';
  if (item) {
    for (const field of ['name', 'description', 'location', 'deadline']) {
      document.querySelector(`#item-form [name="${field}"]`).value = item[field];
    }
  }
  document.querySelector('#form-error').textContent = ''; dialog.showModal();
}
document.querySelector('#new-item').addEventListener('click', () => openForm());
document.querySelector('#close-dialog').addEventListener('click', () => dialog.close());
form.addEventListener('submit', async event => {
  event.preventDefault();
  const save = document.querySelector('#save-item'); save.disabled = true;
  try {
    const editing = editingId !== null;
    await request(editing ? `/api/items/${editingId}/edit` : '/api/items', Object.fromEntries(new FormData(form)));
    dialog.close(); await load(); notice(`Objeto ${editing ? 'atualizado' : 'registrado'}. Ajuste os filtros caso ele não apareça na lista.`);
  } catch (error) { document.querySelector('#form-error').textContent = error.message; }
  finally { save.disabled = false; }
});
load();
