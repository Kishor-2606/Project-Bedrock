actual = [50, 60, 70, 80]
predicted = [52, 58, 72, 77]

errors = []

for y, y_hat in zip(actual, predicted):
    errors.append((y - y_hat) ** 2)

mse = sum(errors) / len(errors)

print("MSE:", mse)