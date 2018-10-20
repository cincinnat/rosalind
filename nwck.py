#! /usr/bin/python3

import sys
import argparse
import signal

import tools


def find_dist(root, u, v):
    u = tools.newick.bfs(root, lambda n, _: n.label == u)
    assert u is not None

    path = None
    def visitor(node, current_path):
        nonlocal path
        if node.label == v:
            path = current_path
            return True

    v = tools.newick.bfs(u, visitor)
    assert v is not None

    def path_len(path, start):
        dist = 0
        while path[start] is not None:
            dist += 1
            start = path[start]
        return dist

    return path_len(path, v)


def main(args):
    inputs = map(str.strip, args.input)
    inputs = filter(bool, inputs)  # remove blanks
    inputs = tools.helpers.iter_chunks(inputs, 2)

    distances = []
    for string, pair in inputs:
        tree = tools.newick.parse(string)
        pair = pair.split()
        distances.append(find_dist(tree, *pair))

    print(*distances)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='description',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('input', nargs='?', type=argparse.FileType('r'),
        default=sys.stdin)

    args = parser.parse_args()

    try:
        main(args)
    except BrokenPipeError:
        sys.exit(128 + signal.SIGPIPE)
    except KeyboardInterrupt:
        sys.exit(128 + signal.SIGINT)
