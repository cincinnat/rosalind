#! /usr/bin/python3

import sys
import argparse
import signal

import tools


def inc(value, base):
    value[-1] += 1
    for i in range(len(value)-1, 0, -1):
        value[i-1] += value[i] // base
        value[i] = value[i] % base


def main(args):
    inputs = map(str.strip, sys.stdin.readlines())
    alphabet = next(inputs).split()
    sz = int(next(inputs))

    for string in tools.helpers.gen_kmers(alphabet, sz):
        print(string)


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
