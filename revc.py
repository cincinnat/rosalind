#! /usr/bin/python3

import sys
import argparse
import signal
import functools

import tools


def main(args):
    s = sys.stdin.read().strip()

    print(tools.reverse_complement(s))


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
