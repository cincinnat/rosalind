#! /usr/bin/python3

import sys
import argparse
import signal

import tools


def main(args):
    inputs = tools.io.read_fasta(sys.stdin)
    dna = ''.join(next(inputs)[1])

    alphabet = 'ACGT'
    n = 4

    composition = { kmer: 0 for kmer in tools.helpers.gen_kmers(alphabet, n) }
    for i in range(len(dna)-n+1):
        composition[dna[i:i+n]] += 1

    composition = [v for _, v in sorted(composition.items())]
    print(*composition)


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
