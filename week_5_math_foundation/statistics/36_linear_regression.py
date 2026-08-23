import numpy as np

X = np.array([1, 2, 3, 4, 5])
Y = np.array([2, 4, 5, 8, 10])

m, b = np.polyfit(X, Y, 1)

predictions = m * X + b

print("Slope:", m)
print("Intercept:", b)
print("Predictions:", predictions)