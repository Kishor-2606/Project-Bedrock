import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("students.csv")

print("Shape:", df.shape)

print("\nStatistics:")
print(df.describe())

print("\nMedian:")
print(df.median(numeric_only=True))

print("\nCorrelation:")
print(df.corr(numeric_only=True))

print("\nQuantiles:")
print(df.quantile(
    [0.25, 0.50, 0.75],
    numeric_only=True
))

plt.hist(df["Final_Marks"], bins=20)
plt.xlabel("Final Marks")
plt.ylabel("Frequency")
plt.title("Final Marks Distribution")
plt.show()

plt.scatter(
    df["Study_Hours"],
    df["Final_Marks"]
)

plt.xlabel("Study Hours")
plt.ylabel("Final Marks")
plt.title("Study Hours vs Final Marks")
plt.show()