import collections
import itertools

__all__ = [
    'hamming_distance',
    'edit_matrix',
    'edit_dist',
    'reversal_distance',
]


def hamming_distance(s1, s2):
    return sum((a != b for a, b in zip(s1, s2)))


def edit_matrix(s1, s2, indel_weight=1, substitution_weight=1):
    Cell = collections.namedtuple('Arrow', ['arrow', 'dist'])

    def weight(u, v):
        if u[0] != v[0] and u[1] != v[1]:
            # The short version
            #     (s1[..] != s2[..]) * substitution_weight
            # will not work if `substitution_weight` is an infinity
            # because `inf * 0` gives nan.
            #
            if s1[u[0]] != s2[u[1]]:
                return substitution_weight

            return 0
        return indel_weight

    dist = dict()
    for v in itertools.product(range(len(s1)+1), range(len(s2)+1)):
        i, j = v
        if i == 0 and j == 0:
            dist[v] = Cell(v, 0)
        elif i == 0:
            u = (i, j-1)
            dist[v] = Cell(u, weight(u, v) + dist[u].dist)
        elif j == 0:
            u = (i-1, j)
            dist[v] = Cell(u, weight(u, v) + dist[u].dist)
        else:
            parents = [(i-1, j), (i, j-1), (i-1, j-1)]
            weights = [weight(u, v) + dist[u].dist for u in parents]
            w = min(weights)
            u = parents[weights.index(w)]
            dist[v] = Cell(u, w)

    r1 = []
    r2 = []
    cur = v
    while cur != (0, 0):
        i, j = dist[cur].arrow
        if i != cur[0] and j != cur[1]:
            r1.append(s1[i])
            r2.append(s2[j])
        elif i != cur[0]:
            r1.append(s1[i])
            r2.append('-')
        else:
            r1.append('-')
            r2.append(s2[j])
        cur = dist[cur].arrow

    return dist[v].dist, [''.join(reversed(r1)), ''.join(reversed(r2))]


def edit_dist(s1, s2, indel_weight=1, substitution_weight=1):
    dist, _ = edit_matrix(s1, s2, indel_weight, substitution_weight)
    return dist


def _find_breaks(seq):
    def neighbors(seq, i, j):
        return abs(seq[i] - seq[j]) == 1

    seq = [min(seq)-1] + seq + [max(seq)+1]
    breaks = []
    for i in range(len(seq)-1):
        if not neighbors(seq, i, i+1):
            breaks.append(i)
    return breaks


def _flip(seq, i, j):
    return seq[0:i] + seq[i:j][::-1] + seq[j:len(seq)]


def _reversal_distance(seq, breaks):
    if len(breaks) == 0:
        return 0, []
    if len(breaks) == 2:
        return 1, [tuple(breaks)]

    # there is always > 1 break
    assert len(breaks) != 1, (seq, breaks)

    dist = float('inf')
    reversals = None

    for off, i in enumerate(breaks):
        for j in breaks[off+1:]:
            new_seq = _flip(seq, i, j)
            new_breaks = _find_breaks(new_seq)
            if len(new_breaks) < len(breaks):
                d, r = _reversal_distance(new_seq, new_breaks)
                d += 1  # plus one flip
                if d < dist:
                    dist = d
                    reversals = [(i, j)] + r

    return dist, reversals


def _reversal_distance_init(a, b):
    # map `b` into sequence [0 .. len(b)-1]
    code_table = dict(zip(b, range(len(b))))
    a = list(map(code_table.get, a))

    breaks = _find_breaks(a)

    return (a, breaks)


def reversal_distance(a, b):
    dist, _ = _reversal_distance(*_reversal_distance_init(a, b))
    return dist


def reversals_path(a, b):
    '''Return a collection of reversals sorting a into b.
    '''

    _, reversals = _reversal_distance(*_reversal_distance_init(a, b))
    return reversals
