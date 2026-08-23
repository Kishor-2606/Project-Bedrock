from scipy import stats

group_a = [70, 72, 75, 78, 80]
group_b = [82, 85, 87, 90, 92]

result = stats.ttest_ind(
    group_a,
    group_b
)

print("t-statistic:", result.statistic)
print("p-value:", result.pvalue)