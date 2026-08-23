students = list(range(1, 101))

population = students

sample = students[::10]

print("Population:", population)
print("Population size:", len(population))

print("Sample:", sample)
print("Sample size:", len(sample))