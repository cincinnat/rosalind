import json
import lark
import collections


class Node:
    def __init__(self):
        self.label = None
        self.neighbours = []

    def as_dict(self, parent=None):
        return dict(
            label = self.label,
            parent = parent.label if parent else None,
            children = [c.as_dict(self) for c in self.neighbours if c is not parent]
        )

    def __str__(self):
        return json.dumps(self.as_dict(), indent=4)


def _convert(tree, parent=None):
    def select(children, data):
        return [ch for ch in children if ch.data in data]

    def name(tree):
        name = select(tree.children, ['name'])
        if len(name) == 1:
            return name[0].children[0].value
        return '<empty #%s>' % id(tree)


    def link(u, v):
        u.neighbours.append(v)
        v.neighbours.append(u)

    node = Node()
    node.label = name(tree)

    if tree.data == 'internal':
        for ch in select(tree.children, ['leaf', 'internal']):
            link(node, _convert(ch, node))

    return node


def parse(string):
    grammar = '''
        ?tree:      subtree ";"
        ?subtree:   leaf | internal
        leaf:      [name]
        internal:  "(" [subtree ("," subtree)*] ")" [name]
        name:      CNAME

        %import common.CNAME
    '''

    parser = lark.Lark(grammar, start='tree')
    tree = parser.parse(string)
    return _convert(tree)


def bfs(root, visitor):
    open_set = collections.deque()
    closet_set = set()
    path = dict()

    open_set.append(root)
    path[root] = None

    while open_set:
        subtree_root = open_set.popleft()
        if subtree_root in closet_set:
            continue
        closet_set.add(subtree_root)

        if visitor(subtree_root, path):
            return subtree_root

        for child in subtree_root.neighbours:
            if child in closet_set:
                continue
            open_set.append(child)
            path[child] = subtree_root

    return None
