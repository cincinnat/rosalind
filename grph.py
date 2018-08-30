#! /usr/bin/python3

import sys
import argparse
import signal

import tools

def main(args):
    records = tools.io.read_fasta(sys.stdin)

    vertices = [(key, ''.join(val)) for key, val in records]

    k = 3

    edges = []
    for s_key, s_value in vertices:
        for t_key, t_value in vertices:
            if s_key == t_key:
                continue
            if s_value[:k] == t_value[-k:]:
                edges.append((t_key, s_key))

    for edge in edges:
        print(*edge)



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
