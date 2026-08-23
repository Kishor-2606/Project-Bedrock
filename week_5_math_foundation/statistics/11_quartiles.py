data = sorted([10, 20, 30, 40, 50, 60, 70, 80])

def percentile(data, p):
    index = (len(data) - 1) * p / 100
    lower = int(index)
    upper = min(lower + 1, len(data))

    weight = index - lower

    return data[lower] + weight * (data[upper] - data[lower])


Q1 = percentile(data, 25)
Q2 = percentile(data, 50)
Q3 = percentile(data, 75)

print("Q1:", Q1)
print("Q2:", Q2)
print("Q3:", Q3)