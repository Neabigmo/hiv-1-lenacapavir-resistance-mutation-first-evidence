#!/usr/bin/env python3
"""
Fitness-resistance tradeoff analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

def parse_fitness(fitness_str):
    """Parse fitness percentage from string"""
    if pd.isna(fitness_str):
        return np.nan

    s = str(fitness_str)
    # Extract numeric value
    if '%' in s:
        s = s.replace('%', '')

    # Handle ranges like "0.06%-7.8%"
    if '-' in s:
        parts = s.split('-')
        try:
            return float(parts[0])  # Use lower bound
        except:
            return np.nan

    try:
        return float(s)
    except:
        return np.nan

def main():
    print("Analyzing fitness-resistance tradeoff...")

    # Load unified data
    pheno = pd.read_csv('data/curated/phenotype_unified.csv')
    fitness = pd.read_csv('data/curated/fitness_unified.csv')

    # Parse fitness values
    fitness['Fitness_numeric'] = fitness['Fitness_WT_pct'].apply(parse_fitness)

    # Merge phenotype and fitness
    merged = pd.merge(
        pheno[['Mutation', 'FC_numeric', 'Subtype']],
        fitness[['Mutation', 'Fitness_numeric']],
        on='Mutation',
        how='inner'
    )

    print(f"Merged data: {len(merged)} mutations with both FC and fitness")

    if len(merged) < 3:
        print("Insufficient data for tradeoff analysis")
        return

    # Log transform
    merged['LogFC'] = np.log10(merged['FC_numeric'] + 1)
    merged['LogFitness'] = np.log10(merged['Fitness_numeric'] + 1)

    # Create visualization
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Plot 1: Linear scale
    ax1 = axes[0]
    ax1.scatter(merged['FC_numeric'], merged['Fitness_numeric'],
                alpha=0.6, s=100)
    ax1.set_xlabel('Fold-Change (FC)', fontsize=12)
    ax1.set_ylabel('Fitness (% WT)', fontsize=12)
    ax1.set_title('Fitness-Resistance Tradeoff', fontsize=14)
    ax1.grid(True, alpha=0.3)

    # Annotate key mutations
    for _, row in merged.iterrows():
        if row['FC_numeric'] > 100 or row['Fitness_numeric'] < 10:
            ax1.annotate(row['Mutation'],
                        (row['FC_numeric'], row['Fitness_numeric']),
                        fontsize=8, alpha=0.7)

    # Plot 2: Log scale
    ax2 = axes[1]
    ax2.scatter(merged['LogFC'], merged['LogFitness'],
                alpha=0.6, s=100, c='red')
    ax2.set_xlabel('Log10(FC)', fontsize=12)
    ax2.set_ylabel('Log10(Fitness % WT)', fontsize=12)
    ax2.set_title('Log-Scale Tradeoff', fontsize=14)
    ax2.grid(True, alpha=0.3)

    # Fit linear regression
    from scipy.stats import linregress
    valid = merged[['LogFC', 'LogFitness']].dropna()
    if len(valid) >= 3:
        slope, intercept, r, p, se = linregress(valid['LogFC'], valid['LogFitness'])
        x_line = np.linspace(valid['LogFC'].min(), valid['LogFC'].max(), 100)
        y_line = slope * x_line + intercept
        ax2.plot(x_line, y_line, 'k--', alpha=0.5,
                label=f'R²={r**2:.3f}, p={p:.3e}')
        ax2.legend()

    plt.tight_layout()

    # Save figure
    output_dir = Path('results/figures')
    output_dir.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_dir / 'fitness_resistance_tradeoff.png', dpi=300)
    print(f"Saved figure to {output_dir}")

    # Identify Pareto frontier
    pareto = []
    for i, row in merged.iterrows():
        dominated = False
        for j, other in merged.iterrows():
            if i != j:
                # Check if other dominates row (higher FC AND higher fitness)
                if (other['FC_numeric'] >= row['FC_numeric'] and
                    other['Fitness_numeric'] >= row['Fitness_numeric'] and
                    (other['FC_numeric'] > row['FC_numeric'] or
                     other['Fitness_numeric'] > row['Fitness_numeric'])):
                    dominated = True
                    break
        if not dominated:
            pareto.append(row)

    pareto_df = pd.DataFrame(pareto)
    print(f"\nPareto frontier: {len(pareto_df)} mutations")
    print(pareto_df[['Mutation', 'FC_numeric', 'Fitness_numeric']].to_string())

    # Save results
    pareto_df.to_csv(output_dir.parent / 'pareto_frontier.csv', index=False)

    # Summary statistics
    print(f"\nCorrelation: {merged['LogFC'].corr(merged['LogFitness']):.3f}")
    print(f"High resistance (FC>100): {(merged['FC_numeric']>100).sum()} mutations")
    print(f"Severe fitness cost (<10% WT): {(merged['Fitness_numeric']<10).sum()} mutations")

if __name__ == '__main__':
    main()
