#! /usr/bin/python3

import sys
import argparse
import signal
import math
import functools

import tools


def strig_prob(gc_content, s):
    return tools.rand.match_logprob(gc_content, s)


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
