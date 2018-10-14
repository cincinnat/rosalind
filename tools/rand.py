import math


def match_logprob(gc_content, s):
    ''' Probability of a random string to be equal to s.

    Returns the log-probability that a random string constructed with
    given gc_content is equal to s.
    '''

    def symbol_logprob(gc_content):
        prob_g = math.log(gc_content/2, 10)
        prob_a = math.log((1 - gc_content)/2, 10)
        return dict(
            A = prob_a,
            T = prob_a,
            G = prob_g,
            C = prob_g,
        )

    prob = symbol_logprob(gc_content)
    return sum((prob[ch] for ch in s))


def match_prob(gc_content, s):
    return math.pow(10., match_logprob(gc_content, s))
