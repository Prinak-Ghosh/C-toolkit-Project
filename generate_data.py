"""
Generates a small synthetic dataset of employee records with a manager's
overall rating, for use in train_model.py.

The "true" underlying relationship is deliberately different from the
hand-picked weights used in the original C toolkit (0.5 / 0.3 / 0.2),
so the regression model has something meaningful to recover. Gaussian
noise is added to simulate the imperfect, subjective nature of real
manager ratings.
"""

import numpy as np
import pandas as pd

RNG_SEED = 42
N_EMPLOYEES = 120

# The "true" weights a manager unconsciously applies when rating
# employees overall (unknown to the model - it has to learn these).
TRUE_WEIGHTS = {"productivity": 0.62, "attendance": 0.18, "teamwork": 0.24}
TRUE_BIAS = -8.0
NOISE_STD = 4.0


def generate_dataset(n=N_EMPLOYEES, seed=RNG_SEED):
    rng = np.random.default_rng(seed)

    productivity = rng.uniform(40, 100, n)
    attendance = rng.uniform(50, 100, n)
    teamwork = rng.uniform(40, 100, n)

    true_rating = (
        TRUE_WEIGHTS["productivity"] * productivity
        + TRUE_WEIGHTS["attendance"] * attendance
        + TRUE_WEIGHTS["teamwork"] * teamwork
        + TRUE_BIAS
    )
    noise = rng.normal(0, NOISE_STD, n)
    manager_rating = np.clip(true_rating + noise, 0, 100)

    df = pd.DataFrame({
        "productivity": productivity.round(1),
        "attendance": attendance.round(1),
        "teamwork": teamwork.round(1),
        "manager_rating": manager_rating.round(1),
    })
    return df


if __name__ == "__main__":
    df = generate_dataset()
    df.to_csv("employee_ratings.csv", index=False)
    print(f"Wrote {len(df)} records to employee_ratings.csv")
    print(df.head())
