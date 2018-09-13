#! /usr/bin/python3

import sys
import argparse
import signal
import numpy as np

import tools


def main(args):
    nodes = int(sys.stdin.readline().strip())
    inodes = nodes - 2
    print(inodes)


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
