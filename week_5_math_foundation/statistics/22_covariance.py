import numpy as np

X = np.array([1, 2, 3, 4, 5])
Y = np.array([2, 4, 6, 8, 10])

covariance = np.cov(X, Y)[0, 1]

print("Covariance:", covariance)