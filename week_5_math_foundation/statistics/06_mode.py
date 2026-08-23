data = [10, 20, 20, 30, 40, 20, 50]

frequency = {}

for value in data:
    frequency[value] = frequency.get(value, 0) + 1

mode = max(frequency, key=frequency.get)

print("Mode:", mode)
print("Frequency:", frequency[mode])