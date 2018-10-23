#! /usr/bin/python3

import sys
import argparse
import signal
from scipy.stats import binom
import math

import tools


def main(args):
    n = int(sys.stdin.read().strip())
    p = .5

    A = []
    for i in range(2*n):
        A.append(binom(2*n, p).sf(i))

    A = [round(math.log10(p), 3) for p in A]
    print(*A)


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
