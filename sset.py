#! /usr/bin/python3

import sys
import argparse
import signal
import math

import tools


def num_subsets(n, mod):
    cnt = 1
    for i in range(n):
        cnt = (cnt * 2) % mod
    return cnt % mod


def main(args):
    n = int(sys.stdin.read())
    mod = 1000000
    print(num_subsets(n, mod))


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
