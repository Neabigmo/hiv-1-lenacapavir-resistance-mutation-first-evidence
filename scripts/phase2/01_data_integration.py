#!/usr/bin/env python3
"""
Phase 2 Data Integration Script
Consolidates all extracted CSV files into unified analysis-ready dataset
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'logs/experiments/phase2_integration_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)

def load_all_csvs(data_dir):
    """Load all CSV files from papers directory"""
    csv_files = list(Path(data_dir).glob('*.csv'))
    logging.info(f"Found {len(csv_files)} CSV files")

    all_data = []
    for csv_file in csv_files:
        try:
            df = pd.read_csv(csv_file)
            # Remove duplicate columns if any
            df = df.loc[:, ~df.columns.duplicated()]
            df['source_file'] = csv_file.name
            all_data.append(df)
            logging.info(f"Loaded {csv_file.name}: {len(df)} records")
        except Exception as e:
            logging.error(f"Failed to load {csv_file.name}: {e}")

    return pd.concat(all_data, ignore_index=True)

def standardize_columns(df):
    """Standardize column names and data types"""
    column_mapping = {
        'Fold_Change': 'FC',
        'fold_change': 'FC',
        'FoldChange': 'FC',
        'Value': 'FC',  # Some files use Value for FC
        'mutation': 'Mutation',
        'subtype': 'Subtype',
        'context': 'Context',
        'quality': 'Quality',
        'source': 'Source',
        'Paper': 'Source'
    }

    df = df.rename(columns=column_mapping)

    # Remove duplicate columns after renaming
    df = df.loc[:, ~df.columns.duplicated()]

    required_cols = ['Source', 'Mutation', 'FC', 'Context', 'Subtype', 'Quality']
    for col in required_cols:
        if col not in df.columns:
            df[col] = np.nan

    return df

def clean_data(df):
    """Quality control and cleaning"""
    initial_count = len(df)

    # Filter by quality threshold
    df = df[df['Quality'] >= 2].copy()
    logging.info(f"Quality filter: {initial_count} -> {len(df)} records")

    # Remove duplicates based on key columns
    df = df.drop_duplicates(subset=['Mutation', 'Subtype', 'Source', 'FC'], keep='first')
    logging.info(f"After deduplication: {len(df)} records")

    # Convert FC to numeric
    df['FC_numeric'] = pd.to_numeric(df['FC'], errors='coerce')

    # Calculate log10_FC
    df['log10_FC'] = np.where(df['FC_numeric'] > 0, np.log10(df['FC_numeric']), np.nan)

    # Flag outliers (>3 sigma)
    valid_log = df['log10_FC'].dropna()
    if len(valid_log) > 0:
        mean_log = valid_log.mean()
        std_log = valid_log.std()
        df['outlier_flag'] = np.abs(df['log10_FC'] - mean_log) > 3 * std_log
        logging.info(f"Outliers flagged: {df['outlier_flag'].sum()}")

    return df

def generate_summary_stats(df):
    """Generate summary statistics"""
    stats = {
        'total_records': len(df),
        'unique_mutations': df['Mutation'].nunique(),
        'unique_subtypes': df['Subtype'].nunique(),
        'unique_sources': df['Source'].nunique(),
        'fc_range': (df['FC'].min(), df['FC'].max()),
        'context_distribution': df['Context'].value_counts().to_dict(),
        'subtype_distribution': df['Subtype'].value_counts().to_dict()
    }

    logging.info(f"\n=== Summary Statistics ===")
    logging.info(f"Total records: {stats['total_records']}")
    logging.info(f"Unique mutations: {stats['unique_mutations']}")
    logging.info(f"Unique subtypes: {stats['unique_subtypes']}")
    logging.info(f"FC range: {stats['fc_range']}")

    return stats

def main():
    logging.info("Starting Phase 2 data integration")

    # Load all CSV files
    raw_data = load_all_csvs('data/raw/papers')
    logging.info(f"Total raw records loaded: {len(raw_data)}")

    # Standardize columns
    data = standardize_columns(raw_data)

    # Clean and filter
    clean_data_df = clean_data(data)

    # Generate statistics
    stats = generate_summary_stats(clean_data_df)

    # Save integrated dataset
    output_path = 'data/processed/integrated_500plus.csv'
    clean_data_df.to_csv(output_path, index=False)
    logging.info(f"Saved integrated dataset to {output_path}")

    # Save summary
    summary_path = 'data/processed/integration_summary.txt'
    with open(summary_path, 'w') as f:
        f.write(f"Phase 2 Data Integration Summary\n")
        f.write(f"Generated: {datetime.now()}\n\n")
        for key, value in stats.items():
            f.write(f"{key}: {value}\n")

    logging.info("Integration complete")
    return clean_data_df

if __name__ == '__main__':
    df = main()
