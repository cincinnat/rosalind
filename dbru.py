#! /usr/bin/python3

import sys
import argparse
import signal

import tools


def main(args):
    strings = list(map(str.strip, sys.stdin))
    complements = list(map(tools.dna.reverse_complement, strings))
    kmers = set(strings + complements)

    for kmer in kmers:
        print('(%s, %s)' % (kmer[:-1], kmer[1:]))


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
