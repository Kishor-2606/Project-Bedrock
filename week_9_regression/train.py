import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# 1. LOAD DATA
# ============================================================

df = pd.read_csv("used_cars.csv")

print("Shape:", df.shape)
print(df.head())
print(df.info())
print(df.isnull().sum())


# ============================================================
# 2. CLEAN DATA
# ============================================================

# Price: "$38,005" -> 38005
df["price"] = (
    df["price"]
    .str.replace("$", "", regex=False)
    .str.replace(",", "", regex=False)
    .astype(float)
)

# Mileage: "34,742 mi." -> 34742
df["milage"] = (
    df["milage"]
    .str.replace(" mi.", "", regex=False)
    .str.replace(",", "", regex=False)
    .astype(float)
)


# ============================================================
# 3. FEATURE ENGINEERING
# ============================================================

# Extract horsepower from engine
df["horsepower"] = (
    df["engine"]
    .str.extract(r"([\d,.]+)HP", expand=False)
    .str.replace(",", "", regex=False)
    .astype(float)
)

# Extract engine size
df["engine_liters"] = (
    df["engine"]
    .str.extract(r"([\d,.]+)L", expand=False)
    .astype(float)
)


# ============================================================
# 4. SELECT FEATURES
# ============================================================

features = [
    "model_year",
    "milage",
    "horsepower",
    "engine_liters"
]

target = "price"

data = df[features + [target]].copy()

print("\nSelected data:")
print(data.head())


# ============================================================
# 5. HANDLE MISSING VALUES
# ============================================================

for column in features:
    data[column] = data[column].fillna(data[column].median())

print("\nMissing values:")
print(data.isnull().sum())


# ============================================================
# 6. X AND y
# ============================================================

X = data[features].values
y = data[target].values

print("\nX shape:", X.shape)
print("y shape:", y.shape)


# ============================================================
# 7. TRAIN / TEST SPLIT
# ============================================================

np.random.seed(42)

indices = np.arange(len(X))
np.random.shuffle(indices)

split = int(0.8 * len(X))

train_indices = indices[:split]
test_indices = indices[split:]

X_train = X[train_indices]
X_test = X[test_indices]

y_train = y[train_indices]
y_test = y[test_indices]

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))


# ============================================================
# 8. STANDARDIZATION
# ============================================================

# IMPORTANT:
# Calculate mean/std ONLY from training data.

mean = X_train.mean(axis=0)
std = X_train.std(axis=0)

X_train = (X_train - mean) / std
X_test = (X_test - mean) / std


# ============================================================
# 9. LINEAR REGRESSION FROM SCRATCH
# ============================================================

class LinearRegression:

    def __init__(self, learning_rate=0.01, epochs=5000):

        self.learning_rate = learning_rate
        self.epochs = epochs

        self.weights = None
        self.bias = 0

        self.loss_history = []


    def fit(self, X, y):

        n_samples, n_features = X.shape

        # Initial parameters
        self.weights = np.zeros(n_features)
        self.bias = 0


        # Gradient Descent
        for epoch in range(self.epochs):

            # -------------------------
            # Prediction
            # -------------------------

            y_pred = X @ self.weights + self.bias


            # -------------------------
            # Error
            # -------------------------

            error = y_pred - y


            # -------------------------
            # MSE
            # -------------------------

            mse = np.mean(error ** 2)

            self.loss_history.append(mse)


            # -------------------------
            # Gradients
            # -------------------------

            dw = (2 / n_samples) * (X.T @ error)

            db = (2 / n_samples) * np.sum(error)


            # -------------------------
            # Update parameters
            # -------------------------

            self.weights -= self.learning_rate * dw

            self.bias -= self.learning_rate * db


            # Print progress
            if epoch % 500 == 0:
                print(
                    f"Epoch {epoch} | MSE: {mse:.2f}"
                )


    def predict(self, X):

        return X @ self.weights + self.bias


# ============================================================
# 10. TRAIN MODEL
# ============================================================

model = LinearRegression(
    learning_rate=0.01,
    epochs=5000
)

model.fit(X_train, y_train)


# ============================================================
# 11. PREDICTIONS
# ============================================================

y_pred = model.predict(X_test)

print("\nFirst 10 predictions:")

for actual, predicted in zip(y_test[:10], y_pred[:10]):

    print(
        f"Actual: ${actual:,.0f} | "
        f"Predicted: ${predicted:,.0f}"
    )


# ============================================================
# 12. MANUAL EVALUATION METRICS
# ============================================================

errors = y_test - y_pred


# MAE
mae = np.mean(np.abs(errors))


# MSE
mse = np.mean(errors ** 2)


# RMSE
rmse = np.sqrt(mse)


# R²
ss_res = np.sum((y_test - y_pred) ** 2)

ss_tot = np.sum(
    (y_test - np.mean(y_test)) ** 2
)

r2 = 1 - (ss_res / ss_tot)


print("\n==============================")
print("MODEL PERFORMANCE")
print("==============================")

print(f"MAE  : ${mae:,.2f}")
print(f"MSE  : {mse:,.2f}")
print(f"RMSE : ${rmse:,.2f}")
print(f"R²   : {r2:.4f}")


# ============================================================
# 13. MODEL PARAMETERS
# ============================================================

print("\n==============================")
print("LEARNED PARAMETERS")
print("==============================")

for feature, weight in zip(features, model.weights):

    print(
        f"{feature:15} : {weight:.4f}"
    )

print(f"bias            : {model.bias:.4f}")


# ============================================================
# 14. LOSS CURVE
# ============================================================

plt.figure(figsize=(8, 5))

plt.plot(model.loss_history)

plt.xlabel("Epoch")
plt.ylabel("MSE")
plt.title("Gradient Descent Loss")

plt.show()


# ============================================================
# 15. ACTUAL VS PREDICTED
# ============================================================

plt.figure(figsize=(8, 6))

plt.scatter(
    y_test,
    y_pred,
    alpha=0.6
)

# Perfect prediction line
minimum = min(y_test.min(), y_pred.min())
maximum = max(y_test.max(), y_pred.max())

plt.plot(
    [minimum, maximum],
    [minimum, maximum]
)

plt.xlabel("Actual Price")
plt.ylabel("Predicted Price")

plt.title("Actual vs Predicted Car Prices")

plt.show()