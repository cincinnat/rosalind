#! /usr/bin/python3

import sys
import argparse
import signal
import numpy as np

import tools

_dtable = dict()

def motz(s, mod):
    if s in _dtable:
        return _dtable[s]
    if len(s) < 2:
        return 1

    def match(i, j):
        return int({s[i], s[j]} in [{'A', 'U'}, {'C', 'G'}])

    res = motz(s[1:], mod)
    for i in range(1, len(s)):
        if match(0, i):
            res = (res + motz(s[1:i], mod) * motz(s[i+1:], mod)) % mod

    _dtable[s] = res 
    return res


def main(args):
    inputs = tools.io.read_fasta(sys.stdin)
    rna = ''.join(next(inputs)[1])
    mod = 1000000

    print(motz(rna, mod))


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
