#!/usr/bin/env python3
"""
Simplified cross-validation using simple linear model
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import LeaveOneOut
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder

def main():
    print("Running simplified cross-validation...")

    # Load data
    df = pd.read_csv('data/curated/phenotype_unified.csv')
    df = df[df['FC_numeric'].notna()].copy()
    df['LogFC'] = np.log10(df['FC_numeric'] + 1)

    # Encode mutations
    le = LabelEncoder()
    df['Mutation_encoded'] = le.fit_transform(df['Mutation'])

    X = df[['Mutation_encoded']].values
    y = df['LogFC'].values

    # LOO CV
    loo = LeaveOneOut()
    predictions = []
    actuals = []

    for train_idx, test_idx in loo.split(X):
        X_train, X_test = X[train_idx], X[test_idx]
        y_train, y_test = y[train_idx], y[test_idx]

        model = LinearRegression()
        model.fit(X_train, y_train)
        pred = model.predict(X_test)[0]

        predictions.append(pred)
        actuals.append(y_test[0])

    predictions = np.array(predictions)
    actuals = np.array(actuals)

    # Metrics
    rmse = np.sqrt(np.mean((predictions - actuals) ** 2))
    mae = np.mean(np.abs(predictions - actuals))
    r2 = 1 - np.sum((actuals - predictions) ** 2) / np.sum((actuals - np.mean(actuals)) ** 2)

    print(f"\nResults (n={len(predictions)}):")
    print(f"RMSE: {rmse:.3f}")
    print(f"MAE: {mae:.3f}")
    print(f"R²: {r2:.3f}")

    # Save
    pd.DataFrame({
        'Actual': actuals,
        'Predicted': predictions,
        'Error': actuals - predictions
    }).to_csv('results/cv_results.csv', index=False)

    print("Saved to results/cv_results.csv")

if __name__ == '__main__':
    main()
