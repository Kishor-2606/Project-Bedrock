actual = [50, 60, 70, 80]
predicted = [52, 58, 72, 77]

errors = []

for y, y_hat in zip(actual, predicted):
    errors.append(abs(y - y_hat))

mae = sum(errors) / len(errors)

print("MAE:", mae)