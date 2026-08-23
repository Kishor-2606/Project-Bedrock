import numpy as np

actual = np.array([50, 60, 70, 80])
predicted = np.array([52, 58, 72, 77])

ss_res = np.sum((actual - predicted) ** 2)

ss_total = np.sum(
    (actual - np.mean(actual)) ** 2
)

r2 = 1 - (ss_res / ss_total)

print("R²:", r2)