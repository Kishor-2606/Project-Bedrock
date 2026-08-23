import math

lam = 3
k = 2

probability = (
    math.exp(-lam)
    * lam ** k
    / math.factorial(k)
)

print("Probability:", probability)