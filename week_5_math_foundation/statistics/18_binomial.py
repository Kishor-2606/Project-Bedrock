import math

n = 10
p = 0.05
k = 2

probability = (
    math.comb(n, k)
    * p ** k
    * (1 - p) ** (n - k)
)

print("Probability of exactly 2 successes:", probability)