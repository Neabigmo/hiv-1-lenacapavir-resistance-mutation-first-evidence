#!/usr/bin/env python3
"""
Figure 1: Evidence Landscape (Improved Academic Design)
4 panels showing PRISMA flow, availability matrix, observation counts, harmonization
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
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
    """Panel A: PRISMA-style flow diagram with improved design"""

    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Color scheme
    color_identification = '#E3F2FD'
    color_screening = '#FFF3E0'
    color_included = '#E8F5E9'
    color_excluded = '#FFEBEE'

    # Helper function for gradient boxes
    def draw_box(x, y, w, h, text, count, color, edge_color='#333', edge_width=2):
        box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05",
                            facecolor=color, edgecolor=edge_color,
                            linewidth=edge_width, zorder=2)
        ax.add_patch(box)

        # Text
        lines = text.split('\n')
        if len(lines) == 1:
            ax.text(x + w/2, y + h*0.62, text, ha='center', va='center',
                   fontsize=8.5, weight='600', zorder=3)
            ax.text(x + w/2, y + h*0.30, f'(n = {count})', ha='center', va='center',
                   fontsize=9.5, weight='bold', zorder=3)
        else:
            # Use relative positions to avoid overlap in compact boxes.
            ax.text(x + w/2, y + h*0.72, lines[0], ha='center', va='center',
                   fontsize=8.2, weight='600', zorder=3)
            if len(lines) > 1:
                ax.text(x + w/2, y + h*0.48, lines[1], ha='center', va='center',
                       fontsize=7.6, weight='500', zorder=3)
            if len(lines) > 2:
                ax.text(x + w/2, y + h*0.28, lines[2], ha='center', va='center',
                       fontsize=7.2, weight='500', zorder=3)
            ax.text(x + w/2, y + h*0.10, f'(n = {count})', ha='center', va='center',
                   fontsize=9.2, weight='bold', zorder=3)

    # Phase labels
    ax.text(0.3, 9.5, 'IDENTIFICATION', fontsize=11, weight='bold',
           color='#1976D2', style='italic')
    ax.text(0.3, 6.8, 'SCREENING', fontsize=11, weight='bold',
           color='#F57C00', style='italic')
    ax.text(0.3, 3.5, 'INCLUDED', fontsize=11, weight='bold',
           color='#388E3C', style='italic')

    # Identification boxes
    draw_box(1, 8.5, 3, 0.8, 'Database searching\n(PubMed)', 82, color_identification, '#1976D2', 2.5)
    draw_box(6, 8.5, 3, 0.8, 'Other sources\n(References)', 5, color_identification, '#1976D2', 2.5)

    # Arrow down
    arrow1 = FancyArrowPatch((5, 8.4), (5, 7.8), arrowstyle='->', mutation_scale=20,
                            linewidth=3, color='#333', zorder=1)
    ax.add_patch(arrow1)

    # After deduplication
    draw_box(2.5, 7.2, 5, 0.8, 'Records after\ndeduplication', 78, color_identification, '#1976D2', 2.5)

    arrow2 = FancyArrowPatch((5, 7.1), (5, 6.5), arrowstyle='->', mutation_scale=20,
                            linewidth=3, color='#333', zorder=1)
    ax.add_patch(arrow2)

    # Screening
    draw_box(2.5, 5.9, 5, 0.8, 'Title/abstract\nscreened', 78, color_screening, '#F57C00', 2.5)

    # Exclusion 1
    draw_box(8, 5.85, 1.8, 0.7, 'Excluded', 56, color_excluded, '#D32F2F', 2)
    ax.text(8.9, 5.6, 'Not relevant', ha='center', fontsize=7, style='italic', color='#666')
    arrow_ex1 = FancyArrowPatch((7.5, 6.25), (8, 6.25), arrowstyle='->', mutation_scale=15,
                               linewidth=2, color='#D32F2F', linestyle='--', zorder=1)
    ax.add_patch(arrow_ex1)

    arrow3 = FancyArrowPatch((5, 5.8), (5, 5.2), arrowstyle='->', mutation_scale=20,
                            linewidth=3, color='#333', zorder=1)
    ax.add_patch(arrow3)

    # Full-text assessment
    draw_box(2.5, 4.6, 5, 0.8, 'Full-text articles\nassessed', 22, color_screening, '#F57C00', 2.5)

    # Exclusion 2
    draw_box(8, 4.4, 1.8, 1, 'Excluded', 11, color_excluded, '#D32F2F', 2)
    ax.text(8.9, 4.15, 'No quant: 8', ha='center', fontsize=6.5, color='#666')
    ax.text(8.9, 3.95, 'HIV-2: 3', ha='center', fontsize=6.5, color='#666')
    arrow_ex2 = FancyArrowPatch((7.5, 5), (8, 5), arrowstyle='->', mutation_scale=15,
                               linewidth=2, color='#D32F2F', linestyle='--', zorder=1)
    ax.add_patch(arrow_ex2)

    arrow4 = FancyArrowPatch((5, 4.5), (5, 3.9), arrowstyle='->', mutation_scale=20,
                            linewidth=3, color='#333', zorder=1)
    ax.add_patch(arrow4)

    # Qualitative synthesis
    draw_box(2.5, 3.3, 5, 0.8, 'Qualitative\nsynthesis', 11, color_included, '#388E3C', 2.5)

    arrow5 = FancyArrowPatch((5, 3.2), (5, 2.6), arrowstyle='->', mutation_scale=20,
                            linewidth=3, color='#333', zorder=1)
    ax.add_patch(arrow5)

    # Quantitative synthesis
    draw_box(2.5, 2, 5, 0.8, 'Quantitative synthesis\n(meta-analysis)', 11, color_included, '#388E3C', 2.5)

    ax.set_title('A. PRISMA Evidence Flow', fontsize=12, weight='bold', loc='left', pad=10)

def create_availability_matrix(ax):
    """Panel B: Mutation × Subtype × Context availability matrix"""

    # Load data
    avail_df = pd.read_csv(DATA_DIR / "availability_matrix.csv")

    # Create pivot table
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
    ax.set_title('B. Data Availability Matrix', fontsize=12, weight='bold', loc='left', pad=10)
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
    ax.set_title('C. Observation Count per Mutation', fontsize=12, weight='bold', loc='left', pad=10)
    ax.grid(axis='x', alpha=0.3)

    # Add legend
    single_patch = mpatches.Patch(color='#2E86AB', label='Single mutant')
    double_patch = mpatches.Patch(color='#A23B72', label='Double mutant')
    ax.legend(handles=[single_patch, double_patch], loc='lower right', fontsize=8)

    # Add study count as text
    for i, (n_obs, n_studies) in enumerate(zip(obs_df['n_observations'], obs_df['n_studies'])):
        ax.text(n_obs + 0.1, i, f"{n_studies} studies", va='center', ha='left', fontsize=6, color='gray', clip_on=False)

def create_harmonization_schematic(ax):
    """Panel D: Data harmonization schematic with improved design"""

    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Color scheme
    color_raw = '#FFEBEE'
    color_std = '#FFF3E0'
    color_harm = '#E8F5E9'
    color_meta = '#E3F2FD'

    # Helper function
    def draw_stage_box(x, y, w, h, title, content_lines, color, edge_color):
        box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08",
                            facecolor=color, edgecolor=edge_color,
                            linewidth=2.5, zorder=2)
        ax.add_patch(box)

        # Title
        ax.text(x + w/2, y + h - 0.25, title, ha='center', va='top',
               fontsize=10, weight='bold', zorder=3)

        # Content
        y_start = y + h - 0.55
        for i, line in enumerate(content_lines):
            ax.text(x + w/2, y_start - i*0.22, line, ha='center', va='top',
                   fontsize=7.5, zorder=3)

    # Stage 1: Raw data
    draw_stage_box(0.5, 7, 4, 1.8, 'Raw Data Sources',
                  ['11 studies, heterogeneous formats',
                   'FC, EC₅₀, IC₅₀, Kd'],
                  color_raw, '#E53935')

    # Arrow
    arrow1 = FancyArrowPatch((2.5, 6.9), (2.5, 6.3), arrowstyle='->', mutation_scale=25,
                            linewidth=3, color='#333', zorder=1)
    ax.add_patch(arrow1)

    # Stage 2: Standardization
    draw_stage_box(0.5, 4.5, 4, 1.8, 'Standardization',
                  ['All values → log₁₀(FC)',
                   'Context tier assignment',
                   'Quality scoring'],
                  color_std, '#FB8C00')

    # Arrow
    arrow2 = FancyArrowPatch((2.5, 4.4), (2.5, 3.8), arrowstyle='->', mutation_scale=25,
                            linewidth=3, color='#333', zorder=1)
    ax.add_patch(arrow2)

    # Stage 3: Harmonized
    draw_stage_box(0.5, 2, 4, 1.8, 'Harmonized Dataset',
                  ['26 observations (23 complete)',
                   'Full provenance tracking'],
                  color_harm, '#43A047')

    # Metadata box
    meta_box = FancyBboxPatch((5.5, 2), 4, 6.8, boxstyle="round,pad=0.1",
                             facecolor=color_meta, edgecolor='#1976D2',
                             linewidth=2, linestyle='--', zorder=2)
    ax.add_patch(meta_box)

    ax.text(7.5, 8.3, 'Metadata Tracked', ha='center', fontsize=10,
           weight='bold', color='#1565C0', zorder=3)

    metadata_items = [
        'Study source', 'Assay type', 'HIV-1 subtype',
        'Context tier', 'Quality score', 'Provenance chain',
        'Observation ID', 'Validation flags'
    ]

    y_start = 7.8
    for i, item in enumerate(metadata_items):
        ax.text(5.8, y_start - i*0.7, f'✓ {item}', ha='left', fontsize=7,
               color='#37474F', zorder=3)

    # Connection arrow
    arrow_meta = FancyArrowPatch((4.6, 5.5), (5.4, 5.5), arrowstyle='->', mutation_scale=20,
                                linewidth=2, color='#607D8B', linestyle='--', zorder=1)
    ax.add_patch(arrow_meta)

    ax.set_title('D. Data Harmonization Pipeline', fontsize=12, weight='bold', loc='left', pad=10)

def main():
    """Generate Figure 1"""
    print("="*60)
    print("Generating Figure 1: Evidence Landscape (Improved Design)")
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
