#! /usr/bin/python3

import sys
import argparse
import signal
import lark
import json
import collections

import tools

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


def find_dist(root, u, v):
    u = bfs(root, lambda n, _: n.label == u)
    assert u is not None

    path = None
    def visitor(node, current_path):
        nonlocal path
        if node.label == v:
            path = current_path
            return True

    v = bfs(u, visitor)
    assert v is not None

    def path_len(path, start):
        dist = 0
        while path[start] is not None:
            dist += 1
            start = path[start]
        return dist

    return path_len(path, v)


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


def parse_newick(string):
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


def main(args):
    inputs = map(str.strip, args.input)
    inputs = filter(bool, inputs)  # remove blanks
    inputs = tools.helpers.iter_chunks(inputs, 2)

    distances = []
    for string, pair in inputs:
        tree = parse_newick(string)
        pair = pair.split()
        distances.append(find_dist(tree, *pair))

    print(*distances)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='description',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('input', nargs='?', type=argparse.FileType('r'),
        default=sys.stdin)

    args = parser.parse_args()

    try:
        main(args)
    except BrokenPipeError:
        sys.exit(128 + signal.SIGPIPE)
    except KeyboardInterrupt:
        sys.exit(128 + signal.SIGINT)
