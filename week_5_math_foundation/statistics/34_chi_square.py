from scipy.stats import chi2_contingency

table = [
    [30, 20],
    [10, 40]
]

chi2, p, dof, expected = chi2_contingency(table)

print("Chi-square:", chi2)
print("p-value:", p)
print("Degrees of freedom:", dof)
print("Expected:", expected)