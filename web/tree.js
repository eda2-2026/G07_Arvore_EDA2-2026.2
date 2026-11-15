import {element} from './api.js';

export function drawTree(container, root, lab = false, {path = [], target = null} = {}) {
  container.replaceChildren();
  if (!root) { container.append(element('p', 'Árvore vazia.', 'muted')); return; }
  const tree = element('div', undefined, 'tree');
  function branch(node) {
    const li = element('li');
    const label = element('span', lab ? String(node.key[0]) : `${node.key[0]} · #${node.key[1]}`, 'node');
    label.classList.toggle('search-path', path.includes(node.key[0]));
    label.classList.toggle('search-target', path.includes(node.key[0]) && node.key[0] === target);
    label.append(element('small', `h=${node.height} · BF=${node.balance}`));
    label.append(element('small', `n=${node.size ?? 1}${node.truncated ? ' · expandir níveis ↓' : ''}`));
    li.append(label);
    if (node.left || node.right) {
      const children = element('ul');
      for (const child of [node.left, node.right]) {
        const item = child ? branch(child) : element('li', '∅');
        children.append(item);
      }
      li.append(children);
    }
    return li;
  }
  const ul = element('ul'); ul.append(branch(root)); tree.append(ul); container.append(tree);
}
