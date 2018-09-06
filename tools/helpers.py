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
