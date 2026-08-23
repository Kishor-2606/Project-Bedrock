import numpy as np
ice_cream_sales = [10, 20, 30, 40, 50]
drowning_cases = [5, 10, 15, 20, 25]

correlation = np.corrcoef(
    ice_cream_sales,
    drowning_cases
)[0, 1]

print("Correlation:", correlation)

print(
    "Correlation does not prove that "
    "ice cream causes drowning."
)