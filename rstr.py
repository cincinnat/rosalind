#! /usr/bin/python3

import sys
import argparse
import signal
from scipy.stats import binom

import tools

def main(args):
    N, x, s = sys.stdin.read().split()
    N = int(N)
    x = float(x)

    prob = tools.rand.match_prob(x, s)
    print(1 - binom(N, prob).pmf(0))

    


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
