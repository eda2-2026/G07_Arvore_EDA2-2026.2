from app.normalization import normalize


class Trie:
    def __init__(self):
        self.root = {'children': {}, 'ids': set()}

    def insert(self, text, item_id):
        node = self.root
        for letter in normalize(text):
            node = node['children'].setdefault(letter, {'children': {}, 'ids': set()})
        node['ids'].add(item_id)

    def prefix(self, text):
        node, visited = self.root, 0
        for letter in normalize(text):
            visited += 1
            if letter not in node['children']:
                return set(), visited
            node = node['children'][letter]
        result, stack = set(), [node]
        while stack:
            current = stack.pop()
            visited += 1
            result.update(current['ids'])
            stack.extend(current['children'].values())
        return result, visited

    def remove(self, text, item_id):
        """Remove uma referência e poda somente os ramos que ficaram vazios."""
        node, path = self.root, []
        for letter in normalize(text):
            child = node['children'].get(letter)
            if child is None:
                return
            path.append((node, letter))
            node = child
        node['ids'].discard(item_id)
        for parent, letter in reversed(path):
            child = parent['children'][letter]
            if child['ids'] or child['children']:
                break
            del parent['children'][letter]
