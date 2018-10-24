#! /usr/bin/python3

import sys
import argparse
import signal
import itertools
import bisect

import tools


def mlcs(strings):
    stree = tools.suffix_tree.SuffixTree()
    for string in strings:
        stree.add(string)

    lcs = ''

    for v in stree.traverse():
        if len(strings) == len(v.sids):
            path = stree.path(v)
            if len(path) > len(lcs):
                lcs = stree.path(v)

    # print(stree)
    return lcs


def main(args):
    records = tools.io.read_fasta(sys.stdin)
    strings = [''.join(seq) for _, seq in records]


    # for i, s in enumerate(strings):
        # if 'GAGGGCATTGATTGGTATACTTAATGTAACGGTAAT' not in s:
            # print(i)
    # return

    subseq = mlcs(strings)
    print(subseq)


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
