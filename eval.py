#! /usr/bin/python3

import sys
import argparse
import signal

import tools


def num_expected_occurences(n, s, gc_content):
    p = tools.rand.match_prob(gc_content, s)
    return (n-len(s)+1) * p


def main(args):
    n = int(sys.stdin.readline().strip())
    s = sys.stdin.readline().strip()
    A = [float(v) for v in sys.stdin.readline().split()]

    B = [num_expected_occurences(n, s, gc_content) for gc_content in A]
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
