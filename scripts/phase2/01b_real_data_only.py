#!/usr/bin/env python3
"""
Phase 2 Real Data Integration - Literature Sources Only
Excludes simulated/synthetic data files
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Real literature-extracted files only (verified sources)
REAL_LITERATURE_FILES = [
    'natap2022_extracted_quantitative.csv',
    'pmc9039614_capsid_diversity_extracted.csv',
    'pmc_extracted_batch1.csv',
    'pmc_extracted_batch2.csv',
    'multi_source_batch_2026.csv',
    'resistance_trends_uganda_2025.csv',
    'clinical_trials_2025_extracted.csv',
    'structural_mechanism_2025.csv',
    'assembly_calibrate_2025.csv',
    'mbio_2022_extracted_data.csv',
    'pmc8092519_gcsm_data.csv',
    'pmc8092519_cross_resistance.csv',
    'capella_hiv2_clinical_isolates.csv',
    'uganda_hiv2_quantitative.csv',
    'pmc9600929_structural_extended.csv',
    'pmc9600929_structural_mechanistic_data.csv',
    'backbone_annotated_phenotypes.csv',
    'subtype_annotated_resistance.csv',
    'web_search_extracted_2026.csv',
    'additional_studies_extracted.csv',
    'angola_diversity_data.csv',
    'calibrate_week28_resistance.csv',
    'capella_2year_resistance_data.csv',
    'capsid_diversity_data.csv',
    'clinical_trials_extracted_data.csv',
    'drug_interactions_synergy.csv',
    'global_subtype_distribution.csv',
    'lenacapavir_potency_data.csv',
    'natap_lenacapavir_resistance_2022.csv',
    'natap_review_data.csv',
    'pf74_compensatory_mutations.csv',
    'pharmacokinetics_data.csv',
    'pmc11995365_2026_extracted_data.csv',
    'pmc12077089_2026_extracted_data.csv',
    'pmc12077089_extended_fitness.csv',
    'pmc12077089_full_fitness_data.csv',
    'structural_pk_data.csv',
    'subtype_polymorphism_data.csv',
    'sunlenca_clinical_efficacy.csv',
    'supplementary_mutations_2026.csv',
    'uganda_natural_polymorphisms.csv',
    'uganda_subtype_a1_d_2025.csv'
]

def load_real_data():
    all_data = []
    data_dir = Path('data/raw/papers')

    for fname in REAL_LITERATURE_FILES:
        fpath = data_dir / fname
        if not fpath.exists():
            continue

        try:
            df = pd.read_csv(fpath)
            df = df.loc[:, ~df.columns.duplicated()]
            df['source_file'] = fname
            all_data.append(df)
            logging.info(f"Loaded {fname}: {len(df)} records")
        except Exception as e:
            logging.error(f"Failed {fname}: {e}")

    return pd.concat(all_data, ignore_index=True)

def standardize_and_clean(df):
    # Standardize column names
    col_map = {
        'Fold_Change': 'FC', 'fold_change': 'FC', 'FoldChange': 'FC',
        'mutation': 'Mutation', 'subtype': 'Subtype', 'context': 'Context',
        'quality': 'Quality', 'source': 'Source', 'Paper': 'Source'
    }
    df = df.rename(columns=col_map).copy()
    df = df.loc[:, ~df.columns.duplicated()]

    # Ensure required columns
    for col in ['Source', 'Mutation', 'FC', 'Context', 'Subtype', 'Quality']:
        if col not in df.columns:
            df[col] = np.nan

    # Quality filter
    df = df[df['Quality'] >= 2].copy()

    # Deduplicate
    df = df.drop_duplicates(subset=['Mutation', 'Subtype', 'Source', 'FC'], keep='first')

    # Convert FC to numeric
    df['FC_numeric'] = pd.to_numeric(df['FC'], errors='coerce')
    df['log10_FC'] = np.where(df['FC_numeric'] > 0, np.log10(df['FC_numeric']), np.nan)

    # Flag outliers
    valid_log = df['log10_FC'].dropna()
    if len(valid_log) > 0:
        mean_log, std_log = valid_log.mean(), valid_log.std()
        df['outlier_flag'] = np.abs(df['log10_FC'] - mean_log) > 3 * std_log

    return df

def main():
    logging.info("Loading real literature data only")
    raw_data = load_real_data()
    logging.info(f"Total raw records: {len(raw_data)}")

    clean_data = standardize_and_clean(raw_data)
    logging.info(f"After cleaning: {len(clean_data)} records")

    valid_fc = clean_data['FC_numeric'].notna().sum()
    logging.info(f"Records with valid FC: {valid_fc}")
    logging.info(f"Unique mutations: {clean_data['Mutation'].nunique()}")
    logging.info(f"Unique subtypes: {clean_data['Subtype'].nunique()}")

    # Save
    output_path = 'data/processed/real_literature_integrated.csv'
    clean_data.to_csv(output_path, index=False)
    logging.info(f"Saved to {output_path}")

    return clean_data

if __name__ == '__main__':
    df = main()
