#! /usr/bin/python3

import sys
import argparse
import signal
import json

import tools


class Vertex:
    def __init__(self, vid):
        self.vid = vid
        self.parent = None
        self.in_edge = None
        self.children = []


    def as_dict(self):
        return dict(
            vid = self.vid,
            parent = self.parent,
            in_edge = self.in_edge,
            children = [c.as_dict() for c in self.children],
        )


class Trie:
    def __init__(self):
        self.root = Vertex(vid=1)
        self.size = 1


    def __str__(self):
        return json.dumps(dict(Trie=self.root.as_dict()), indent=4)


    def add(self, string):
        def find(parent, edge):
            for c in parent.children:
                if c.in_edge == edge:
                    return c
            return None

        def add_node(parent, edge):
            child = Vertex(vid=self.size+1)
            child.parent = parent.vid
            child.in_edge = edge
            parent.children.append(child)
            self.size += 1
            return child

        node = self.root
        for ch in string:
            next_node = find(node, ch)
            if next_node is None:
                next_node = add_node(node, ch)
            node = next_node


    def traverse(self, visitor, root=None):
        root = root or self.root
        for c in root.children:
            visitor(root, c)
            self.traverse(visitor, root=c)


def main(args):
    strings = map(str.strip, sys.stdin)

    trie = Trie()
    for string in strings:
        trie.add(string)

    def print_edge(parent, child):
        print(parent.vid, child.vid, child.in_edge)
    trie.traverse(print_edge)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='description',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    args = parser.parse_args()

    try:
        main(args)
    except BrokenPipeError:
        sys.exit(128 + signal.SIGPIPE)
    except KeyboardInterrupt:
        sys.exit(128 + signal.SIGINT)
