#!/usr/bin/env python3
"""
Figure 1: Evidence Landscape
4 panels showing PRISMA flow, availability matrix, observation counts, harmonization
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import seaborn as sns
from pathlib import Path

# Setup
BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "data" / "processed" / "revision_v2"
RESULTS_DIR = BASE_DIR / "results" / "revision_v2"
OUTPUT_DIR = BASE_DIR / "manuscript" / "figures" / "revision_v2"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Set style
plt.style.use('seaborn-v0_8-paper')
sns.set_palette("husl")

def create_prisma_flow(ax):
    """Panel A: PRISMA-style flow diagram"""

    # Load data
    flow_df = pd.read_csv(DATA_DIR / "evidence_flow.csv")

    # Define boxes
    boxes = [
        # (y_pos, text, count, color)
        (0.9, "Records identified\nthrough database searching", 82, '#E8F4F8'),
        (0.9, "Additional records identified\nthrough other sources", 5, '#E8F4F8'),
        (0.75, "Records after duplicates removed", 78, '#E8F4F8'),
        (0.6, "Records screened\n(title/abstract)", 78, '#FFF4E6'),
        (0.45, "Full-text articles assessed\nfor eligibility", 22, '#FFF4E6'),
        (0.3, "Studies included in\nqualitative synthesis", 11, '#E8F5E9'),
        (0.15, "Studies included in\nquantitative synthesis\n(meta-analysis)", 11, '#E8F5E9'),
    ]

    # Exclusions
    exclusions = [
        (0.6, 0.7, "Excluded (n=56)\nNot relevant", '#FFE6E6'),
        (0.45, 0.55, "Excluded (n=11)\n• No quantitative data (n=8)\n• HIV-2 only (n=3)", '#FFE6E6'),
    ]

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Draw identification boxes (side by side)
    rect1 = mpatches.FancyBboxPatch((0.05, 0.88), 0.35, 0.1,
                                     boxstyle="round,pad=0.01",
                                     facecolor='#E8F4F8', edgecolor='black', linewidth=1.5)
    ax.add_patch(rect1)
    ax.text(0.225, 0.93, "PubMed search\nn=82", ha='center', va='center', fontsize=9, weight='bold')

    rect2 = mpatches.FancyBboxPatch((0.55, 0.88), 0.35, 0.1,
                                     boxstyle="round,pad=0.01",
                                     facecolor='#E8F4F8', edgecolor='black', linewidth=1.5)
    ax.add_patch(rect2)
    ax.text(0.725, 0.93, "Other sources\nn=5", ha='center', va='center', fontsize=9, weight='bold')

    # Arrow down to combined - increase length to avoid breaking
    ax.arrow(0.45, 0.87, 0, -0.10, head_width=0.03, head_length=0.02, fc='black', ec='black')

    # Main flow boxes - increase vertical spacing
    y_positions = [0.73, 0.57, 0.41, 0.25, 0.09]
    labels = [
        "Records after\ndeduplication\nn=78",
        "Title/abstract\nscreened\nn=78",
        "Full-text assessed\nn=22",
        "Qualitative synthesis\nn=11",
        "Quantitative synthesis\nn=11"
    ]
    colors = ['#E8F4F8', '#FFF4E6', '#FFF4E6', '#E8F5E9', '#E8F5E9']

    for i, (y, label, color) in enumerate(zip(y_positions, labels, colors)):
        rect = mpatches.FancyBboxPatch((0.3, y-0.05), 0.4, 0.1,
                                        boxstyle="round,pad=0.01",
                                        facecolor=color, edgecolor='black', linewidth=1.5)
        ax.add_patch(rect)
        ax.text(0.5, y, label, ha='center', va='center', fontsize=8, weight='bold')

        # Arrow to next box - increase length
        if i < len(y_positions) - 1:
            ax.arrow(0.5, y-0.06, 0, -0.09, head_width=0.03, head_length=0.02, fc='black', ec='black')

    # Exclusion boxes
    # Excluded after screening
    rect_ex1 = mpatches.FancyBboxPatch((0.75, 0.58), 0.2, 0.08,
                                        boxstyle="round,pad=0.005",
                                        facecolor='#FFE6E6', edgecolor='red', linewidth=1, linestyle='--')
    ax.add_patch(rect_ex1)
    ax.text(0.85, 0.62, "Excluded\nn=56", ha='center', va='center', fontsize=8)
    ax.arrow(0.7, 0.6, 0.04, 0.02, head_width=0.02, head_length=0.01, fc='red', ec='red', linestyle='--')

    # Excluded after full-text
    rect_ex2 = mpatches.FancyBboxPatch((0.75, 0.4), 0.2, 0.12,
                                        boxstyle="round,pad=0.005",
                                        facecolor='#FFE6E6', edgecolor='red', linewidth=1, linestyle='--')
    ax.add_patch(rect_ex2)
    ax.text(0.85, 0.46, "Excluded (n=11)\nNo quant: 8\nHIV-2: 3", ha='center', va='center', fontsize=7)
    ax.arrow(0.7, 0.45, 0.04, 0.01, head_width=0.02, head_length=0.01, fc='red', ec='red', linestyle='--')

    ax.set_title('A. PRISMA Evidence Flow', fontsize=11, weight='bold', loc='left')

def create_availability_matrix(ax):
    """Panel B: Mutation × Subtype × Context availability matrix"""

    # Load data
    avail_df = pd.read_csv(DATA_DIR / "availability_matrix.csv")

    # Create pivot table
    # For visualization, combine subtype and context
    avail_df['subtype_context'] = avail_df['subtype'] + '_' + avail_df['context']

    pivot = avail_df.pivot_table(
        index='mutation',
        columns='subtype_context',
        values='n_observations',
        fill_value=0
    )

    # Plot heatmap
    sns.heatmap(pivot, annot=True, fmt='g', cmap='YlOrRd',
                cbar_kws={'label': 'N observations'},
                linewidths=0.5, linecolor='gray',
                ax=ax, vmin=0, vmax=5)

    ax.set_xlabel('Subtype × Context', fontsize=9)
    ax.set_ylabel('Mutation', fontsize=9)
    ax.set_title('B. Data Availability Matrix', fontsize=11, weight='bold', loc='left')
    plt.setp(ax.get_xticklabels(), rotation=45, ha='right', fontsize=7)
    plt.setp(ax.get_yticklabels(), rotation=0, fontsize=8)

def create_observation_counts(ax):
    """Panel C: Observation count per mutation"""

    # Load data
    obs_df = pd.read_csv(DATA_DIR / "observation_summary.csv")
    obs_df = obs_df.sort_values('n_observations', ascending=True)

    # Create horizontal bar plot
    colors = ['#2E86AB' if '+' not in mut else '#A23B72'
              for mut in obs_df['mutation']]

    bars = ax.barh(range(len(obs_df)), obs_df['n_observations'], color=colors, alpha=0.8)

    ax.set_yticks(range(len(obs_df)))
    ax.set_yticklabels(obs_df['mutation'], fontsize=8)
    ax.set_xlabel('Number of Observations', fontsize=9)
    ax.set_title('C. Observation Count per Mutation', fontsize=11, weight='bold', loc='left')
    ax.grid(axis='x', alpha=0.3)

    # Add legend
    single_patch = mpatches.Patch(color='#2E86AB', label='Single mutant')
    double_patch = mpatches.Patch(color='#A23B72', label='Double mutant')
    ax.legend(handles=[single_patch, double_patch], loc='lower right', fontsize=8)

    # Add study count as text
    for i, (n_obs, n_studies) in enumerate(zip(obs_df['n_observations'], obs_df['n_studies'])):
        ax.text(n_obs + 0.1, i, f"{n_studies} studies", va='center', ha='left', fontsize=6, color='gray', clip_on=False)

def create_harmonization_schematic(ax):
    """Panel D: Data harmonization schematic"""

    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Title
    ax.text(5, 9.5, 'D. Data Harmonization Pipeline', ha='center', fontsize=10, weight='bold')

    # Step 1: Raw data
    rect1 = mpatches.FancyBboxPatch((0.5, 7), 4, 1.5,
                                     boxstyle="round,pad=0.1",
                                     facecolor='#FFE6E6', edgecolor='black', linewidth=1.5)
    ax.add_patch(rect1)
    ax.text(2.5, 7.75, 'Raw Data Sources', ha='center', fontsize=9, weight='bold')
    ax.text(2.5, 7.3, '11 studies, heterogeneous formats\nFC, EC50, IC50, Kd',
            ha='center', fontsize=7)

    # Arrow
    ax.arrow(2.5, 6.9, 0, -0.5, head_width=0.3, head_length=0.2, fc='black', ec='black')

    # Step 2: Standardization
    rect2 = mpatches.FancyBboxPatch((0.5, 4.5), 4, 1.5,
                                     boxstyle="round,pad=0.1",
                                     facecolor='#FFF4E6', edgecolor='black', linewidth=1.5)
    ax.add_patch(rect2)
    ax.text(2.5, 5.25, 'Standardization', ha='center', fontsize=9, weight='bold')
    ax.text(2.5, 4.75, 'All values → log10(FC)', ha='center', fontsize=6.5)
    ax.text(2.5, 4.45, 'Context tier assignment', ha='center', fontsize=6.5)
    ax.text(2.5, 4.15, 'Quality scoring', ha='center', fontsize=6.5)

    # Arrow
    ax.arrow(2.5, 4.4, 0, -0.5, head_width=0.3, head_length=0.2, fc='black', ec='black')

    # Step 3: Harmonized
    rect3 = mpatches.FancyBboxPatch((0.5, 2), 4, 1.5,
                                     boxstyle="round,pad=0.1",
                                     facecolor='#E8F5E9', edgecolor='black', linewidth=1.5)
    ax.add_patch(rect3)
    ax.text(2.5, 2.75, 'Harmonized Dataset', ha='center', fontsize=9, weight='bold')
    ax.text(2.5, 2.3, '26 observations, 23 complete\nFull provenance tracking',
            ha='center', fontsize=7)

    # Metadata boxes on the right - single column layout to avoid overlap
    meta_items = [
        'Study source',
        'Assay type',
        'Subtype',
        'Context tier',
        'Quality score',
        'Provenance',
        'Observation ID',
        'Validation flags'
    ]

    # Draw single metadata box
    rect = mpatches.FancyBboxPatch((5.8, 1.5), 3.5, 7,
                                    boxstyle="round,pad=0.1",
                                    facecolor='#E8F4F8', edgecolor='gray',
                                    linewidth=1.5, linestyle='--')
    ax.add_patch(rect)
    ax.text(7.55, 8, 'Metadata Tracked:', ha='center', fontsize=7, weight='bold')

    # List items vertically
    y_start = 7.2
    for i, item in enumerate(meta_items):
        ax.text(6.2, y_start - i*0.65, f'• {item}', ha='left', fontsize=5.5)

    # Single arrow from middle box
    ax.arrow(4.6, 5, 1.1, 0, head_width=0.2, head_length=0.15,
            fc='gray', ec='gray', linestyle='--', alpha=0.5, linewidth=1.5)

def main():
    """Generate Figure 1"""
    print("="*60)
    print("Generating Figure 1: Evidence Landscape")
    print("="*60)

    # Create figure with 4 panels
    fig = plt.figure(figsize=(20, 15))
    gs = GridSpec(2, 2, figure=fig, hspace=0.5, wspace=0.45)

    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    ax3 = fig.add_subplot(gs[1, 0])
    ax4 = fig.add_subplot(gs[1, 1])

    # Generate panels
    print("\nPanel A: PRISMA flow...")
    create_prisma_flow(ax1)

    print("Panel B: Availability matrix...")
    create_availability_matrix(ax2)

    print("Panel C: Observation counts...")
    create_observation_counts(ax3)

    print("Panel D: Harmonization schematic...")
    create_harmonization_schematic(ax4)

    # Save
    plt.tight_layout()

    output_pdf = OUTPUT_DIR / "figure1_evidence_landscape.pdf"
    output_png = OUTPUT_DIR / "figure1_evidence_landscape.png"

    fig.savefig(output_pdf, dpi=300, bbox_inches='tight', pad_inches=0.3)
    fig.savefig(output_png, dpi=300, bbox_inches='tight', pad_inches=0.3)

    print(f"\n[OK] Saved: {output_pdf}")
    print(f"[OK] Saved: {output_png}")
    print("\n" + "="*60)
    print("Figure 1 complete!")
    print("="*60)

    plt.close()

if __name__ == "__main__":
    main()
