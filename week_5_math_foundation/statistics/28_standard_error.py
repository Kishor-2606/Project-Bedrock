import numpy as np

data = np.array([10, 12, 15, 18, 20, 22, 25])

sample_std = np.std(data, ddof=1)
n = len(data)

standard_error = sample_std / np.sqrt(n)

print("Sample standard deviation:", sample_std)
print("Standard error:", standard_error)

# for n in [10, 30, 50, 100, 500]:
#     se = 10 / np.sqrt(n)
#     print("n =", n, "SE =", se)