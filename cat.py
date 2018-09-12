#! /usr/bin/python3

import sys
import argparse
import signal
import numpy as np

import tools

# as usual, my solution is overcomplicated and can be simplified to
#
# def catalan(s):
#     if s not in c:
#         c[s] = sum([catalan(s[1:k]) * c[s[0]+s[k]] * catalan(s[k+1:]) for k in range(1, len(s))])
#     return c[s]


def catlan(string):
    n = len(string)
    C = np.zeros((n, n), dtype=int)

    def I(i, j):
        return int({string[i], string[j]} in [{'A', 'U'}, {'C', 'G'}])

    base = 1000000

    for i in range(n-2, -1, -1):
        for j in range(i, n):
            if i == j:
                C[i, j] = 0
            elif i+1 == j:
                C[i, j] = I(i, j)
            else:
                C[i, j] = I(i, j) * C[i+1, j-1] + I(i, i+1) * C[i+2, j]
                for k in range(i+2, j):
                    C[i, j] += I(i, k) * C[i+1, k-1] * C[k+1, j] % base

    return C[0, n-1] % base


def main(args):
    inputs = tools.io.read_fasta(sys.stdin)
    rna = ''.join(next(inputs)[1])

    print(catlan(rna))


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
