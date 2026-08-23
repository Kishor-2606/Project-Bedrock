data = [40, 50, 60, 70, 80]

mean = sum(data) / len(data)

variance = sum((x - mean) ** 2 for x in data) / len(data)

std = variance ** 0.5

x = 80

z = (x - mean) / std

print("Mean:", mean)
print("Standard deviation:", std)
print("Z-score:", z)