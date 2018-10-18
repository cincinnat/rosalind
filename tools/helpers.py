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


def inc_indices(indices, base):
    indices[-1] += 1
    for i in range(len(indices)-1, 0, -1):
        if indices[i] < base:
            break
        indices[i-1] += indices[i] // base
        indices[i] = indices[i] % base


def gen_indices(base, n, init=0):
    indices = [init] * n
    while indices[0] < base:
        yield list(indices)  # copy
        inc_indices(indices, base)


def gen_kmers(alphabet, n):
    base = len(alphabet)
    for indices in gen_indices(base, n):
        yield ''.join((alphabet[i] for i in indices))
