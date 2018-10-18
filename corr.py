#! /usr/bin/python3

import sys
import argparse
import signal
import numpy as np
import itertools

import tools


def correct_error(read, correct_reads):
    for s in correct_reads:
        if tools.dist.hamming_distance(s, read) == 1:
            return s
    assert False


def main(args):
    inputs = tools.io.read_fasta(sys.stdin)
    reads = [ ''.join(seq) for _, seq in inputs ]
    complements = [ tools.dna.reverse_complement(s) for s in reads ]

    correct_reads = set()
    for _, g in itertools.groupby(sorted(reads + complements)):
        g = list(g)
        if len(g) >= 2:
            correct_reads |= set(g)


    for read in reads:
        if read in correct_reads:
            continue

        corrected = correct_error(read, correct_reads)
        print('%s->%s' % (read, corrected))



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
