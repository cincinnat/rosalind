import collections
import itertools

from . import helpers

_mass_table = '''
A   71.03711
C   103.00919
D   115.02694
E   129.04259
F   147.06841
G   57.02146
H   137.05891
I   113.08406
K   128.09496
L   113.08406
M   131.04049
N   114.04293
P   97.05276
Q   128.05858
R   156.10111
S   87.03203
T   101.04768
V   99.06841
W   186.07931
Y   163.06333
'''

# Monoisotopic mass table
#
mass_table = helpers.parse(_mass_table, dtype=float)


def minkowski_diff(s1, s2):
    assert isinstance(s1, collections.Counter)
    assert isinstance(s2, collections.Counter)

    def diff(s1, s2):
        for a, b in itertools.product(s1.elements(), s2.elements()):
            yield a - b

    return collections.Counter(diff(s1, s2))


def minkowski_sum(s1, s2):
    assert isinstance(s1, collections.Counter)
    assert  isinstance(s2, collections.Counter)

    def diff(s1, s2):
        for a, b in itertools.product(s1.elements(), s2.elements()):
            yield a + b

    return collections.Counter(diff(s1, s2))
