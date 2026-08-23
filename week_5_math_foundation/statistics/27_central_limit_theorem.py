import numpy as np
import matplotlib.pyplot as plt

population = np.random.exponential(
    scale=2,
    size=10000
)

sample_means = []

for _ in range(5000):
    sample = np.random.choice(
        population,
        size=30
    )

    sample_means.append(np.mean(sample))

plt.hist(sample_means, bins=40)
plt.title("Distribution of Sample Means")
plt.xlabel("Sample Mean")
plt.ylabel("Frequency")
plt.show()