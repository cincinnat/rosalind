#! /usr/bin/python3

import sys
import argparse
import signal
import itertools
import math

import tools


def main(args):
    l = int(sys.stdin.read())

    print(math.factorial(l))
    for perm in itertools.permutations(range(1, l+1)):
        print(*perm)


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
