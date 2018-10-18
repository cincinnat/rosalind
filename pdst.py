#! /usr/bin/python3

import sys
import argparse
import signal
import numpy as np

import tools


def main(args):
    inputs = tools.io.read_fasta(sys.stdin)
    strings = [''.join(seq) for _, seq in inputs]

    def foo(i, j):
        dist = tools.dist.hamming_distance(strings[i], strings[j])
        return dist / len(strings[i])

    dist = np.fromfunction(np.vectorize(foo), (len(strings), len(strings)), dtype=int)
    for i in range(len(strings)):
        print(*dist[i, :])


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
