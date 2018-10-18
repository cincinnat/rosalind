#! /usr/bin/python3

import sys
import argparse
import signal

import tools


def main(args):
    s, t = list(map(str.strip, sys.stdin))

    _, m = tools.dist.edit_matrix(s, t, substitution_weight=float('inf'))

    superseq = []
    for a, b in zip(*m):
        superseq.append(*({a, b} - {'-'}))
    print(''.join(superseq))


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
