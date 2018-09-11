#! /usr/bin/python3

import sys
import argparse
import signal
import math
import functools


def symbol_logprob(gc_content):
    prob_g = math.log(gc_content/2, 10)
    prob_a = math.log((1 - gc_content)/2, 10)
    return dict(
        A = prob_a,
        T = prob_a,
        G = prob_g,
        C = prob_g,
    )


def strig_prob(gc_content, s):
    prob = symbol_logprob(gc_content)
    return sum((prob[ch] for ch in s))


def main(args):
    s = sys.stdin.readline().strip()
    A = list(map(float, sys.stdin.readline().split()))

    B = [strig_prob(gc_content, s) for gc_content in A]
    print(*B)


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
