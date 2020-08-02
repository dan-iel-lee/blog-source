import math
from typing import List

# binomial(total number, probability, number of successes)
def binomial(n: int, p: float, k: int):
    return math.comb(n, k) * math.pow(p, k) * math.pow(1 - p, n - k)

# creates a dp table for expected value when there are i lanes and j people left
def expected_carts_table(N: int, L: int):
    # dp table, L x N
    dp = [[math.inf for j in range(0, N + 1)] for i in range(0, L + 1)]

    # initialize base case
    # number of people in the last lane must be the number of people left
    dp[1] = [j for j in range(0, N + 1)]
    
    # loop from low L (N) to high L (N)
    for i in range(2, L + 1):
        for j in range(0, N + 1):
            p = 1 / i
            v = [binomial(j, p, k) * min(k, dp[i - 1][j - k]) for k in range(0, j + 1)]
            dp[i][j] = sum(v)
    
    return dp



def bin_exp_mean_dev(n: int):
    half = math.floor(n/2) + 1
    return 1/math.pow(2,n) * half * math.comb(n, half)

EPSILON = 10 ** -12
# creates a dp table for expected number of lanes checked given the carts table from before
def expected_lanes_table(carts_table: List[List[float]]):
    L = len(carts_table) - 1
    N = len(carts_table[0]) - 1
    lanes = [[math.inf for j in range(0, N + 1)] for i in range(0, L + 1)] # initialize array
    lanes[1] = [1 for i in range(0, N + 1)] # initialize base case: 1 if we're in the last lane

    # loop from low L (N) to high L (N)
    for i in range(2, L + 1):
        for j in range(0, N + 1):
            p = 1 / i
            # terms in the sum for E[W]
            v = [binomial(j, p, k) * (1 + (0 if k <= carts_table[i-1][j-k] + EPSILON else lanes[i - 1][j - k])) for k in range(0, j + 1)]
            lanes[i][j] = sum(v)

    return lanes
