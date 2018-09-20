#! /usr/bin/python3

import sys
import argparse
import signal
import itertools
import math

import tools


def neighbors(seq, i, j):
    return abs(seq[i] - seq[j]) == 1


def find_breaks(seq):
    seq = [min(seq)-1] + seq + [max(seq)+1]
    breaks = []
    for i in range(len(seq)-1):
        if not neighbors(seq, i, i+1):
            breaks.append(i)
    return breaks


def flip(seq, i, j):
    return seq[0:i] + seq[i:j][::-1] + seq[j:len(seq)]


def _reversal_distance(seq, breaks):
    if len(breaks) == 0:
        return 0
    if len(breaks) == 2:
        return 1
    if len(breaks) == 3:
        return 2

    # there is always > 1 break
    assert len(breaks) != 1, (seq, breaks)

    dist = float('inf')

    for i in breaks:
        for j in breaks[i+1:]:
            new_seq = flip(seq, i, j)
            new_breaks = find_breaks(new_seq)
            if len(new_breaks) < len(breaks):
                # plus one flip
                d = 1 + _reversal_distance(new_seq, new_breaks)
                dist = min(d, dist)
    return dist


def reversal_distance(a, b):
    # map `a` into sequence [0 .. len(a)-1]
    code_table = dict(zip(a, range(len(a))))
    b = list(map(code_table.get, b))

    breaks = find_breaks(b)

    return _reversal_distance(b, breaks)


def main(args):
    inputs = filter(bool, map(str.split, sys.stdin))
    inputs = map(lambda l: list(map(int, l)), inputs)
    pairs = tools.helpers.iter_chunks(inputs, chunk_size=2)
    distances = itertools.starmap(reversal_distance, pairs)

    print(*distances)


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
