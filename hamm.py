#! /usr/bin/python3

import sys
import argparse
import signal
import functools
import collections

import tools


def main(args):
    s1 = sys.stdin.readline().strip()
    s2 = sys.stdin.readline().strip()

    print(tools.helpers.hamming_distance(s1, s2))


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
