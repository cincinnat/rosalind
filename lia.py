#! /usr/bin/python3

import sys
import argparse
import signal
from scipy.stats import binom
import numpy as np

import tools

def main(args):
    inputs = sys.stdin.read().split()
    k, N = list(map(int, inputs))

    prob = {
        'AA': [1/2, 1/2, 0],
        'Aa': [1/4, 1/2, 1/4],
        'aa': [0, 1/2, 1/2],
    }

    # at each generation there is alway the same probability distribution:
    # P(AA) = P(aa) = 1/4, P(Aa) = 1/2
    #
    # thus P(AaBb) = 1/2 * 1/2 = 1/4

    def at_least(n, k, p):
        return sum((binom(n, p).pmf(i) for i in range(k, n+1)))

    print(at_least(2**k, N, 1/4))

    


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
