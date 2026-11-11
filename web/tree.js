import {element} from './api.js';

export function drawTree(container, root, lab = false) {
  container.replaceChildren();
  if (!root) { container.append(element('p', 'Árvore vazia.', 'muted')); return; }
  const tree = element('div', undefined, 'tree');
  function branch(node) {
    const li = element('li');
    const label = element('span', lab ? String(node.key[0]) : `${node.key[0]} · #${node.key[1]}`, 'node');
    label.append(element('small', `h=${node.height} · BF=${node.balance}`));
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
