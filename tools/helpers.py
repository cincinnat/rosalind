import itertools

def iter_chunks(iterable, chunk_size):
    it = iter(iterable)
    while True:
        chunk = list(itertools.islice(it, chunk_size))
        if not chunk:
            break
        yield chunk


def split_string(string, substring_len):
    return map(''.join, iter_chunks(string, chunk_size=substring_len))


def parse(table, dtype=str):
    table = table.split()
    keys = table[::2]
    values = map(dtype, table[1::2])
    return dict(zip(keys, values))


def hamming_distance(s1, s2):
    return sum((a != b for a, b in zip(s1, s2)))


def inc_indices(indices, base):
    indices[-1] += 1
    for i in range(len(indices)-1, 0, -1):
        indices[i-1] += indices[i] // base
        indices[i] = indices[i] % base


def gen_kmers(alphabet, n):
    base = len(alphabet)
    indices = [0] * base
    while indices[0] < base:
        yield ''.join((alphabet[i] for i in indices))
        inc_indices(indices, base)
