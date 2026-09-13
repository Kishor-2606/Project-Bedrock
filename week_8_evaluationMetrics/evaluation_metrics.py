from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)
import numpy as np


# ==========================================
# 1. REGRESSION EVALUATION
# ==========================================

actual = [100, 200, 300, 400, 500]
predicted = [110, 190, 310, 380, 520]

mae = mean_absolute_error(actual, predicted)
mse = mean_squared_error(actual, predicted)
rmse = np.sqrt(mse)
r2 = r2_score(actual, predicted)

print("REGRESSION METRICS")
print("------------------")
print("MAE :", mae)
print("MSE :", mse)
print("RMSE:", rmse)
print("R²  :", r2)


# ==========================================
# 2. CLASSIFICATION EVALUATION
# ==========================================

actual = [1, 1, 1, 0, 0, 0, 1, 0]
predicted = [1, 1, 0, 0, 0, 1, 1, 0]

accuracy = accuracy_score(actual, predicted)
precision = precision_score(actual, predicted)
recall = recall_score(actual, predicted)
f1 = f1_score(actual, predicted)
matrix = confusion_matrix(actual, predicted)

print("\nCLASSIFICATION METRICS")
print("----------------------")
print("Accuracy :", accuracy)
print("Precision:", precision)
print("Recall   :", recall)
print("F1 Score :", f1)

print("\nConfusion Matrix:")
print(matrix)


# ==========================================
# 3. TRAIN / TEST SPLIT
# ==========================================

X = np.array([[1], [2], [3], [4], [5], [6], [7], [8]])
y = np.array([10, 20, 30, 40, 50, 60, 70, 80])

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.25,
    random_state=42
)

model = LinearRegression()

model.fit(X_train, y_train)

predictions = model.predict(X_test)

print("\nTRAIN / TEST EVALUATION")
print("-----------------------")
print("Actual     :", y_test)
print("Predictions:", predictions)
print("MAE        :", mean_absolute_error(y_test, predictions))
print("R²         :", r2_score(y_test, predictions))


# ==========================================
# 4. CROSS VALIDATION
# ==========================================

scores = cross_val_score(
    model,
    X,
    y,
    cv=5,
    scoring="r2"
)

print("\nCROSS VALIDATION")
print("----------------")
print("Scores:", scores)
print("Average R²:", scores.mean())