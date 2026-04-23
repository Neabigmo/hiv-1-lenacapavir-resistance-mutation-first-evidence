#!/usr/bin/env python3
"""
Figure 2: Core Phenotypic Evidence and Model Comparison
4 panels: raw observations, pooled estimates, model comparison, rank stability
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.gridspec import GridSpec
from pathlib import Path

# Setup
BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "data" / "processed" / "revision_v2"
RESULTS_DIR = BASE_DIR / "results" / "revision_v2"
OUTPUT_DIR = BASE_DIR / "manuscript" / "figures" / "revision_v2"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

plt.style.use('seaborn-v0_8-paper')

def create_raw_observations_strip(ax):
    """Panel A: Strip plot of raw observations colored by context"""

    # Load data
    df = pd.read_csv(DATA_DIR / "harmonized_phenotype_data.csv")
    df = df[df['log10_FC'].notna()].copy()

    # Sort mutations by mean log10_FC
    mut_order = df.groupby('Mutation')['log10_FC'].mean().sort_values(ascending=False).index.tolist()

    # Color by context
    context_colors = {
        'clinical': '#E74C3C',
        'in_vitro': '#3498DB',
        'natural_polymorphism': '#2ECC71'
    }

    # Create strip plot
    for i, mut in enumerate(mut_order):
        mut_data = df[df['Mutation'] == mut]

        for _, row in mut_data.iterrows():
            color = context_colors.get(row['context_tier'], 'gray')
            ax.scatter(row['log10_FC'], i, c=color, s=80, alpha=0.7,
                      edgecolors='black', linewidth=0.5, zorder=3)

    ax.set_yticks(range(len(mut_order)))
    ax.set_yticklabels(mut_order, fontsize=8)
    ax.set_xlabel('log10(Fold-Change)', fontsize=10, weight='bold')
    ax.set_title('A. Raw Phenotypic Observations', fontsize=11, weight='bold', loc='left')
    ax.grid(axis='x', alpha=0.3, zorder=1)
    ax.axvline(x=1, color='gray', linestyle='--', alpha=0.5, label='10-fold')
    ax.axvline(x=2, color='gray', linestyle='--', alpha=0.5, label='100-fold')
    ax.axvline(x=3, color='red', linestyle='--', alpha=0.5, label='1000-fold')

    # Legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#E74C3C', label='Clinical'),
        Patch(facecolor='#3498DB', label='In vitro'),
        Patch(facecolor='#2ECC71', label='Natural polymorphism')
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=7, framealpha=0.95)

def create_pooled_estimates(ax):
    """Panel B: Partial pooling estimates with uncertainty"""

    # Load data
    df = pd.read_csv(DATA_DIR / "harmonized_phenotype_data.csv")
    df = df[df['log10_FC'].notna()].copy()

    # Calculate mean and std for each mutation
    summary = df.groupby('Mutation')['log10_FC'].agg(['mean', 'std', 'count']).reset_index()
    summary['sem'] = summary['std'] / np.sqrt(summary['count'])
    summary = summary.sort_values('mean', ascending=True)

    # Create horizontal error bars
    colors = ['#E74C3C' if mean > 3 else '#F39C12' if mean > 2 else '#3498DB' if mean > 1 else '#95A5A6'
              for mean in summary['mean']]

    y_pos = range(len(summary))

    for i, (_, row) in enumerate(summary.iterrows()):
        # Error bar
        if not np.isnan(row['sem']):
            ax.errorbar(row['mean'], i, xerr=row['sem']*1.96, fmt='o',
                       color=colors[i], markersize=8, capsize=4, capthick=2,
                       elinewidth=2, alpha=0.8)
        else:
            ax.scatter(row['mean'], i, c=colors[i], s=80, alpha=0.8,
                      edgecolors='black', linewidth=1)

        # Add n count with clip_on=False to allow labels outside axis
        ax.text(row['mean'] + 0.15, i, f"n={int(row['count'])}",
               va='center', fontsize=6, color='gray', clip_on=False)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(summary['Mutation'], fontsize=8)
    ax.set_xlabel('log10(Fold-Change) ± 95% CI', fontsize=10, weight='bold')
    ax.set_title('B. Pooled Effect Estimates', fontsize=11, weight='bold', loc='left')
    ax.grid(axis='x', alpha=0.3)
    ax.axvline(x=1, color='gray', linestyle='--', alpha=0.5)
    ax.axvline(x=2, color='gray', linestyle='--', alpha=0.5)
    ax.axvline(x=3, color='red', linestyle='--', alpha=0.5)

    # Legend for colors
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#E74C3C', label='>1000-fold'),
        Patch(facecolor='#F39C12', label='100-1000-fold'),
        Patch(facecolor='#3498DB', label='10-100-fold'),
        Patch(facecolor='#95A5A6', label='<10-fold')
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=7, framealpha=0.9)

def create_model_comparison(ax):
    """Panel C: Model comparison (AIC/BIC bars)"""

    # Load model comparison
    models_df = pd.read_csv(RESULTS_DIR / "model_comparison.csv")

    # Filter valid models
    models_df = models_df[models_df['aic'].notna()].copy()

    model_names = models_df['model_name'].str.replace('_', ' ').str.title()
    aic_values = models_df['aic'].values
    bic_values = models_df['bic'].values

    x = np.arange(len(model_names))
    width = 0.35

    bars1 = ax.bar(x - width/2, aic_values, width, label='AIC', color='#3498DB', alpha=0.8)
    bars2 = ax.bar(x + width/2, bic_values, width, label='BIC', color='#E74C3C', alpha=0.8)

    ax.set_xlabel('Model', fontsize=10, weight='bold')
    ax.set_ylabel('Information Criterion', fontsize=10, weight='bold')
    ax.set_title('C. Model Comparison', fontsize=11, weight='bold', loc='left')
    ax.set_xticks(x)
    ax.set_xticklabels(model_names, rotation=15, ha='right', fontsize=9)
    ax.legend(fontsize=9)
    ax.grid(axis='y', alpha=0.3)

    # Add values on bars
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            if not np.isnan(height):
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.1f}',
                       ha='center', va='bottom', fontsize=7)

    # Highlight best model - position inside the plot area
    best_idx = np.argmin(aic_values)
    max_height = max(max(aic_values), max(bic_values))
    ax.text(best_idx, max_height * 0.85, '★ Best', ha='center',
           fontsize=9, weight='bold', color='#F39C12')

def create_rank_stability_heatmap(ax):
    """Panel D: Leave-one-study-out rank stability"""

    # Load bootstrap ranks
    ranks_df = pd.read_csv(RESULTS_DIR / "bootstrap_ranks.csv")
    ranks_df = ranks_df.sort_values('mean_rank')

    # Create data for heatmap: mutation × metric
    data = ranks_df[['mean_rank', 'std_rank', 'rank_stability']].T
    data.columns = ranks_df['mutation']

    # Plot heatmap with better color range and smaller font
    sns.heatmap(data, annot=True, fmt='.2f', cmap='RdYlGn_r',
                cbar_kws={'label': 'Value'},
                linewidths=0.5, linecolor='white',
                annot_kws={'fontsize': 6},
                ax=ax, vmin=0, vmax=max(10, data.max().max()))

    ax.set_xlabel('Mutation', fontsize=9, weight='bold')
    ax.set_ylabel('Metric', fontsize=9, weight='bold')
    ax.set_title('D. Bootstrap Ranking Stability', fontsize=10, weight='bold', loc='left')
    ax.set_yticklabels(['Mean Rank', 'Std Rank', 'Stability'], rotation=0, fontsize=7)
    plt.setp(ax.get_xticklabels(), rotation=45, ha='right', fontsize=6)

def main():
    """Generate Figure 2"""
    print("="*60)
    print("Generating Figure 2: Core Phenotypic Evidence")
    print("="*60)

    # Create figure with increased size and spacing
    fig = plt.figure(figsize=(20, 15))
    gs = GridSpec(2, 2, figure=fig, hspace=0.5, wspace=0.45)

    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    ax3 = fig.add_subplot(gs[1, 0])
    ax4 = fig.add_subplot(gs[1, 1])

    # Generate panels
    print("\nPanel A: Raw observations...")
    create_raw_observations_strip(ax1)

    print("Panel B: Pooled estimates...")
    create_pooled_estimates(ax2)

    print("Panel C: Model comparison...")
    create_model_comparison(ax3)

    print("Panel D: Rank stability...")
    create_rank_stability_heatmap(ax4)

    # Save
    plt.tight_layout()

    output_pdf = OUTPUT_DIR / "figure2_core_evidence.pdf"
    output_png = OUTPUT_DIR / "figure2_core_evidence.png"

    fig.savefig(output_pdf, dpi=300, bbox_inches='tight', pad_inches=0.3)
    fig.savefig(output_png, dpi=300, bbox_inches='tight', pad_inches=0.3)

    print(f"\n[OK] Saved: {output_pdf}")
    print(f"[OK] Saved: {output_png}")
    print("\n" + "="*60)
    print("Figure 2 complete!")
    print("="*60)

    plt.close()

if __name__ == "__main__":
    main()
