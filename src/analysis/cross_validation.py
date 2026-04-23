#!/usr/bin/env python3
"""
Cross-validation for hierarchical model
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import LeaveOneOut
from statsmodels.formula.api import mixedlm

def main():
    print("Running leave-one-out cross-validation...")

    # Load data
    df = pd.read_csv('data/curated/phenotype_unified.csv')
    df['Backbone'] = df['Subtype'].fillna('Unknown')
    df['LogFC'] = np.log10(df['FC_numeric'] + 1)

    # Filter valid data
    df_model = df[(df['Backbone'] != 'Unknown') &
                  (df['FC_numeric'].notna())].copy()
    df_model = df_model.reset_index(drop=True)

    print(f"Total samples: {len(df_model)}")

    # Leave-one-out CV
    loo = LeaveOneOut()
    predictions = []
    actuals = []

    for train_idx, test_idx in loo.split(df_model):
        train = df_model.iloc[train_idx]
        test = df_model.iloc[test_idx]

        try:
            # Train model
            formula = "LogFC ~ Mutation"
            model = mixedlm(formula, train, groups=train["Backbone"])
            result = model.fit(disp=False)

            # Predict
            # Use intercept + mutation effect
            test_mut = test['Mutation'].values[0]
            pred = result.fe_params.get('Intercept', 0)
            pred += result.fe_params.get(f'Mutation[T.{test_mut}]', 0)

            predictions.append(pred)
            actuals.append(test['LogFC'].values[0])

        except Exception as e:
            print(f"Skipped sample {test_idx}: {e}")
            continue

    # Calculate metrics
    predictions = np.array(predictions)
    actuals = np.array(actuals)

    rmse = np.sqrt(np.mean((predictions - actuals) ** 2))
    mae = np.mean(np.abs(predictions - actuals))
    r2 = 1 - np.sum((actuals - predictions) ** 2) / np.sum((actuals - np.mean(actuals)) ** 2)

    print(f"\nCross-validation results (n={len(predictions)}):")
    print(f"RMSE: {rmse:.3f}")
    print(f"MAE: {mae:.3f}")
    print(f"R²: {r2:.3f}")

    # Save results
    results_df = pd.DataFrame({
        'Actual_LogFC': actuals,
        'Predicted_LogFC': predictions,
        'Error': actuals - predictions
    })
    results_df.to_csv('results/cv_results.csv', index=False)
    print(f"\nSaved to results/cv_results.csv")

if __name__ == '__main__':
    main()
