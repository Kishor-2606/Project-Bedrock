data = [10, 12, 13, 14, 15, 16, 18, 100]

Q1 = 12.5
Q3 = 17
IQR = Q3 - Q1

lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR

outliers = []

for x in data:
    if x < lower or x > upper:
        outliers.append(x)

print("Lower bound:", lower)
print("Upper bound:", upper)
print("Outliers:", outliers)