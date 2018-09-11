#! /usr/bin/python3

import sys
import argparse
import signal
import math

import tools


# When there are n matching pairs in a string (i.e. A-U or C-G) then
# the number of possible perfect matchings are n!.
# Thus, if number of occurences of A ans U is the sames as for C and G,
# then the total number of perfect matches for a DNA string is
#     count(A)! * count(C)!


def main(args):
    inputs = tools.io.read_fasta(sys.stdin)
    rna = ''.join(next(inputs)[1])

    print(math.factorial(rna.count('A')) * math.factorial(rna.count('C')))


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
