#! /usr/bin/python3

import sys
import argparse
import signal
import numpy as np

import tools


alphabet = sorted('ACGT')


def get_profile(strings):
    profile = list()
    for ch in alphabet:
        profile.append((strings == ch).sum(axis=0))
    profile = np.array(profile)

    return profile


def get_consensus(profile):
    consensus = np.argmax(profile, axis=0)
    return ''.join([alphabet[i] for i in consensus])


def main(args):
    records = tools.io.read_fasta(sys.stdin)
    strings = [list(''.join(seq)) for _, seq in records]
    strings = np.array(strings)

    profile = get_profile(strings)
    consensus = get_consensus(profile)

    print(consensus)
    for i, row in enumerate(profile):
        print('%s:' % alphabet[i], *row)



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
