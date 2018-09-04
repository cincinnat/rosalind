#! /usr/bin/python3

import sys
import argparse
import signal
import re
import requests
import io

import tools


def get_protein(protein_id):
    r = requests.get('https://www.uniprot.org/uniprot/%s.fasta' % protein_id)
    r.raise_for_status()

    content = io.StringIO(r.text)
    string = next(tools.io.read_fasta(content))
    string = ''.join(string[1])
    return string


def search(string):
    pattern = re.compile('N[^P][ST][^P]')
    locations = []

    offset = 0
    while True:
        match = pattern.search(string, offset)
        if match is None:
            break
        locations.append(match.span()[0] + 1)
        offset = match.span()[0] + 1

    return locations


def main(args):
    protein_ids = list(map(str.strip, sys.stdin))

    strings = map(get_protein, protein_ids)
    locations = map(search, strings)

    for protein_id, loc in zip(protein_ids, locations):
        if loc:
            print(protein_id)
            print(*loc)


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
