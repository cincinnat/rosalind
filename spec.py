#! /usr/bin/python3

import sys
import argparse
import signal
import itertools
import math

import tools


def find_amino_acid(mass):
    for a, m in tools.spectrometry.mass_table.items():
        if math.isclose(mass, m, rel_tol=1e-6):
            return a
    assert False, 'should never be reached'


def main(args):
    spectrum = map(str.strip, sys.stdin)
    spectrum = list(map(float, spectrum))

    protein = []
    for x, y in zip(spectrum[:-1], spectrum[1:]):
        mass = y - x
        protein.append(find_amino_acid(mass))

    protein = ''.join(protein)
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
