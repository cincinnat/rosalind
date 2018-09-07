#! /usr/bin/python3

import sys
import argparse
import signal

import tools


def main(args):
    inputs = tools.io.read_fasta(sys.stdin)
    inputs = (''.join(seq) for _, seq in inputs)
    dna = next(inputs)
    introns = list(inputs)

    for intron in introns:
        assert dna.count(intron) == 1
        dna = dna.replace(intron, '')

    codon_table = tools.dna.codon_table()

    codons = tools.helpers.split_string(dna, 3)
    codons = list(codons)
    assert codon_table[codons[-1]] == 'Stop'
    codons = codons[:-1]

    protein = map(codon_table.get, codons)
    print(''.join(protein))


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
