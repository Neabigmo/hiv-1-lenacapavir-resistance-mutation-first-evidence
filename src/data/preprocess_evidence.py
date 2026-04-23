#!/usr/bin/env python3
"""
Data preprocessing pipeline for lenacapavir resistance analysis
Consolidates evidence atlas data into model-ready format
"""

import pandas as pd
import numpy as np
from pathlib import Path

def load_evidence_atlas():
    """Load and consolidate all extracted data"""
    data_dir = Path("data/raw/papers")

    # Load all CSV files
    dfs = []
    for csv_file in data_dir.glob("*.csv"):
        try:
            df = pd.read_csv(csv_file)
            df['source_file'] = csv_file.stem

            # Standardize column names
            if 'Subtype' not in df.columns and 'subtype' in df.columns:
                df['Subtype'] = df['subtype']

            dfs.append(df)
        except Exception as e:
            print(f"Warning: Could not load {csv_file}: {e}")

    # Load interim data
    interim_file = Path("data/interim/evidence_atlas_v2.csv")
    if interim_file.exists():
        df_interim = pd.read_csv(interim_file)
        df_interim['source_file'] = 'evidence_atlas_v2'
        dfs.append(df_interim)

    # Concatenate all data
    if not dfs:
        raise ValueError("No data files found")

    df_all = pd.concat(dfs, ignore_index=True)
    return df_all

def extract_phenotype_data(df):
    """Extract mutation-phenotype associations"""
    # Focus on quantitative resistance measurements
    phenotype_cols = ['Mutation', 'FC', 'Value', 'Context', 'Type']

    df_pheno = df[df['Type'].str.contains('FC|EC50|Kd|Resistance', na=False, case=False)]

    # Parse fold-change values
    df_pheno['FC_numeric'] = pd.to_numeric(df_pheno['FC'], errors='coerce')

    # Extract backbone/subtype information from multiple sources
    df_pheno['Backbone'] = None

    # From Subtype column if exists
    if 'Subtype' in df_pheno.columns:
        df_pheno['Backbone'] = df_pheno['Subtype'].fillna(df_pheno['Backbone'])

    # From Context field
    context_patterns = r'(Subtype_[A-Z0-9]+|CRF\d+_[A-Z]+|Group_[A-Z]|subtype [A-Z]|CRF[0-9]+)'
    df_pheno['Backbone'] = df_pheno['Backbone'].fillna(
        df_pheno['Context'].str.extract(context_patterns, expand=False)
    )

    # From Notes field
    df_pheno['Backbone'] = df_pheno['Backbone'].fillna(
        df_pheno['Notes'].str.extract(context_patterns, expand=False)
    )

    # Clean backbone labels
    df_pheno['Backbone'] = df_pheno['Backbone'].str.replace('subtype ', 'Subtype_', case=False)
    df_pheno['Backbone'] = df_pheno['Backbone'].fillna('Unknown')

    return df_pheno

def extract_fitness_data(df):
    """Extract fitness cost measurements"""
    fitness_keywords = ['infectivity', 'replication', 'fitness', 'impaired']

    df_fitness = df[df['Type'].str.contains('|'.join(fitness_keywords), na=False, case=False)]

    return df_fitness

def extract_clinical_data(df):
    """Extract clinical emergence data"""
    df_clinical = df[df['Context'].str.contains('Clinical|CAPELLA', na=False, case=False)]

    return df_clinical

def main():
    """Main preprocessing pipeline"""
    print("Loading evidence atlas...")
    df = load_evidence_atlas()
    print(f"Loaded {len(df)} total entries")

    # Extract different data types
    df_pheno = extract_phenotype_data(df)
    df_fitness = extract_fitness_data(df)
    df_clinical = extract_clinical_data(df)

    print(f"Phenotype entries: {len(df_pheno)}")
    print(f"Fitness entries: {len(df_fitness)}")
    print(f"Clinical entries: {len(df_clinical)}")

    # Save processed data
    output_dir = Path("data/processed")
    output_dir.mkdir(exist_ok=True)

    df_pheno.to_csv(output_dir / "phenotype_data.csv", index=False)
    df_fitness.to_csv(output_dir / "fitness_data.csv", index=False)
    df_clinical.to_csv(output_dir / "clinical_data.csv", index=False)

    print(f"Saved processed data to {output_dir}")

if __name__ == "__main__":
    main()
