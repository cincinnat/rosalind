import json


class Vertex:
    def __init__(self, parent, label):
        self.parent = parent
        self.in_label = label
        self.chidren = []
        self.sids = set()


    def as_dict(self):
        return dict(
            self = id(self),
            parent = id(self.parent),
            in_label = self.in_label,
            sids = list(self.sids),
            chidren = [c.as_dict() for c in self.chidren],
        )
 

class SuffixTree:
    def __init__(self, end='$'):
        self.end = '$'
        self.strings = []
        self.root = Vertex(None, None)


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
        string += self.end
        string_id = len(self.strings)
        self.strings.append(string)

        for i in range(len(string)):
            suffix = string[i:]
            self.__add_suffix(string_id, self.root, suffix)


    def __str__(self):
        return json.dumps(self.root.as_dict(), indent=4)


    def traverse(self, root=None):
        root = root or self.root
        yield root

        for child in root.chidren:
            for v in self.traverse(child):
                yield v


    def path(self, vertex):
        path = []
        while vertex.parent is not None:
            label = vertex.in_label
            if label.endswith(self.end):
                label = label[:-1]

            path.append(label)
            vertex = vertex.parent

        return ''.join(reversed(path))


    def find(self, substr, root=None):
        root = root or self.root

        for child in root.chidren:
            label = child.in_label

            if label.endswith(self.end) and label.startswith(substr):
                return child
            elif substr == label:
                return child
            elif substr.startswith(label):
                return self.find(substr[len(label):], child)

        return None
