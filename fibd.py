#! /usr/bin/python3

import sys
import argparse
import signal
import functools


# Let a(n) is the number of adult couples at nth step
#     c(n) - child couples
#     d(n) - dead rabbits
#
# F(n) = a(n) + c(n)
#
# a(n) =  F(n-1) - d(n) + c(n)   // all from the last step except for dead
# d(n) = c(n-m) if n >= m else 0   // at nth step die rabbits born m moths before
# c(n) = a(n-1)  // at the previous step all adult couples produces offspring
#
# After substitution we get the following mutual recurrence:
#    F(n) = F(n-1) + c(n) - c(n-m)
#    c(n) = F(n-1) - c(n-1)
#


# UPD: and of courcse my solution is overcomplicated
# http://rosalind.info/problems/fibd/solutions/
# 
# Solution 1: count ages
#
#    def fib(n,k=1):
#        ages = [1] + [0]*(k-1)
#        for i in xrange(n-1):
#            ages = [sum(ages[1:])] + ages[:-1]
#        return sum(ages)
#
#
# Solution 2: recursion
#
#    for i in xrange(2,n):
#        f[i]=f[i-1]+f[i-2]
#        if i>=k:
#            f[i]-=f[(i-k)-1]
#    print f[i]
#
# Solution 3:
#
#    F(n) = usual Fibonacci for n in 1..m
#    F(n) = sum F(n-i) for i in 2..m, n in m+1..N


def fibd(n, m):
    f = [1] * n
    c = [1] * n

    for i in range(1, n):
        c[i] = f[i-1] - c[i-1]

        f[i] = f[i-1] + c[i]
        if i >= m:
            f[i] -= c[i-m]

    return f[-1]


def main(args):
    n, m = sys.stdin.read().split()
    n = int(n)
    m = int(m)

    print(fibd(n, m))


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
