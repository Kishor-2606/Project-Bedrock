data = [1, 2, 2, 3, 3, 3, 4, 4, 5]

frequency = {}

for x in data:
    frequency[x] = frequency.get(x, 0) + 1

total = len(data)

for value, count in frequency.items():
    relative_frequency = count / total

    print(
        value,
        "Frequency:", count,
        "Relative:", relative_frequency
    )