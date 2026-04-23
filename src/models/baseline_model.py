#!/usr/bin/env python3
"""
Baseline model: Simple linear regression for resistance prediction
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
from pathlib import Path

def load_data():
    """Load processed phenotype data"""
    df = pd.read_csv("data/processed/phenotype_data.csv")
    df = df[df['FC_numeric'].notna()]
    return df

def prepare_features(df):
    """Create simple feature matrix"""
    mutations = pd.get_dummies(df['Mutation'], prefix='mut')
    context = pd.get_dummies(df['Context'], prefix='ctx')
    X = pd.concat([mutations, context], axis=1)
    y = np.log10(df['FC_numeric'] + 1)
    return X, y

def train_baseline(X, y):
    """Train simple linear model"""
    model = LinearRegression()
    model.fit(X, y)
    y_pred = model.predict(X)
    mse = mean_squared_error(y, y_pred)
    r2 = r2_score(y, y_pred)
    return model, mse, r2

def main():
    print("Loading data...")
    df = load_data()
    print(f"Loaded {len(df)} phenotype entries")

    print("Preparing features...")
    X, y = prepare_features(df)
    print(f"Feature matrix: {X.shape}")

    print("Training baseline model...")
    model, mse, r2 = train_baseline(X, y)

    print(f"\nBaseline Results:")
    print(f"MSE: {mse:.4f}")
    print(f"R2: {r2:.4f}")

    output_dir = Path("results/checkpoints")
    output_dir.mkdir(parents=True, exist_ok=True)

    import joblib
    joblib.dump(model, output_dir / "baseline_model.pkl")
    print(f"Saved model to {output_dir}")

if __name__ == "__main__":
    main()
