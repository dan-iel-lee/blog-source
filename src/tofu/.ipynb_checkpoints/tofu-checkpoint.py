from functools import reduce
from math import factorial, inf, comb, pow
from typing import List
import pandas as pd



def multiset_perms(multiset: list):
    numerator = factorial(sum(multiset))
    denominator = reduce(lambda acc, x: acc * factorial(x), multiset, 1)
    return numerator/denominator


memo = [[[[[] for m in range(6 + 1)] for k in range(30)] for j in range(100)] for length in range(6 + 1)]


# Generates the multisets for a given length, number of flips (n), flips to brown (k), and number of faces (m)
def generate_multisets_helper(length: int, k: int, n: int, m: int) -> List[List[int]]:
    # base case
    if length == 1:
        if (m > 0 and n >= k) or (m == 0 and n < k):
            memo[length][n][k][m] = [[n]]
            return memo[length][n][k][m]
        # if conditions aren't satisfied, then there's no possible such multiset
        return []

    # memoization
    if len(memo[length][n][k][m]) > 0:
        return memo[length][n][k][m]

    adder = 0 if m == 0 else k # add k if this is one of the first m faces
    maxi = min(n + 1, k if m == 0 else inf) # upper bound
    multisets = []
    for i in range(adder, maxi):
        next_res = generate_multisets_helper(length - 1, k, n - i, max(m - 1, 0))

        current = list(map(lambda ms: ms + [i], next_res))
        multisets.extend(current)

    memo[length][n][k][m] = multisets
    return multisets


def generate_multisets(k: int, n: int, m: int):
    return generate_multisets_helper(6, k, n, m)


def prob_Y(k: int, n: int, m: int):
    multisets = generate_multisets(k, n, m)

    size_Y = reduce(lambda acc, ms: acc + multiset_perms(ms), multisets, 0)  # size of event Y_{k,n}^m
    size_omega = pow(6, n) # size of the sample space

    return size_Y / size_omega


def prob_X_equals_m(k: int, n: int, m: int):
    combs = comb(6, m)

    return combs * prob_Y(k, n, m)


def prob_X_atleast_m(n: int, k: int, m: int):
    return sum(map(lambda i: prob_X_equals_m(k, n, i), range(m, 6 + 1)))


def flips_required_for_confidence(confidence: float, k: int, m: int):
    current_conf = 0
    n = 1
    while current_conf < confidence:
        current_conf = prob_X_atleast_m(n, k, m)
        n += 1
    return n


def total_time_required_for_confidence(flip_time: float, brown_time: float, confidence: float, n: int, m: int):
    return (brown_time / n + flip_time) * flips_required_for_confidence(confidence, n, m)


def times_required_dataframe(flip_time: float, brown_time: float, confidence: float, m: int, top: int):
    ran = range(1, top)

    ks = pd.Series(ran, name="K")
    times = pd.Series(map(lambda k: total_time_required_for_confidence(flip_time, brown_time, confidence, k, m),
                          ran), name="Times")

    return pd.concat([ks, times], 1)
