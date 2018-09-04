#! /usr/bin/python3

import sys
import argparse
import signal
import itertools

import tools


rna_codon_table = tools.rna.codon_table()


def iter_chunks(iterable, chunk_size):
    it = iter(iterable)
    while True:
        chunk = list(itertools.islice(it, chunk_size))
        if not chunk:
            break
        yield chunk


def main(args):
    mRNA = sys.stdin.read().strip()

    codons = iter_chunks(mRNA, chunk_size=3)
    codons = map(''.join, codons)

    amino_acids = map(lambda codon: rna_codon_table[codon], codons)
    amino_acids = itertools.takewhile(lambda s: s != 'Stop', amino_acids)

    protein = ''.join(amino_acids)
    print(protein)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='description',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    args = parser.parse_args()

    try:
        main(args)
    except BrokenPipeError:
        sys.exit(128 + signal.SIGPIPE)
    except KeyboardInterrupt:
        picksys.exit(128 + signal.SIGINT)
