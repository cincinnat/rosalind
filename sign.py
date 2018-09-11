#! /usr/bin/python3

import sys
import argparse
import signal
import itertools
import math
import numpy as np

import tools


def gen_permutations(n):
    for perm in itertools.permutations(range(n), n):
        yield np.array(perm) + 1


def gen_signs(n):
    for i in range(1 << n):
        sign = np.array([int(bit) for bit in np.binary_repr(i, width=n)])
        sign = sign * 2 - 1
        yield sign


def main(args):
    n = int(sys.stdin.read())

    permutations = list(gen_permutations(n))
    signs = list(gen_signs(n))

    print(len(permutations) * len(signs))
    for perm, sign in itertools.product(permutations, signs):
        signed_perm = perm * sign
        print(*signed_perm)


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
