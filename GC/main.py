#! /usr/bin/python3

import sys
import argparse
import signal
import functools


def iter_chunks(iterable, chunk_size):
    it = iter(iterable)
    while True:
        chunk = list(itertools.islice(it, chunk_size))
        if not chunk:
            break
        yield chunk


def read_fasta(fd):
    label = fd.readline().strip()

    while label and label.startswith('>'):
        label = label[1:]

        values = []
        for line in map(str.strip, fd):
            if not line.startswith('>'):
                values.append(line)
            else:
                break

        yield label, values
        label = line


def gc_content(dna):
    def count_gc(acc, ch):
        return acc + (ch in 'GC')
    return functools.reduce(count_gc, dna, 0) / len(dna)


def main(args):
    records = read_fasta(sys.stdin)

    def get_gc_content(rec):
        label, values = rec
        return label, gc_content(''.join(values))
    records = map(get_gc_content, records)

    label, value = max(records, key=lambda rec: rec[1])

    print(label)
    print(value * 100)
    


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
