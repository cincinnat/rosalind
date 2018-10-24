#! /usr/bin/python3

import sys
import argparse
import signal

import tools


def n_leaves(tree, v):
    n = 0
    for c in tree.traverse(v):
        n += not c.children
    return n


def main(args):
    s = sys.stdin.readline().strip()
    k = int(sys.stdin.readline().strip())
    # ignore the rest

    s = s[:-1]  # cut trailing '$'

    tree = tools.suffix_tree.SuffixTree()
    tree.add(s)

    l = ''
    for v in tree.traverse():
        if n_leaves(tree, v) >= k:
            path = tree.path(v)
            if len(l) < len(path):
                l = path
    print(l)



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
