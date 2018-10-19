#! /usr/bin/python3

import sys
import argparse
import signal
import itertools
import math

import tools


def main(args):
    inputs = filter(bool, map(str.split, sys.stdin))
    inputs = map(lambda l: list(map(int, l)), inputs)
    pairs = tools.helpers.iter_chunks(inputs, chunk_size=2)
    distances = itertools.starmap(tools.dist.reversal_distance, pairs)

    print(*distances)


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
