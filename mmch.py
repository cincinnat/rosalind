#! /usr/bin/python3

import sys
import argparse
import signal
import math

import tools


def main(args):
    _, rna = next(tools.io.read_fasta(sys.stdin))
    rna = ''.join(rna)

    a = rna.count('A')
    u = rna.count('U')
    c = rna.count('C')
    g = rna.count('G')

    # if there are n, m bonding bases (n <= m)
    # then there are n! / (n-m)! different basepairs
    #
    def cnt(m, n):
        m, n = sorted([m, n])
        return math.factorial(n) // math.factorial(n-m)
    print(cnt(a, u) * cnt(c, g))


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
