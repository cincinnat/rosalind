#! /usr/bin/python3

import sys
import argparse
import signal
import collections
import itertools

import tools


def minkowski_diff(s1, s2):
    def diff(s1, s2):
        for a, b in itertools.product(s1.elements(), s2.elements()):
            yield round(a - b, 5)

    return collections.Counter(diff(s1, s2))


def main(args):
    s1 = list(map(float, sys.stdin.readline().split()))
    s2 = list(map(float, sys.stdin.readline().split()))

    s1 = collections.Counter(s1)
    s2 = collections.Counter(s2)
    diff = minkowski_diff(s1, s2)

    x, cnt = diff.most_common(1)[0]
    print(cnt)
    print(x)


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
