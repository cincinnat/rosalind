#! /usr/bin/python3

import sys
import argparse
import signal


def main(args):
    s = sys.stdin.read()
    s = s.replace('T', 'U')
    sys.stdout.write(s)


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
