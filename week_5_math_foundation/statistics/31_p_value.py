from scipy import stats

scores = [72, 75, 78, 80, 82, 85]

test = stats.ttest_1samp(
    scores,
    popmean=70
)

print("t-statistic:", test.statistic)
print("p-value:", test.pvalue)

if test.pvalue < 0.05:
    print("Reject H0")
else:
    print("Fail to reject H0")