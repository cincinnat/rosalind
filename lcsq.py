#! /usr/bin/python3

import sys
import argparse
import signal
import dataclasses
import typing
import numpy as np

import tools


@dataclasses.dataclass
class Cell:
    lcs_len: int = 0
    arrow: typing.Tuple[int, int] = None


def lcs(s, t):
    table = np.empty(shape=(len(s)+1, len(t)+1), dtype=object)
    vCell = np.vectorize(Cell)
    table[:,:] = vCell(np.zeros(table.shape, dtype=int))

    for i in range(1, table.shape[0]):
        for j in range(1, table.shape[1]):
            if s[i-1] == t[j-1]:
                arrow = (i-1, j-1)
                table[i, j].arrow = arrow
                table[i, j].lcs_len = table[arrow].lcs_len + 1
            elif table[i-1, j].lcs_len > table[i, j-1].lcs_len:
                arrow = (i-1, j)
                table[i, j].arrow = arrow
                table[i, j].lcs_len = table[arrow].lcs_len
            else:
                arrow = (i, j-1)
                table[i, j].arrow = arrow
                table[i, j].lcs_len = table[arrow].lcs_len

    lcs = []
    loc = (table.shape[0]-1, table.shape[1]-1)
    while table[loc].lcs_len > 0:
        if table[loc].arrow == (loc[0]-1, loc[1]-1):
            lcs.append(s[loc[0]-1])
        loc = table[loc].arrow

    return ''.join(reversed(lcs))


def main(args):
    inputs = tools.io.read_fasta(sys.stdin)
    s, t = [''.join(seq) for _, seq in inputs]

    print(lcs(s, t))


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
