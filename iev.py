#! /usr/bin/python3

import sys
import argparse
import signal

import tools

def main(args):
    counters = sys.stdin.read().split()
    counters = list(map(int, counters))

    couples = [
        ('AA', 'AA'),
        ('AA', 'Aa'),
        ('AA', 'aa'),
        ('Aa', 'Aa'),
        ('Aa', 'aa'),
        ('aa', 'aa'),
    ]
    assert len(counters) == len(couples)

    def prob_of_domininat_factor(first, second):
        def prob_recessive(parent):
            return parent.count('a') / len(parent)
        return 1 - prob_recessive(first) * prob_recessive(second)

    offspring_size = 2

    expected_dominant = 0
    for cnt, couple in zip(counters, couples):
        expected_dominant += cnt * prob_of_domininat_factor(*couple)
    expected_dominant *= offspring_size

    print(expected_dominant)
    


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
