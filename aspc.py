#! /usr/bin/python3

import sys
import argparse
import signal
import math

import tools


# https://en.wikipedia.org/wiki/Binomial_coefficient#Recursive_formula
#
def binom_table(n, mod):
    table = dict()
    for j in range(n+1):
        for i in range(j, n+1):
            if j == 0 or i == j:
                table[(i, j)] = 1
            else:
                table[(i, j)] = (table[(i-1, j-1)] + table[(i-1, j)]) % mod
    return table



def num_subsets(m, n, mod):
    binoms = binom_table(n, mod)

    cnt = 0
    for k in range(m, n+1):
        cnt = (cnt + binoms[(n, k)]) % mod
    return cnt % mod



def main(args):
    inputs = map(int, sys.stdin.read().split())
    n, m = list(inputs)
    mod = 1000000

    print(num_subsets(m, n, mod))


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
