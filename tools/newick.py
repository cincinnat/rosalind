import json
import lark
import collections


class Node:
    def __init__(self):
        self.label = None
        self.neighbours = set()
        self.weights = dict()

    def as_dict(self, parent=None):
        children = [node for node in self.neighbours if node is not parent]
        return dict(
            self = id(self),
            label = self.label,
            parent = id(parent) if parent else None,
            in_weight = parent.weights.get(self, None) if parent else None,
            children = [c.as_dict(self) for c in children],
        )

    def __str__(self):
        return json.dumps(self.as_dict(), indent=4)


def _convert(term, parent=None):
    if term.data in ['internal', 'leaf']:
        node = Node()
        if parent:
            parent.neighbours.add(node)
            node.neighbours.add(parent)

        for ch in term.children:
            _convert(ch, node)
        return node

    elif term.data == 'branch':
        assert parent is not None

        w = None
        for ch in term.children:
            if ch.data == 'weight':
                w = float(ch.children[0].value)
            else:
                child = _convert(ch, parent)

        if w is not None:
            parent.weights[child] = w
            child.weights[parent] = w
            

    elif term.data == 'name':
        parent.label = term.children[0].value

    else:
        assert False, 'unexpected term: %' % term.data


def parse(string):
    grammar = '''
        ?tree:     subtree ";"
        ?subtree:  leaf | internal
        leaf:      [name]
        internal:  "(" [branch ("," branch)*] ")" [name]
        branch:    subtree [weight]
        weight:    ":" SIGNED_NUMBER
        name:      CNAME

        %import common.CNAME
        %import common.SIGNED_NUMBER
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
