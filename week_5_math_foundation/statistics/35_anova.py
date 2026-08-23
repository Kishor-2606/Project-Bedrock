from scipy.stats import f_oneway

model_a = [80, 82, 81, 79, 83]
model_b = [85, 87, 86, 88, 84]
model_c = [90, 91, 89, 92, 90]

result = f_oneway(
    model_a,
    model_b,
    model_c
)

print("F-statistic:", result.statistic)
print("p-value:", result.pvalue)