#! /usr/bin/python3

import sys
import argparse
import signal
import functools
import collections

import tools


def find_palindroms(dna, complement, offset):
    min_len = 4
    max_len = 12

    for end in range(offset + min_len, offset + max_len + 1):
        if end > len(dna):
            break

        first = dna[offset:end]
        second = complement[::-1][offset:end][::-1]
        if first == second:
            yield (offset+1, end-offset)  # starts with 1


def main(args):
    _, dna = next(tools.io.read_fasta(sys.stdin))
    dna = ''.join(dna)
    complement = tools.dna.reverse_complement(dna)

    for i in range(len(dna)):
        for palindrom in find_palindroms(dna, complement, i):
            print(*palindrom)



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
