#! /usr/bin/python3

import sys
import argparse
import signal
import collections
import decimal

import tools


def main(args):
    s1 = list(map(decimal.Decimal, sys.stdin.readline().split()))
    s2 = list(map(decimal.Decimal, sys.stdin.readline().split()))

    s1 = collections.Counter(s1)
    s2 = collections.Counter(s2)
    diff = tools.spectrometry.minkowski_diff(s1, s2)

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
