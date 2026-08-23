import numpy as np

data = np.array([10, 11, 12, 13, 100])

mean = np.mean(data)
std = np.std(data)

skewness = np.mean(((data - mean) / std) ** 3)

print("Skewness:", skewness)