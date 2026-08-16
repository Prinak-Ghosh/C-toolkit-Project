"""
Learns employee-scoring weights from data via linear regression, instead
of using the hand-picked weights (0.5 / 0.3 / 0.2) from the original C
toolkit. See README.md for the full writeup.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error

FEATURES = ["productivity", "attendance", "teamwork"]
TARGET = "manager_rating"

# The weights hard-coded in the original C toolkit, for comparison.
HANDPICKED_WEIGHTS = {"productivity": 0.5, "attendance": 0.3, "teamwork": 0.2}


def load_data(path="employee_ratings.csv"):
    return pd.read_csv(path)


def train(df):
    X = df[FEATURES].values
    y = df[TARGET].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42
    )

    model = LinearRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)

    return model, X_test, y_test, y_pred, r2, mae


def compare_weights(model):
    # Normalize learned coefficients to sum to 1, so they're directly
    # comparable to the hand-picked weights (which already sum to 1).
    raw = dict(zip(FEATURES, model.coef_))
    total = sum(raw.values())
    normalized = {k: v / total for k, v in raw.items()}

    print("\nFeature weight comparison (normalized to sum to 1):")
    print(f"{'Feature':<14}{'Hand-picked':>12}{'Learned':>12}")
    for f in FEATURES:
        print(f"{f:<14}{HANDPICKED_WEIGHTS[f]:>12.2f}{normalized[f]:>12.2f}")

    return normalized


def plot_results(y_test, y_pred, normalized_weights, outfile="model_results.png"):
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

    # Predicted vs actual
    axes[0].scatter(y_test, y_pred, alpha=0.7, edgecolor="k")
    lims = [min(y_test.min(), y_pred.min()), max(y_test.max(), y_pred.max())]
    axes[0].plot(lims, lims, "r--", label="Perfect prediction")
    axes[0].set_xlabel("Actual manager rating")
    axes[0].set_ylabel("Predicted rating")
    axes[0].set_title("Predicted vs. Actual Ratings")
    axes[0].legend()
    axes[0].grid(alpha=0.3)

    # Hand-picked vs learned weights
    x = np.arange(len(FEATURES))
    width = 0.35
    axes[1].bar(x - width / 2, [HANDPICKED_WEIGHTS[f] for f in FEATURES],
                width, label="Hand-picked (original)")
    axes[1].bar(x + width / 2, [normalized_weights[f] for f in FEATURES],
                width, label="Learned (regression)")
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(FEATURES)
    axes[1].set_ylabel("Weight")
    axes[1].set_title("Hand-Picked vs. Learned Weights")
    axes[1].legend()
    axes[1].grid(alpha=0.3, axis="y")

    plt.tight_layout()
    plt.savefig(outfile, dpi=150)
    print(f"\nPlot saved to {outfile}")


def score_new_employees(model):
    new_employees = pd.DataFrame([
        {"productivity": 92, "attendance": 75, "teamwork": 80},
        {"productivity": 60, "attendance": 95, "teamwork": 88},
        {"productivity": 78, "attendance": 82, "teamwork": 70},
    ])
    predicted = model.predict(new_employees[FEATURES].values)
    new_employees["predicted_rating"] = predicted.round(1)
    print("\nScoring new employees with the trained model:")
    print(new_employees.to_string(index=False))


def main():
    df = load_data()
    model, X_test, y_test, y_pred, r2, mae = train(df)

    print(f"Model performance on held-out test set:")
    print(f"  R^2: {r2:.3f}")
    print(f"  MAE: {mae:.2f} rating points")

    normalized_weights = compare_weights(model)
    plot_results(y_test, y_pred, normalized_weights)
    score_new_employees(model)


if __name__ == "__main__":
    main()
