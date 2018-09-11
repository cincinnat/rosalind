#! /usr/bin/python3

import sys
import argparse
import signal
import numpy as np

import tools


def make_graph(seq):
    adj_matrix = np.zeros((len(seq), len(seq)), dtype=float)

    # There is an edge from i'th element to j'th element if
    # i < j and seq[i] < seq[j].
    # 0 at position (j,i) means that there are no edg from i to j.
    #
    for i in range(len(seq)):
        for j in range(i):
            if seq[j] < seq[i]:
                adj_matrix[i,j] = 1

    return adj_matrix


def dag_shortest_path(adj_matrix):
    n = len(adj_matrix)
    path_len = [0] * n
    path = [0] * n

    for i in range(n):
        for j in range(i):
            if adj_matrix[i, j] == 0:
                continue
            if path_len[i] > path_len[j] + adj_matrix[i, j]:
                path_len[i] = path_len[j] + adj_matrix[i, j]
                path[i] = j

    # note that the shortest path will alway include the first and
    # the last vertices (i.e. -inf and +inf respectively).
    #
    shortest_path = [n-1]
    while True:
        prev = path[shortest_path[-1]]
        shortest_path.append(prev)
        if prev == 0:
            break

    return shortest_path[::-1]


def dag_longest_path(adj_matrix):
    return dag_shortest_path(adj_matrix * -1)


# There are better solutions. In general, the longest increasing
# subsequence of a sequence S is the longest common subsequence of
# S and sorted(S). If S is a permutation of the sequnces 1..len(S)
# then there is a faster solution (see on wikipedia).
#

def main(args):
    inputs = map(str.strip, sys.stdin.readlines())
    sz = int(next(inputs))
    seq = next(inputs).split()
    seq = list(map(int, seq))

    seq = [float('-inf')] + seq + [float('+inf')]

    # the longes increasing subsequence
    #
    #note that the vertices (aka seq) are already topologically sorted
    adj_matrix = make_graph(seq)

    longest_path = dag_longest_path(adj_matrix)
    subseq = [seq[i] for i in longest_path[1:-1]]
    print(*subseq)


    # the longes decreasing subsequence
    #
    seq[1:-1] = seq[1:-1][::-1]
    adj_matrix = make_graph(seq)

    longest_path = dag_longest_path(adj_matrix)
    subseq = [seq[i] for i in longest_path[1:-1]]
    subseq = subseq[::-1]
    print(*subseq)



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
