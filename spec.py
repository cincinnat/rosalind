#! /usr/bin/python3

import sys
import argparse
import signal
import itertools

import tools


def main(args):
    spectrum = map(str.strip, sys.stdin)
    spectrum = list(map(float, spectrum))

    protein = tools.spectrometry.infer_protein(spectrum)
    assert protein is not None
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
