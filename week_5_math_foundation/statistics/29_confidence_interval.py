import numpy as np

data = np.array([70, 72, 75, 78, 80, 82, 85, 88])

mean = np.mean(data)
std = np.std(data, ddof=1)
n = len(data)

se = std / np.sqrt(n)

z = 1.96

margin = z * se

lower = mean - margin
upper = mean + margin

print("Mean:", mean)
print("95% CI:", lower, "to", upper)