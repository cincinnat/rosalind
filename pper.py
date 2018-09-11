#! /usr/bin/python3

import sys
import argparse
import signal
import math
import functools


# the number of partial permutations is
#    C(n, k) * k!
# or, after some simplification,
#    n * (n-1) * ... (n-k+1)


def main(args):
    inputs = map(int, sys.stdin.read().split())
    n, k = list(inputs)


    base = 1000000
    def mul(a, b):
       return ((a % base) * (b % base)) % base
    print(functools.reduce(mul, (i for i in range(n, n-k, -1)), 1) % base)
    



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
