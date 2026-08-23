actual = [50, 60, 70, 80]
predicted = [52, 58, 72, 77]

residuals = []

for y, y_hat in zip(actual, predicted):
    residuals.append(y - y_hat)

print("Residuals:", residuals)