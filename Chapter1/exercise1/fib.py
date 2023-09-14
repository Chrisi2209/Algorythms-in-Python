from math import sqrt

def my_fib(n):
    # only correct until fib(71) because of precision
    # time complexity: constant
    phi = (1 + sqrt(5)) / 2

    return round((phi**n - (1 - phi)**n) / sqrt(5))

def fib(n):
    # always correct
    # time complexity: linear
    prev, next = 1, 0

    for _ in range(n):
        next, prev = prev + next, next

    return next