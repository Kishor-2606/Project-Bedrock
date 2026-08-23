import matplotlib.pyplot as plt

data = [10, 12, 15, 17, 18, 20, 21, 22, 25, 30]

plt.hist(data, bins=5)
plt.xlabel("Value")
plt.ylabel("Frequency")
plt.title("Histogram")
plt.show()