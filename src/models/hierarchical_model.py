#!/usr/bin/env python3
"""
Hierarchical backbone-aware model for lenacapavir resistance
Decomposes effects into: main + backbone interaction + fitness constraint
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import statsmodels.api as sm
from statsmodels.formula.api import mixedlm
from pathlib import Path

class BackboneAwareModel:
    """
    Hierarchical model: Y_ij = mu + alpha_i + beta_j + gamma_ij + epsilon

    Y_ij: phenotype (log FC) for mutation i in backbone j
    mu: global mean
    alpha_i: main effect of mutation i (cross-backbone)
    beta_j: backbone effect
    gamma_ij: mutation-backbone interaction
    epsilon: error
    """

    def __init__(self):
        self.main_effects = {}
        self.backbone_effects = {}
        self.interactions = {}

    def fit(self, df):
        """
        Fit hierarchical model using mixed effects

        Args:
            df: DataFrame with columns [Mutation, Backbone, LogFC, Fitness]
        """
        # Mixed effects model: mutation as fixed, backbone as random
        formula = "LogFC ~ Mutation"
        model = mixedlm(formula, df, groups=df["Backbone"])
        result = model.fit()

        # Extract main effects (fixed effects)
        self.main_effects = result.fe_params.to_dict()

        # Extract backbone effects (random effects)
        self.backbone_effects = result.random_effects

        return result

    def decompose_effects(self, mutation, backbone):
        """
        Decompose total effect into components

        Returns:
            dict with main_effect, backbone_effect, interaction
        """
        main = self.main_effects.get(f"Mutation[T.{mutation}]", 0)
        backbone_eff = self.backbone_effects.get(backbone, {}).get('Group', 0)

        # Interaction estimated as residual
        total = main + backbone_eff

        return {
            'main_effect': main,
            'backbone_effect': backbone_eff,
            'total_effect': total
        }

def prepare_hierarchical_data():
    """Load and prepare data for hierarchical modeling"""
    # Load unified phenotype data
    df_pheno = pd.read_csv("data/curated/phenotype_unified.csv")

    # Use Subtype column as backbone
    df_pheno['Backbone'] = df_pheno['Subtype'].fillna('Unknown')

    # Log-transform FC
    df_pheno['LogFC'] = np.log10(df_pheno['FC_numeric'] + 1)

    # Load fitness data
    df_fitness = pd.read_csv("data/curated/fitness_unified.csv")

    return df_pheno, df_fitness

def main():
    print("Preparing hierarchical data...")
    df_pheno, df_fitness = prepare_hierarchical_data()

    print(f"Phenotype entries: {len(df_pheno)}")
    print(f"Unique mutations: {df_pheno['Mutation'].nunique()}")
    print(f"Unique backbones: {df_pheno['Backbone'].nunique()}")

    # Filter for mutations with backbone info and valid FC
    df_model = df_pheno[(df_pheno['Backbone'] != 'Unknown') &
                        (df_pheno['FC_numeric'].notna())].copy()

    # Reset index to avoid indexing issues
    df_model = df_model.reset_index(drop=True)

    if len(df_model) < 3:
        print("Warning: Insufficient data for hierarchical modeling")
        print("Need more mutation-backbone combinations")
        return

    print(f"\nFitting backbone-aware model on {len(df_model)} entries...")
    model = BackboneAwareModel()
    result = model.fit(df_model)

    print("\nModel Summary:")
    print(result.summary())

    # Save model
    output_dir = Path("results/checkpoints")
    output_dir.mkdir(parents=True, exist_ok=True)

    import joblib
    joblib.dump(model, output_dir / "hierarchical_model.pkl")
    print(f"\nSaved model to {output_dir}")

if __name__ == "__main__":
    main()
