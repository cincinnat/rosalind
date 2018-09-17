#! /usr/bin/python3

import sys
import argparse
import signal

import tools


def overlap(s, P, k):
    for l in range(P[k-1]+1, 0, -1):
        if s.startswith(s[k-l+1:k+1]):
            return l
    return 0


def main(args):
    _, s = next(tools.io.read_fasta(sys.stdin))
    s = ''.join(s)

    P = [0] * len(s)
    for k in range(1, len(s)):
        P[k] = overlap(s, P, k)
    print(*P)


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
