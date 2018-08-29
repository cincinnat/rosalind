#! /usr/bin/python3

import sys
import argparse
import signal
import functools
import collections


def main(args):
    string = sys.stdin.readline().strip()
    pattern = sys.stdin.readline().strip()

    # NOTE: obviously, not the fastest algorithm
    # a suffix array (or a suffix tree, or something) would be faster for
    # real data
    #
    locations = []
    for i in range(len(string) - len(pattern)):
        if string[i:].startswith(pattern):
            locations.append(i+1)

    print(*locations)


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
