#!/usr/bin/env python3
"""
Create visualization for hierarchical model results
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

def main():
    print("Creating visualizations...")

    # Load data
    df = pd.read_csv('data/curated/phenotype_unified.csv')
    df = df[df['FC_numeric'].notna()].copy()
    df['LogFC'] = np.log10(df['FC_numeric'] + 1)

    # Create figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Plot 1: FC distribution
    ax1 = axes[0, 0]
    ax1.hist(df['LogFC'], bins=20, edgecolor='black', alpha=0.7)
    ax1.set_xlabel('Log10(Fold-Change)', fontsize=11)
    ax1.set_ylabel('Count', fontsize=11)
    ax1.set_title('Resistance Distribution', fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3)

    # Plot 2: Top mutations
    ax2 = axes[0, 1]
    top_muts = df.nlargest(15, 'FC_numeric')[['Mutation', 'FC_numeric']]
    ax2.barh(range(len(top_muts)), top_muts['FC_numeric'], color='steelblue')
    ax2.set_yticks(range(len(top_muts)))
    ax2.set_yticklabels(top_muts['Mutation'], fontsize=9)
    ax2.set_xlabel('Fold-Change', fontsize=11)
    ax2.set_title('Top 15 Resistant Mutations', fontsize=12, fontweight='bold')
    ax2.invert_yaxis()
    ax2.grid(True, alpha=0.3, axis='x')

    # Plot 3: Subtype distribution
    ax3 = axes[1, 0]
    subtype_counts = df['Subtype'].value_counts().head(10)
    ax3.bar(range(len(subtype_counts)), subtype_counts.values, color='coral')
    ax3.set_xticks(range(len(subtype_counts)))
    ax3.set_xticklabels(subtype_counts.index, rotation=45, ha='right', fontsize=9)
    ax3.set_ylabel('Count', fontsize=11)
    ax3.set_title('Top 10 Subtypes', fontsize=12, fontweight='bold')
    ax3.grid(True, alpha=0.3, axis='y')

    # Plot 4: Context distribution
    ax4 = axes[1, 1]
    context_counts = df['Context'].value_counts()
    ax4.pie(context_counts.values, labels=context_counts.index, autopct='%1.1f%%',
            startangle=90, textprops={'fontsize': 10})
    ax4.set_title('Data Context Distribution', fontsize=12, fontweight='bold')

    plt.tight_layout()

    # Save
    output_dir = Path('results/figures')
    output_dir.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_dir / 'model_overview.png', dpi=300, bbox_inches='tight')
    print(f"Saved to {output_dir}/model_overview.png")

    # Summary stats
    print(f"\nDataset summary:")
    print(f"Total entries: {len(df)}")
    print(f"FC range: {df['FC_numeric'].min():.1f} - {df['FC_numeric'].max():.1f}")
    print(f"Median FC: {df['FC_numeric'].median():.1f}")
    print(f"Subtypes: {df['Subtype'].nunique()}")

if __name__ == '__main__':
    main()
