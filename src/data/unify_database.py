#!/usr/bin/env python3
"""
Unify 31 CSV files into standardized curated database
"""

import pandas as pd
import numpy as np
import glob
from pathlib import Path

def standardize_columns(df, source_file):
    """Standardize column names across different CSV formats"""

    standard = pd.DataFrame()

    # Mutation
    if 'Mutation' in df.columns:
        standard['Mutation'] = df['Mutation']
    elif 'mutation' in df.columns:
        standard['Mutation'] = df['mutation']
    else:
        standard['Mutation'] = None

    # FC_numeric
    if 'FC' in df.columns:
        standard['FC_numeric'] = pd.to_numeric(df['FC'], errors='coerce')
    elif 'Value' in df.columns and 'Type' in df.columns:
        fc_mask = df['Type'].str.contains('FC', na=False)
        standard['FC_numeric'] = pd.to_numeric(df.loc[fc_mask, 'Value'], errors='coerce')
    else:
        standard['FC_numeric'] = None

    # Subtype
    if 'Subtype' in df.columns:
        standard['Subtype'] = df['Subtype']
    else:
        standard['Subtype'] = None

    # Context
    if 'Context' in df.columns:
        standard['Context'] = df['Context']
    elif 'context' in df.columns:
        standard['Context'] = df['context']
    else:
        standard['Context'] = None

    # Source_PMID
    if 'Source' in df.columns:
        standard['Source_PMID'] = df['Source']
    elif 'source' in df.columns:
        standard['Source_PMID'] = df['source']
    else:
        standard['Source_PMID'] = Path(source_file).stem

    # Infectivity_WT (fitness)
    if 'Infectivity_WT' in df.columns:
        standard['Fitness_WT_pct'] = df['Infectivity_WT']
    elif 'Value' in df.columns and 'Type' in df.columns:
        fit_mask = df['Type'].str.contains('Infectivity', na=False)
        standard['Fitness_WT_pct'] = df.loc[fit_mask, 'Value']
    else:
        standard['Fitness_WT_pct'] = None

    # Notes
    if 'Notes' in df.columns:
        standard['Notes'] = df['Notes']
    else:
        standard['Notes'] = None

    # Quality score (assign based on source)
    standard['Quality_score'] = assign_quality(Path(source_file).stem)

    return standard

def assign_quality(source_stem):
    """Assign quality score based on source"""
    five_star = ['pmc9600929', 'pmc12077089', 'capella', 'uganda', 'jac2025']
    four_star = ['natap', 'pmc8092519', 'calibrate', 'pmc9039614']

    if any(s in source_stem.lower() for s in five_star):
        return 5
    elif any(s in source_stem.lower() for s in four_star):
        return 4
    else:
        return 3

def main():
    print("Unifying 31 CSV files...")

    files = glob.glob('data/raw/papers/*.csv')
    print(f"Found {len(files)} files")

    all_data = []

    for f in files:
        try:
            df = pd.read_csv(f)
            standardized = standardize_columns(df, f)
            all_data.append(standardized)
        except Exception as e:
            print(f"Error processing {f}: {e}")

    unified = pd.concat(all_data, ignore_index=True)

    # Remove rows with no mutation name
    unified = unified[unified['Mutation'].notna()]

    # Save unified database
    output_dir = Path('data/curated')
    output_dir.mkdir(parents=True, exist_ok=True)

    unified.to_csv(output_dir / 'unified_database.csv', index=False)

    # Create phenotype subset (with FC)
    phenotype = unified[unified['FC_numeric'].notna()].copy()
    phenotype.to_csv(output_dir / 'phenotype_unified.csv', index=False)

    # Create fitness subset
    fitness = unified[unified['Fitness_WT_pct'].notna()].copy()
    fitness.to_csv(output_dir / 'fitness_unified.csv', index=False)

    # Statistics
    print(f"\nUnified database: {len(unified)} entries")
    print(f"Phenotype (FC): {len(phenotype)} entries")
    print(f"Fitness: {len(fitness)} entries")
    print(f"Unique mutations: {unified['Mutation'].nunique()}")
    print(f"Subtypes: {unified['Subtype'].nunique()}")
    print(f"Quality 5-star: {(unified['Quality_score']==5).sum()}")
    print(f"Quality 4-star: {(unified['Quality_score']==4).sum()}")

    # Create metadata
    metadata = pd.DataFrame({
        'Source_PMID': unified['Source_PMID'].unique(),
        'Entry_count': [unified[unified['Source_PMID']==s].shape[0]
                       for s in unified['Source_PMID'].unique()]
    })
    metadata.to_csv(output_dir / 'metadata.csv', index=False)

    print(f"\nSaved to {output_dir}/")

if __name__ == '__main__':
    main()
