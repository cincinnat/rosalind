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
