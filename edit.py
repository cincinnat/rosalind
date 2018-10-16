#! /usr/bin/python3

import sys
import argparse
import signal
import collections
import itertools

import tools


def edit_dist(s1, s2):
    Cell = collections.namedtuple('Arrow', ['arrow', 'dist'])

    def weight(u, v):
        if u[0] != v[0] and u[1] != v[1]:
            return s1[u[0]] != s2[u[1]]  # 1 if substitution
        return 1  # indel

    dist = dict()
    for v in itertools.product(range(len(s1)+1), range(len(s2)+1)):
        i, j = v
        if i == 0 and j == 0:
            dist[v] = Cell(v, 0)
        elif i == 0:
            u = (i, j-1)
            dist[v] = Cell(u, weight(u, v) + dist[u].dist)
        elif j == 0:
            u = (i-1, j)
            dist[v] = Cell(u, weight(u, v) + dist[u].dist)
        else:
            parents = [(i-1, j), (i, j-1), (i-1, j-1)]
            weights = [weight(u, v) + dist[u].dist for u in parents]
            w = min(weights)
            u = parents[weights.index(w)]
            dist[v] = Cell(u, w)

    return dist[v].dist


def main(args):
    inputs = tools.io.read_fasta(sys.stdin)
    s1, s2 = [''.join(seq) for _, seq in inputs]

    print(edit_dist(s1, s2))


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
