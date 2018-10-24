#! /usr/bin/python3

import sys
import argparse
import signal
import itertools
import collections
import numpy as np

import tools


def gen_sequences(t, u):
    if not t and not u:
        yield ''
    else:
        if t:
            for suffix in gen_sequences(t[1:], u):
                yield t[0] + suffix
        if u:
            for suffix in gen_sequences(t, u[1:]):
                yield u[0] + suffix


def can_interwoven(tree, t, u):
    for seq in gen_sequences(t, u):
        if tree.find(seq):
            return True
    return False


def main(args):
    inputs = map(str.strip, sys.stdin)
    dna = next(inputs)
    strings = list(inputs)
    n = len(strings)

    tree = tools.suffix_tree.SuffixTree()
    tree.add(dna)

    m = np.zeros((n, n), dtype=int)
    for i, j in itertools.combinations_with_replacement(range(n), 2):
        m[i, j] = can_interwoven(tree, strings[i], strings[j])
        m[j, i] = m[i, j]

    for row in range(n):
        print(*m[row, :])



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
