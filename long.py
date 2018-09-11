#! /usr/bin/python3

import sys
import argparse
import signal
import itertools
import collections

import tools


def overlap(a, b):
    l = 0
    for i in range(len(a)):
        suffix = a[-i-1:]
        if b.startswith(suffix):
            l = i+1
    return l


def main(args):
    reads = tools.io.read_fasta(sys.stdin)
    reads = [''.join(seq) for _, seq in reads]


    left_neighbours = dict()
    right_neighbours = dict()
    overlaps = dict()
    def compute_overlap(i, j):
        l = overlap(reads[i], reads[j])
        if l >= min(len(reads[i]), len(reads[j])) // 2 + 1:
            overlaps[i] = l
            left_neighbours[j] = i
            right_neighbours[i] = j

    for i, j in itertools.combinations(range(len(reads)), 2):
        compute_overlap(i, j)
        compute_overlap(j, i)


    def missing_key(d):
        for i in range(len(d)+1):
            if i not in d:
                return i
        assert False

    superstring = []
    i = missing_key(left_neighbours)
    superstring.append(reads[i])
    while True:
        if i not in right_neighbours:
            break
        l = overlaps[i]
        i = right_neighbours[i]
        superstring.append(reads[i][l:])

    superstring = ''.join(superstring)
    print(superstring)


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
