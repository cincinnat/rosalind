#! /usr/bin/python3

import sys
import argparse
import signal
import numpy as np

import tools


def main(args):
    inputs = tools.io.read_fasta(sys.stdin)
    s1 = ''.join(next(inputs)[1])
    s2 = ''.join(next(inputs)[1])
    assert len(s1) == len(s2)

    transitions = 0
    transversions = 0
    for a, b in zip(s1, s2):
        if a == b:
            continue
        if {a, b} in [{'A', 'G'}, {'C', 'T'}]:
            transitions += 1
        else:
            transversions += 1

    print(transitions/transversions)


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
