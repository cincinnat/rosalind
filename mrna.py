#! /usr/bin/python3

import sys
import argparse
import signal
import collections

import tools


def main(args):
    string = sys.stdin.read().strip()

    codon_table = tools.rna.codon_table()
    original_codons = collections.defaultdict(int)
    for codon, acid in codon_table.items():
        original_codons[acid] += 1

    original_mrnas = 1
    n = 1000000
    for acid in string:
        original_mrnas = (original_mrnas * original_codons[acid]) % n
    original_mrnas = (original_mrnas * original_codons['Stop']) % n

    print(original_mrnas)



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
