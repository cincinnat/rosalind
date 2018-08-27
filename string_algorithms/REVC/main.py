#! /usr/bin/python3

import sys
import argparse
import signal
import functools


def main(args):
    s = sys.stdin.read().strip()

    complements = {
        'A': 'T',
        'T': 'A',
        'C': 'G',
        'G': 'C',
    }
    s = list(map(lambda ch: complements[ch], s))
    s = reversed(s)
    s = ''.join(s)

    print(s)


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
