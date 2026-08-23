data = sorted([10, 20, 30, 40, 50, 60, 70, 80])

def percentile(data, p):
    index = (len(data) - 1) * p / 100
    lower = int(index)
    upper = lower + 1

    if upper >= len(data):
        return data[lower]

    weight = index - lower

    return data[lower] + weight * (data[upper] - data[lower])


print("25th percentile:", percentile(data, 25))
print("50th percentile:", percentile(data, 50))
print("75th percentile:", percentile(data, 75))