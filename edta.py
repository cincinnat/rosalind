#! /usr/bin/python3

import sys
import argparse
import signal
import collections
import itertools

import tools


def main(args):
    inputs = tools.io.read_fasta(sys.stdin)
    s, t = [''.join(seq) for _, seq in inputs]

    dist, matrix = tools.dist.edit_matrix(s, t)
    print(dist)
    print(matrix[0])
    print(matrix[1])


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
