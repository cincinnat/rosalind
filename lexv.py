#! /usr/bin/python3

import sys
import argparse
import signal

import tools


def gen_indices(base, sz):
    indices = tools.helpers.gen_indices(base, sz, init=-1)
    next(indices)  # skip [-1, ..., -1]
    for i in indices:
        yield list(reversed(i))


def main(args):
    inputs = map(str.strip, sys.stdin.readlines())
    alphabet = next(inputs).split()
    sz = int(next(inputs))

    base = len(alphabet)

    indices = gen_indices(base, sz)

    # we would generate in the right order (e.g. using a search tree),
    # but this way is easier
    #
    indices = sorted(indices)

    for perm in indices:
        string = [alphabet[i] for i in perm if i >= 0]
        string = ''.join(string)
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
