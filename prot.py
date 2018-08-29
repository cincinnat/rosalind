#! /usr/bin/python3

import sys
import argparse
import signal
import itertools


rna_codon_table = '''
UUU F      CUU L      AUU I      GUU V
UUC F      CUC L      AUC I      GUC V
UUA L      CUA L      AUA I      GUA V
UUG L      CUG L      AUG M      GUG V
UCU S      CCU P      ACU T      GCU A
UCC S      CCC P      ACC T      GCC A
UCA S      CCA P      ACA T      GCA A
UCG S      CCG P      ACG T      GCG A
UAU Y      CAU H      AAU N      GAU D
UAC Y      CAC H      AAC N      GAC D
UAA Stop   CAA Q      AAA K      GAA E
UAG Stop   CAG Q      AAG K      GAG E
UGU C      CGU R      AGU S      GGU G
UGC C      CGC R      AGC S      GGC G
UGA Stop   CGA R      AGA R      GGA G
UGG W      CGG R      AGG R      GGG G
'''


def parse_codon_table():
    table = rna_codon_table.split()
    codons = table[::2]
    amino_acids = table[1::2]
    return dict(zip(codons, amino_acids))

rna_codon_table = parse_codon_table()


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
        sys.exit(128 + signal.SIGINT)
