#! /usr/bin/python3

import sys
import argparse
import signal
import functools
import collections


def main(args):
    s = sys.stdin.read()

    def count(acc, ch):
        acc[ch] += 1
        return acc
    counters = functools.reduce(count, s, collections.defaultdict(int))

    print(counters['A'], counters['C'], counters['G'], counters['T'])


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
