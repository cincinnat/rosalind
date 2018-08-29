#! /usr/bin/python3

import sys
import argparse
import signal
import functools


def fib(n, k):
    if n <= 2:
        return 1
    return fib(n-1, k) + k * fib(n-2, k)


def main(args):
    n, k = sys.stdin.read().split()
    n = int(n)
    k = int(k)

    print(fib(n, k))


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
