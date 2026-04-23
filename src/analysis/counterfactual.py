#!/usr/bin/env python3
"""
Counterfactual prediction: predict resistance in different subtypes
"""

import pandas as pd
import numpy as np
import joblib
from pathlib import Path

def main():
    print("Implementing counterfactual prediction...")

    # Load trained model
    model = joblib.load('results/checkpoints/hierarchical_model.pkl')

    # Load data
    df = pd.read_csv('data/curated/phenotype_unified.csv')

    # Example: predict M66I in different subtypes
    mutation = 'M66I'
    subtypes = ['Subtype_B', 'Subtype_C', 'Subtype_A1', 'CRF01_AE']

    print(f"\nCounterfactual prediction for {mutation}:")
    print(f"{'Subtype':<15} {'Predicted LogFC':<20} {'Predicted FC':<15}")
    print("-" * 50)

    for subtype in subtypes:
        # Get main effect
        main_effect = model.main_effects.get(f'Mutation[T.{mutation}]', 0)

        # Get backbone effect
        backbone_effect = model.backbone_effects.get(subtype, {}).get('Group', 0)

        # Total prediction
        predicted_logfc = main_effect + backbone_effect
        predicted_fc = 10 ** predicted_logfc

        print(f"{subtype:<15} {predicted_logfc:<20.3f} {predicted_fc:<15.1f}")

    # Save predictions
    predictions = []
    for mut in ['M66I', 'Q67H', 'N74D', 'Q67H+K70R']:
        for subtype in subtypes:
            main = model.main_effects.get(f'Mutation[T.{mut}]', 0)
            backbone = model.backbone_effects.get(subtype, {}).get('Group', 0)
            pred_logfc = main + backbone
            pred_fc = 10 ** pred_logfc

            predictions.append({
                'Mutation': mut,
                'Subtype': subtype,
                'Predicted_LogFC': pred_logfc,
                'Predicted_FC': pred_fc
            })

    pred_df = pd.DataFrame(predictions)
    output_dir = Path('results')
    pred_df.to_csv(output_dir / 'counterfactual_predictions.csv', index=False)

    print(f"\nSaved predictions to {output_dir}")

if __name__ == '__main__':
    main()
