data = [10, 20, 30, 40, 50]

mean = sum(data) / len(data)

squared_deviations = []

for x in data:
    squared_deviations.append((x - mean) ** 2)

population_variance = sum(squared_deviations) / len(data)

print("Population variance:", population_variance)