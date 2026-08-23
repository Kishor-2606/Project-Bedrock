data = [10, 20, 30, 40, 50]

mean = sum(data) / len(data)

variance = sum((x - mean) ** 2 for x in data) / len(data)

std = variance ** 0.5

print("Variance:", variance)
print("Standard deviation:", std)