#! /usr/bin/python3

import sys
import argparse
import signal
import itertools

import tools


def find_all(string, codons):
    locations = []
    for i in range(len(string) - 3):
        if string[i:i+3] in codons:
            locations.append(i)
    return locations


def candidate_proteins_locations(start_locations, stop_locations):
    for start in start_locations:
        for stop in stop_locations:
            if start < stop and (stop - start) % 3 == 0:
                yield (start, stop)
                break


def translate_to_protein(dna):
    codon_table = tools.dna.codon_table()

    codons = tools.helpers.split_string(dna, 3)
    protein = map(codon_table.get, codons)
    protein = list(protein)
    return ''.join(protein)


def find_candidate_proteins(dna):
    codon_table = tools.dna.codon_table()
    start_codon = 'ATG'
    stop_codons = set((k for k, v in codon_table.items() if v == 'Stop'))

    start_locations = find_all(dna, {start_codon})
    stop_locations = find_all(dna, stop_codons)

    candidate_proteins = candidate_proteins_locations(start_locations, stop_locations)
    candidate_proteins = list(candidate_proteins)

    for loc in candidate_proteins:
        yield translate_to_protein(dna[slice(*loc)])


def main(args):
    dna = tools.io.read_fasta(sys.stdin)
    dna = ''.join(next(dna)[1])
    complement_dna = tools.dna.reverse_complement(dna)

    proteins = map(find_candidate_proteins, [dna, complement_dna])
    proteins = itertools.chain.from_iterable(proteins)
    proteins = set(proteins)

    for protein in proteins:
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
