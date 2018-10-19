#! /usr/bin/python3

import sys
import argparse
import signal

import tools


def main(args):
    n = int(sys.stdin.readline().strip())
    a = eval(sys.stdin.readline())
    b = eval(sys.stdin.readline())
    u = set(range(1, n+1))

    print(a | b)
    print(a & b)
    print(a - b)
    print(b - a)
    print(u - a)
    print(u - b)


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
