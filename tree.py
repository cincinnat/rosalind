#! /usr/bin/python3

import sys
import argparse
import signal
import numpy as np

import tools


def main(args):
    n_vertices = int(sys.stdin.readline().strip())
    n_edges = len(sys.stdin.readlines())
    print(n_vertices - n_edges - 1)


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
