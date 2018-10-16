import math


def match_logprob(gc_content, s, base=10):
    ''' Probability of a random string to be equal to s.

    Returns the log-probability that a random string constructed with
    given gc_content is equal to s.
    '''

    def log(x, base=base):
        return math.log(x, base) if x != 0 else float('-inf')

    l = len(s)
    n_gc = len([ch for ch in s if ch in 'GC'])
    return - l * log(2) + n_gc * log(gc_content) + (l-n_gc) * log(1-gc_content)


def match_prob(gc_content, s):
    return math.pow(10., match_logprob(gc_content, s, base=10))
