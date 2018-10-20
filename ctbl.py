#! /usr/bin/python3

import sys
import argparse
import signal
import itertools

import tools


def get_labels(tree):
    labels = set()
    def visitor(v, _):
        if not v.label.startswith('<empty'):
            labels.add(v.label)
    tools.newick.bfs(tree, visitor)

    return labels


def get_edges(tree):
    edges = []
    def visitor(v, path):
        if path[v] is not None:
            edges.append((v, path[v]))
    tools.newick.bfs(tree, visitor)

    return edges


def split(u, v):
    u.neighbours.remove(v)
    v.neighbours.remove(u)

    u_split = get_labels(u)
    v_split = get_labels(v)

    v.neighbours.add(u)
    u.neighbours.add(v)

    return u_split, v_split


def encode_taxa(labels, split_a, split_b):
    taxa = [int(label in split_a) for label in labels]
    return ''.join(map(str, taxa))


def main(args):
    tree = sys.stdin.readline().strip()
    tree = tools.newick.parse(tree)

    labels = sorted(get_labels(tree))
    edges = get_edges(tree)

    for u, v in edges:
        if len(u.neighbours) < 2 or len(v.neighbours) < 2:
            # a trivial character
            continue

        u_split, v_split = split(u, v)
        print(encode_taxa(labels, u_split, v_split))


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
