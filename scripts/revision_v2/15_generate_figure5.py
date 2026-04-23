#!/usr/bin/env python3
"""
Figure 5: Evolution & Fitness Context
5 panels: conservation, subtype frequencies, fitness-resistance, pathway, surveillance priority
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.gridspec import GridSpec
import matplotlib.patches as mpatches
from pathlib import Path
import re

# Setup
BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "data" / "processed" / "revision_v2"
RESULTS_DIR = BASE_DIR / "results" / "revision_v2"
OUTPUT_DIR = BASE_DIR / "manuscript" / "figures" / "revision_v2"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

plt.style.use('seaborn-v0_8-paper')


def _parse_first_number(value):
    """Extract first numeric token from mixed text."""
    if pd.isna(value):
        return np.nan
    s = str(value)
    m = re.search(r'[-+]?\d*\.?\d+', s)
    return float(m.group()) if m else np.nan


def _parse_fitness_percent(value):
    """Parse fitness text into approximate %WT when numeric cues exist."""
    if pd.isna(value):
        return np.nan
    s = str(value).strip().lower()

    # Common textual labels without explicit numeric cues.
    if 'minimal' in s:
        return 95.0
    if 'wt' in s and ('level' in s or 'wt-level' in s):
        return 100.0

    # Use first bound for ranges (e.g., 0.06%-7.8%).
    if '-' in s:
        s = s.split('-')[0]

    val = _parse_first_number(s.replace('%', ''))
    if np.isnan(val):
        return np.nan
    return val

def create_conservation_plot(ax):
    """Panel A: Conservation scores for LEN-contact residues"""

    # Load conservation data
    cons_df = pd.read_csv(RESULTS_DIR / "conservation_analysis.csv")
    cons_df = cons_df.sort_values('position_gag')

    # Create bar plot
    colors = ['#E74C3C' if score < 0.8 else '#F39C12' if score < 0.95 else '#27AE60'
              for score in cons_df['conservation_score']]

    bars = ax.bar(range(len(cons_df)), cons_df['conservation_score'],
                  color=colors, alpha=0.8, edgecolor='black', linewidth=1)

    # Add position labels
    labels = [str(row['position_name'])
              for _, row in cons_df.iterrows()]
    ax.set_xticks(range(len(cons_df)))
    ax.set_xticklabels(labels, rotation=45, ha='right', fontsize=8)

    ax.set_ylabel('Conservation Score', fontsize=9, weight='bold')
    ax.set_title('A. Sequence Conservation at LEN-Contact Residues', fontsize=10, weight='bold', loc='left')
    ax.set_ylim(0, 1.05)
    ax.grid(axis='y', alpha=0.3)

    # Add threshold lines
    ax.axhline(y=0.95, color='green', linestyle='--', alpha=0.5, linewidth=2, label='Highly conserved')
    ax.axhline(y=0.8, color='orange', linestyle='--', alpha=0.5, linewidth=2, label='Moderately conserved')

    # Highlight resistance positions
    resistance_positions = ['N57', 'M66', 'Q67', 'K70', 'N74', 'A105', 'T107']
    for i, label in enumerate(labels):
        if any(rp in str(label) for rp in resistance_positions):
            ax.text(i, cons_df.iloc[i]['conservation_score'] + 0.02, '*',
                   ha='center', fontsize=14, weight='bold', color='red')

    ax.legend(fontsize=7, loc='lower left')

    # Add annotation
    ax.text(0.98, 0.98, '* = Known resistance position',
           transform=ax.transAxes, ha='right', va='top',
           fontsize=7, color='red', weight='bold',
           bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

def create_subtype_frequencies(ax):
    """Panel B: Subtype-specific baseline frequencies"""

    # Load subtype frequency data
    freq_df = pd.read_csv(RESULTS_DIR / "subtype_frequencies.csv")

    # Pivot for heatmap
    pivot = freq_df.pivot_table(
        index='mutation',
        columns='subtype',
        values='mut_frequency',
        aggfunc='mean'
    )

    # Plot heatmap
    sns.heatmap(pivot, annot=True, fmt='.3f', cmap='YlOrRd',
                cbar_kws={'label': 'Frequency'},
                linewidths=0.5, linecolor='white',
                ax=ax, vmin=0, vmax=0.05)

    ax.set_xlabel('HIV-1 Subtype', fontsize=9, weight='bold')
    ax.set_ylabel('Resistance Position', fontsize=9, weight='bold')
    ax.set_title('B. Subtype-Specific Baseline Frequencies', fontsize=10, weight='bold', loc='left')
    plt.setp(ax.get_xticklabels(), rotation=0, fontsize=8)
    plt.setp(ax.get_yticklabels(), rotation=0, fontsize=8)

    # Add annotation for natural polymorphisms - move to upper right
    ax.text(0.98, 0.98, 'Red = elevated baseline\n(potential natural polymorphism)',
           transform=ax.transAxes, ha='right', va='top',
           fontsize=6, bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.3))

def create_fitness_resistance_scatter(ax):
    """Panel C: Fitness cost vs resistance level (observed data only)"""
    # Recover fitness-resistance data from multiple sources.
    candidates = []

    # Source 1: phase2 merged quantitative table (highest priority).
    phase2_path = BASE_DIR / "results" / "phase2" / "fitness_resistance_data.csv"
    if phase2_path.exists():
        p2 = pd.read_csv(phase2_path)
        if {'Mutation', 'FC', 'Fitness_pct'}.issubset(p2.columns):
            p2 = p2[['Mutation', 'FC', 'Fitness_pct']].copy()
            p2['fitness_cost'] = p2['Fitness_pct'].apply(_parse_fitness_percent)
            p2['source_rank'] = 1
            candidates.append(p2[['Mutation', 'FC', 'fitness_cost', 'source_rank']])

    # Source 2: biological annotations with textual fitness/fold-change.
    bio_path = BASE_DIR / "results" / "validation" / "biological_annotations.csv"
    if bio_path.exists():
        bio = pd.read_csv(bio_path)
        if len(bio.columns) > 0 and str(bio.columns[0]).startswith('Unnamed'):
            bio = bio.rename(columns={bio.columns[0]: 'Mutation'})
        if {'Mutation', 'fold_change', 'fitness_cost'}.issubset(bio.columns):
            bio_df = pd.DataFrame({
                'Mutation': bio['Mutation'],
                'FC': bio['fold_change'].apply(_parse_first_number),
                'fitness_cost': bio['fitness_cost'].apply(_parse_fitness_percent),
                'source_rank': 2
            })
            candidates.append(bio_df)

    # Source 3 (fallback): curated phenotype + curated fitness.
    ph_path = BASE_DIR / "data" / "curated" / "phenotype_unified.csv"
    ft_path = BASE_DIR / "data" / "curated" / "fitness_unified.csv"
    if ph_path.exists() and ft_path.exists():
        ph = pd.read_csv(ph_path)
        ft = pd.read_csv(ft_path)
        if {'Mutation', 'FC_numeric'}.issubset(ph.columns) and {'Mutation', 'Fitness_WT_pct'}.issubset(ft.columns):
            cur = ph[['Mutation', 'FC_numeric']].merge(
                ft[['Mutation', 'Fitness_WT_pct']],
                on='Mutation',
                how='inner'
            )
            cur = cur.rename(columns={'FC_numeric': 'FC'})
            cur['fitness_cost'] = cur['Fitness_WT_pct'].apply(_parse_fitness_percent)
            cur['source_rank'] = 3
            candidates.append(cur[['Mutation', 'FC', 'fitness_cost', 'source_rank']])

    if candidates:
        df_fitness = pd.concat(candidates, ignore_index=True)
        df_fitness = df_fitness[df_fitness['FC'].notna() & df_fitness['fitness_cost'].notna()].copy()
        # Prefer high-priority sources, then aggregate by mutation for cleaner labels.
        df_fitness = df_fitness.sort_values('source_rank')
        df_fitness = (
            df_fitness.groupby('Mutation', as_index=False)
            .agg({'FC': 'median', 'fitness_cost': 'median', 'source_rank': 'min'})
        )
        df_fitness['log10_FC'] = np.log10(df_fitness['FC'].clip(lower=1e-6))
    else:
        df_fitness = pd.DataFrame()

    if len(df_fitness) == 0:
        ax.text(0.5, 0.5, 'No fitness data available\n(n=0 observations)',
               ha='center', va='center', fontsize=9, transform=ax.transAxes,
               bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.3))
        ax.set_title('C. Fitness Cost vs Resistance', fontsize=10, weight='bold', loc='left')
        ax.set_xlabel('log10(Fold-Change)', fontsize=9, weight='bold')
        ax.set_ylabel('Fitness Cost (% WT)', fontsize=9, weight='bold')
        return

    # Scatter plot
    colors = ['#E74C3C' if fc > 100 else '#F39C12' if fc > 10 else '#3498DB'
              for fc in df_fitness['FC']]

    ax.scatter(df_fitness['log10_FC'], df_fitness['fitness_cost'],
              c=colors, s=150, alpha=0.7, edgecolors='black', linewidth=1.5)

    # Add labels
    for _, row in df_fitness.iterrows():
        ax.annotate(row['Mutation'],
                   (row['log10_FC'], row['fitness_cost']),
                   xytext=(5, 5), textcoords='offset points',
                   fontsize=7, weight='bold')

    ax.set_xlabel('log10(Fold-Change)', fontsize=9, weight='bold')
    ax.set_ylabel('Fitness Cost (% WT)', fontsize=9, weight='bold')
    ax.set_title('C. Fitness Cost vs Resistance Level', fontsize=10, weight='bold', loc='left')
    ax.grid(alpha=0.3)

    # Add quadrant lines
    if len(df_fitness) > 0:
        median_fc = df_fitness['log10_FC'].median()
        median_fit = df_fitness['fitness_cost'].median()
        ax.axvline(x=median_fc, color='gray', linestyle='--', alpha=0.5)
        ax.axhline(y=median_fit, color='gray', linestyle='--', alpha=0.5)

    # Add annotation
    ax.text(0.98, 0.98, f'n={len(df_fitness)} observations with fitness data',
           transform=ax.transAxes, ha='right', va='top',
           fontsize=7, bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

def create_evidence_pathway(ax):
    """Panel D: Evidence-coded resistance pathway"""

    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Title
    ax.text(5, 9.5, 'D. Evidence-Coded Resistance Pathway', ha='center', fontsize=10, weight='bold')

    # Define pathway nodes with increased vertical spacing
    nodes = [
        (2, 8.5, 'WT\nSusceptible', '#27AE60', 'solid'),
        (2, 6.5, 'Low\nResistance\n(10-100x)', '#3498DB', 'solid'),
        (2, 4.5, 'Moderate\nResistance\n(100-1000x)', '#F39C12', 'solid'),
        (2, 2.5, 'High\nResistance\n(>1000x)', '#E74C3C', 'solid'),
        (5, 6.5, 'Context-\nSensitive', '#9B59B6', 'dashed'),
        (5, 4.5, 'Compensatory\nMutations', '#2ECC71', 'dashed'),
        (8, 6.5, 'Natural\nPolymorphism', '#95A5A6', 'dashed'),
    ]

    # Draw nodes
    for x, y, label, color, style in nodes:
        if style == 'solid':
            circle = plt.Circle((x, y), 0.6, facecolor=color, edgecolor='black',
                              linewidth=2, alpha=0.8)
        else:
            circle = plt.Circle((x, y), 0.6, facecolor=color, edgecolor='black',
                              linewidth=2, linestyle='--', alpha=0.6)
        ax.add_patch(circle)
        ax.text(x, y, label, ha='center', va='center', fontsize=6, weight='bold')

    # Draw edges (arrows) with adjusted positions
    edges = [
        # Main pathway (solid = observed)
        ((2, 7.9), (2, 7.1), 'solid', 'black'),
        ((2, 5.9), (2, 5.1), 'solid', 'black'),
        ((2, 3.9), (2, 3.1), 'solid', 'black'),
        # Context-sensitive branch (dashed = inferred)
        ((2.5, 6.8), (4.5, 6.6), 'dashed', 'purple'),
        ((5, 5.9), (3, 5.0), 'dashed', 'purple'),
        # Compensatory branch (dashed = inferred)
        ((2.5, 4.8), (4.5, 4.6), 'dashed', 'green'),
        ((5.5, 4.5), (2.5, 2.8), 'dashed', 'green'),
        # Natural polymorphism (dashed = inferred)
        ((2.5, 8.2), (7.5, 6.8), 'dashed', 'gray'),
    ]

    for (x1, y1), (x2, y2), style, color in edges:
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                   arrowprops=dict(arrowstyle='->', lw=2, color=color,
                                 linestyle=style, alpha=0.7))

    # Add legend
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], color='black', linewidth=2, linestyle='solid', label='Observed pathway'),
        Line2D([0], [0], color='black', linewidth=2, linestyle='dashed', label='Inferred pathway'),
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=7,
             bbox_to_anchor=(0.98, 0.02))

    # Add example mutations
    ax.text(0.5, 0.5, 'Examples:\nN57H, M66I', ha='center', fontsize=5, color='red')
    ax.text(5, 7.2, 'Q67H+K70R', ha='center', fontsize=5, color='purple')
    ax.text(5, 3.2, 'M66I+A105T', ha='center', fontsize=5, color='green')

def create_surveillance_priority(ax):
    """Panel E: Surveillance priority ranking"""

    # Load classification data
    try:
        class_df = pd.read_csv(RESULTS_DIR / "mutation_classifications.csv")
    except FileNotFoundError:
        ax.text(0.5, 0.5, 'Surveillance priority data not available',
               ha='center', va='center', fontsize=9, transform=ax.transAxes,
               bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.3))
        ax.set_title('E. Surveillance Priority Ranking', fontsize=10, weight='bold', loc='left')
        ax.set_xlabel('Surveillance Priority Score', fontsize=9, weight='bold')
        return

    # Define priority score
    priority_map = {
        # Current revision_v2 categories
        'primary_resistant': 10,
        'moderate_resistant': 7,
        'low_resistant': 4,
        'additive': 7,
        'sub_additive': 5,
        'putative_compensatory': 6,
        # Backward-compatible labels
        'synergistic': 8,
        'compensatory': 6,
        'natural_polymorphism': 3
    }

    class_df['priority_score'] = class_df['category'].map(priority_map)
    class_df = class_df[class_df['priority_score'].notna()].copy()

    # If a mutation appears multiple times, keep one representative row.
    evidence_rank = {'hypothesis_generating': 1, 'moderate': 2, 'strong': 3}
    class_df['evidence_rank'] = class_df['evidence_strength'].map(evidence_rank).fillna(0)
    class_df = class_df.sort_values(['mutation', 'priority_score', 'evidence_rank'], ascending=[True, False, False])
    class_df = class_df.drop_duplicates(subset=['mutation'], keep='first')
    class_df = class_df.sort_values('priority_score', ascending=True)

    # Create horizontal strip plot
    colors_map = {
        'primary_resistant': '#E74C3C',
        'moderate_resistant': '#F39C12',
        'low_resistant': '#3498DB',
        'synergistic': '#9B59B6',
        'compensatory': '#2ECC71',
        'natural_polymorphism': '#95A5A6'
    }

    colors = [colors_map.get(cat, 'gray') for cat in class_df['category']]

    bars = ax.barh(range(len(class_df)), class_df['priority_score'],
                   color=colors, alpha=0.8, edgecolor='black', linewidth=1)

    ax.set_yticks(range(len(class_df)))
    ax.set_yticklabels(class_df['mutation'], fontsize=7)
    ax.set_xlabel('Surveillance Priority Score', fontsize=9, weight='bold')
    ax.set_title('E. Surveillance Priority Ranking', fontsize=10, weight='bold', loc='left')
    ax.grid(axis='x', alpha=0.3)

    # Add priority zones
    ax.axvspan(0, 5, alpha=0.1, color='green', label='Low priority')
    ax.axvspan(5, 8, alpha=0.1, color='yellow', label='Medium priority')
    ax.axvspan(8, 10, alpha=0.1, color='red', label='High priority')

    # Add evidence strength markers
    for i, (score, evidence) in enumerate(zip(class_df['priority_score'], class_df['evidence_strength'])):
        marker = '***' if evidence == 'strong' else '**' if evidence == 'moderate' else '*'
        ax.text(score + 0.2, i, marker, va='center', fontsize=8, weight='bold', color='black', clip_on=False)

    # Merge all E-panel notes into one box with unified font style.
    legend_text = (
        'Priority: Low (0-5), Medium (5-8), High (8-10)\n'
        'Evidence: *** strong, ** moderate, * hypothesis'
    )
    ax.text(0.98, 0.02, legend_text,
           transform=ax.transAxes, ha='right', va='bottom',
           fontsize=6, bbox=dict(boxstyle='round', facecolor='white', alpha=0.85))

def main():
    """Generate Figure 5"""
    print("="*60)
    print("Generating Figure 5: Evolution & Fitness Context")
    print("="*60)

    # Create figure
    fig = plt.figure(figsize=(22, 17))
    gs = GridSpec(3, 2, figure=fig, hspace=0.55, wspace=0.5)

    ax1 = fig.add_subplot(gs[0, :])  # Conservation spans full width
    ax2 = fig.add_subplot(gs[1, 0])
    ax3 = fig.add_subplot(gs[1, 1])
    ax4 = fig.add_subplot(gs[2, 0])
    ax5 = fig.add_subplot(gs[2, 1])

    # Generate panels
    print("\nPanel A: Conservation plot...")
    create_conservation_plot(ax1)

    print("Panel B: Subtype frequencies...")
    create_subtype_frequencies(ax2)

    print("Panel C: Fitness vs resistance...")
    create_fitness_resistance_scatter(ax3)

    print("Panel D: Evidence pathway...")
    create_evidence_pathway(ax4)

    print("Panel E: Surveillance priority...")
    create_surveillance_priority(ax5)

    # Save
    plt.tight_layout()

    output_pdf = OUTPUT_DIR / "figure5_evolution.pdf"
    output_png = OUTPUT_DIR / "figure5_evolution.png"

    fig.savefig(output_pdf, dpi=300, bbox_inches='tight', pad_inches=0.3)
    fig.savefig(output_png, dpi=300, bbox_inches='tight', pad_inches=0.3)

    print(f"\n[OK] Saved: {output_pdf}")
    print(f"\n[OK] Saved: {output_png}")
    print("\n" + "="*60)
    print("Figure 5 complete!")
    print("="*60)

    plt.close()

if __name__ == "__main__":
    main()
