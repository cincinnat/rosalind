#! /usr/bin/python3

import sys
import argparse
import signal
import functools
import collections


def hamming_distance(s1, s2):
    return sum((a != b for a, b in zip(s1, s2)))


def main(args):
    s = sys.stdin.read().split()

    # k homozygous dominant for a factor
    # m heterozygous,
    # n homozygous recessive
    k, m, n = tuple(map(int, s))
    N = k + m + n

    prop_dominant_allele = (
        1 - (n * (n-1) + n * m * .5 * 2 + m * (m-1) * .25) / N / (N-1)
    )
    print(prop_dominant_allele)



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
