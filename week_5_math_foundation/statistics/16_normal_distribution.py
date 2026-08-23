import numpy as np
import matplotlib.pyplot as plt

data = np.random.normal(
    loc=50,
    scale=10,
    size=1000
)

plt.hist(data, bins=30)
plt.xlabel("Value")
plt.ylabel("Frequency")
plt.title("Normal Distribution")
plt.show()