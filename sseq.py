#! /usr/bin/python3

import sys
import argparse
import signal
import numpy as np

import tools


def main(args):
    inputs = tools.io.read_fasta(sys.stdin)
    s = ''.join(next(inputs)[1])
    t = ''.join(next(inputs)[1])

    indices = []
    for ch in t:
        start = indices[-1] if indices else 0
        i = s.find(ch, start)
        assert i >= start
        indices.append(i+1)

    print(*indices)


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
