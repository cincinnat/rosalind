#! /usr/bin/python3

import sys
import argparse
import signal
import itertools
import math

import tools


def candidate_pairs(spectrum, parent_mass):
    pairs = []
    for left, right in itertools.combinations(spectrum, 2):
        if not math.isclose(left + right, parent_mass, rel_tol=1.e-6):
            continue
        pairs.append((left, right))
    return pairs


def _check_mass(string, masses, parent_mass):
    mass = tools.spectrometry.mass(string)
    for left, right in itertools.combinations(masses, 2):
        if math.isclose(parent_mass - mass, left + right, rel_tol=1.e-6):
            return True
    return False


def _infer_protein(masses, n):
    for i, j in itertools.combinations(range(len(masses) - n), 2):
        mass = masses[j] - masses[i]
        acid = tools.spectrometry.find_amino_acid(mass)
        if acid is None:
            continue
        elif n == 1:
            yield acid
        else:
            for tail in _infer_protein(masses[j:], n-1):
                yield acid + tail


def infer_protein(pairs, n, parent_mass):
    masses = itertools.chain.from_iterable(pairs)
    masses = sorted(masses)
    for protein in _infer_protein(masses, n):
        if _check_mass(protein, masses, parent_mass):
            return protein

    assert False, 'should not be reached'


def main(args):
    inputs = map(float, sys.stdin.read().split())
    parent_mass = next(inputs)
    spectrum = list(inputs)
    n = len(spectrum) // 2 - 1

    pairs = candidate_pairs(spectrum, parent_mass)
    protein = infer_protein(pairs, n, parent_mass)
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
