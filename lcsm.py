#! /usr/bin/python3

import sys
import argparse
import signal
import itertools
import bisect

import tools


class Vertex:
    def __init__(self, parent, label):
        self.parent = parent
        self.in_label = label
        self.chidren = []
        self.sids = set()
 

class SuffixTree:
    def __init__(self):
        self.strings = []
        self.__root = Vertex(None, None)


    def __add_suffix(self, string_id, root, suffix):
        def get_prefix_len(string1, string2):
            n = 0
            for ch1, ch2 in zip(string1, string2):
                if ch1 != ch2:
                    break
                n += 1
            return n


        def add_child(parent, label):
            v = Vertex(parent, label)
            v.sids.add(string_id)
            parent.chidren.append(v)
            return v


        def cut(child_index, child, prefix_len):
            head = child.in_label[:prefix_len]
            tail = child.in_label[prefix_len:]

            intermediate_vertex = Vertex(root, head)
            root.chidren[i] = intermediate_vertex

            intermediate_vertex.sids = child.sids | { string_id }
            intermediate_vertex.chidren.append(child)
            child.parent = intermediate_vertex
            child.in_label = tail

            return intermediate_vertex


        root.sids.add(string_id)

        for i, c in enumerate(root.chidren):
            if suffix[0] == c.in_label[0]:
                prefix_len = get_prefix_len(c.in_label, suffix)

                if prefix_len == len(suffix):
                    c.sids.add(string_id)
                    return

                elif prefix_len == len(c.in_label):
                    tail = suffix[prefix_len:]
                    self.__add_suffix(string_id, c, tail)
                    return

                else:
                    intermediate_vertex = cut(i, c, prefix_len)

                    tail = suffix[prefix_len:]
                    add_child(intermediate_vertex, tail)

                    return

        add_child(root, suffix)


    def add(self, string):
        string += '$'
        string_id = len(self.strings)
        self.strings.append(string)

        for i in range(len(string)):
            suffix = string[i:]
            self.__add_suffix(string_id, self.__root, suffix)


    def __str__(self):
        return '\n'.join(self.strings + self.__print(self.__root, 0))


    def __print(self, root, offset):
        values = dict(
            off = ' ' * offset,
            e = root.in_label,
            sids = root.sids,
        )
        lines =  ['{off}|->{e} {sids}'.format(**values)]
        for c in root.chidren:
            lines += self.__print(c, 4 + offset)

        return lines


    def traverse(self, root=None):
        root = root or self.__root
        yield root

        for child in root.chidren:
            for v in self.traverse(child):
                yield v


    def path(self, vertex):
        path = []
        while vertex.parent is not None:
            label = vertex.in_label
            if label.endswith('$'):
                label = label[:-1]

            path.append(label)
            vertex = vertex.parent

        return ''.join(reversed(path))


def mlcs(strings):
    stree = SuffixTree()
    for string in strings:
        stree.add(string)

    lcs = ''

    for v in stree.traverse():
        if len(strings) == len(v.sids):
            path = stree.path(v)
            if len(path) > len(lcs):
                lcs = stree.path(v)

    # print(stree)
    return lcs


def main(args):
    records = tools.io.read_fasta(sys.stdin)
    strings = [''.join(seq) for _, seq in records]


    # for i, s in enumerate(strings):
        # if 'GAGGGCATTGATTGGTATACTTAATGTAACGGTAAT' not in s:
            # print(i)
    # return

    subseq = mlcs(strings)
    print(subseq)


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
