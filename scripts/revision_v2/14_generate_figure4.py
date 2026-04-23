#!/usr/bin/env python3
"""
Figure 4: Structure-Informed Mechanism
6 panels: overview, N57H, M66I, Q67H+N74D, compensatory, perturbation summary
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.gridspec import GridSpec
from pathlib import Path
from PIL import Image

# Setup
BASE_DIR = Path(__file__).parent.parent.parent
RESULTS_DIR = BASE_DIR / "results" / "revision_v2"
OUTPUT_DIR = BASE_DIR / "manuscript" / "figures" / "revision_v2"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

plt.style.use('seaborn-v0_8-paper')

def create_structure_overview(ax):
    """Panel A: Schematic overview of LEN-CA complex"""

    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8.5)
    ax.axis('off')

    # Title
    ax.text(5, 8.2, 'A. LEN-CA Hexamer Complex (PDB: 6VKV)',
           ha='center', fontsize=13, weight='bold')

    # Draw hexamer schematic
    from matplotlib.patches import RegularPolygon, Circle
    import matplotlib.patches as mpatches

    # Central hexagon (hexamer)
    hexagon = RegularPolygon((4.7, 4.1), 6, radius=2.45,
                            facecolor='#E8F4F8', edgecolor='black', linewidth=2)
    ax.add_patch(hexagon)

    # LEN molecule in center
    len_circle = Circle((4.7, 4.1), 0.72, facecolor='#E74C3C', edgecolor='black', linewidth=2)
    ax.add_patch(len_circle)
    ax.text(4.7, 4.1, 'LEN', ha='center', va='center', fontsize=11, weight='bold', color='white')

    # Key residues around hexamer
    residues = [
        (4.7, 6.35, 'N57', '#27AE60'),
        (6.95, 5.45, 'M66', '#E74C3C'),
        (6.95, 2.75, 'Q67', '#F39C12'),
        (4.7, 1.9, 'N74', '#3498DB'),
        (2.45, 2.75, 'K70', '#9B59B6'),
        (2.45, 5.45, 'A105/T107', '#95A5A6'),
    ]

    for x, y, label, color in residues:
        circle = Circle((x, y), 0.52, facecolor=color, edgecolor='black', linewidth=1.5, alpha=0.9)
        ax.add_patch(circle)
        ax.text(x, y, label, ha='center', va='center', fontsize=8.5, weight='bold')

    # Binding site annotation: shorten arrows and point to explicit residues.
    ann1 = ax.annotate('Hydrophobic\nPocket', xy=(7.25, 5.25), xytext=(8.2, 6.25),
               arrowprops=dict(arrowstyle='-|>', lw=1.9, color='red',
                               connectionstyle='arc3,rad=-0.18'),
               fontsize=9.5, weight='bold', color='red',
               bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.9))
    # Keep arrow beneath residue labels to avoid covering text.
    ann1.arrow_patch.set_zorder(1)
    ann1.set_zorder(5)

    ann2 = ax.annotate('NTD-CTD\nInterface', xy=(7.25, 2.55), xytext=(8.2, 1.95),
               arrowprops=dict(arrowstyle='-|>', lw=1.9, color='blue',
                               connectionstyle='arc3,rad=0.18'),
               fontsize=9.5, weight='bold', color='blue',
               bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.9))
    ann2.arrow_patch.set_zorder(1)
    ann2.set_zorder(5)

def create_combined_mechanism_panel(ax):
    """Panel B: Combined mechanism schematic (replaces old B-E)"""

    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8.5)
    ax.axis('off')

    # Title
    ax.text(5, 8.2, 'B. Resistance Mechanisms Overview', ha='center', fontsize=13, weight='bold')

    # Draw LEN-CA interface schematic (simplified)
    from matplotlib.patches import Rectangle, Circle, FancyBboxPatch

    # Central binding pocket
    pocket = Rectangle((3.5, 3.1), 3.0, 2.2, facecolor='#E8F4F8', edgecolor='black', linewidth=2, alpha=0.35)
    ax.add_patch(pocket)
    ax.text(5, 4.2, 'LEN Binding\nPocket', ha='center', fontsize=10, weight='bold')

    # Mechanism 1: N57H (top-left, green)
    region1 = FancyBboxPatch((0.6, 5.6), 2.5, 1.7, boxstyle="round,pad=0.1",
                             facecolor='#27AE60', alpha=0.25, edgecolor='#27AE60', linewidth=2)
    ax.add_patch(region1)
    ax.text(1.85, 6.95, 'N57H', ha='center', fontsize=11, weight='bold', color='#27AE60')
    ax.text(1.85, 6.45, 'H-bond loss', ha='center', fontsize=9)
    ax.text(1.85, 6.0, '2 H-bonds lost', ha='center', fontsize=8)
    ax.text(1.85, 5.7, 'ΔΔG: +4.5', ha='center', fontsize=8, style='italic')

    # Mechanism 2: M66I (top-right, red)
    region2 = FancyBboxPatch((6.9, 5.6), 2.5, 1.7, boxstyle="round,pad=0.1",
                             facecolor='#E74C3C', alpha=0.25, edgecolor='#E74C3C', linewidth=2)
    ax.add_patch(region2)
    ax.text(8.15, 6.95, 'M66I', ha='center', fontsize=11, weight='bold', color='#E74C3C')
    ax.text(8.15, 6.45, 'Steric clash', ha='center', fontsize=9)
    ax.text(8.15, 6.0, 'β-branch clash', ha='center', fontsize=8)
    ax.text(8.15, 5.7, 'ΔΔG: +5.2', ha='center', fontsize=8, style='italic')

    # Mechanism 3: Q67H+N74D (bottom-left, orange)
    region3 = FancyBboxPatch((0.6, 1.3), 2.5, 1.7, boxstyle="round,pad=0.1",
                             facecolor='#F39C12', alpha=0.25, edgecolor='#F39C12', linewidth=2)
    ax.add_patch(region3)
    ax.text(1.85, 2.65, 'Q67H+N74D', ha='center', fontsize=11, weight='bold', color='#F39C12')
    ax.text(1.85, 2.2, 'Dual effect', ha='center', fontsize=9)
    ax.text(1.85, 1.8, 'Conformational + electrostatic', ha='center', fontsize=7.8)
    ax.text(1.85, 1.45, 'ΔΔG: +6.5', ha='center', fontsize=8, style='italic')

    # Mechanism 4: Compensatory (bottom-right, light green)
    region4 = FancyBboxPatch((6.9, 1.3), 2.5, 1.7, boxstyle="round,pad=0.1",
                             facecolor='#2ECC71', alpha=0.25, edgecolor='#2ECC71', linewidth=2)
    ax.add_patch(region4)
    ax.text(8.15, 2.65, 'A105T/T107A', ha='center', fontsize=11, weight='bold', color='#2ECC71')
    ax.text(8.15, 2.2, 'Compensatory', ha='center', fontsize=9)
    ax.text(8.15, 1.8, 'Restores fitness with M66I', ha='center', fontsize=7.8)
    ax.text(8.15, 1.45, 'ΔΔG: +4.0', ha='center', fontsize=8, style='italic')

    # Short, directed arrows from each mechanism box into the central pocket.
    arrow_style = dict(arrowstyle='-|>', lw=2.4, alpha=0.9)
    ax.annotate('', xy=(3.65, 4.85), xytext=(3.05, 5.7), arrowprops={**arrow_style, 'color': '#27AE60'})
    ax.annotate('', xy=(6.35, 4.85), xytext=(6.95, 5.7), arrowprops={**arrow_style, 'color': '#E74C3C'})
    ax.annotate('', xy=(3.65, 3.55), xytext=(3.05, 2.9), arrowprops={**arrow_style, 'color': '#F39C12'})
    ax.annotate('', xy=(6.35, 3.55), xytext=(6.95, 2.9), arrowprops={**arrow_style, 'color': '#2ECC71'})

def create_perturbation_summary(ax):
    """Panel F: Structural perturbation summary scores"""

    # Load data
    struct_df = pd.read_csv(RESULTS_DIR / "structural_perturbation_scores.csv")
    struct_df = struct_df.sort_values('perturbation_score', ascending=True)

    # Create horizontal bar plot
    colors = ['#E74C3C' if score > 7 else '#F39C12' if score > 5 else '#3498DB'
              for score in struct_df['perturbation_score']]

    bars = ax.barh(range(len(struct_df)), struct_df['perturbation_score'],
                   color=colors, alpha=0.8, edgecolor='black', linewidth=1)

    ax.set_yticks(range(len(struct_df)))
    ax.set_yticklabels(struct_df['mutation'], fontsize=7)
    ax.set_xlabel('Structural Perturbation Score', fontsize=9, weight='bold')
    ax.set_title('C. Perturbation Summary', fontsize=10, weight='bold', loc='left')
    ax.grid(axis='x', alpha=0.3)

    # Add mechanism labels
    for i, (score, mech) in enumerate(zip(struct_df['perturbation_score'], struct_df['mechanism'])):
        ax.text(score + 0.3, i, mech.replace('_', ' ').title(),
               va='center', fontsize=6, style='italic', color='gray', clip_on=False)

    # Add threshold lines
    ax.axvline(x=5, color='orange', linestyle='--', alpha=0.5, linewidth=2)
    ax.axvline(x=7, color='red', linestyle='--', alpha=0.5, linewidth=2)

    # Legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#E74C3C', label='High (>7)'),
        Patch(facecolor='#F39C12', label='Moderate (5-7)'),
        Patch(facecolor='#3498DB', label='Low (<5)')
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=8, title='Perturbation')

def main():
    """Generate Figure 4"""
    print("="*60)
    print("Generating Figure 4: Structure-Informed Mechanism")
    print("="*60)

    # Layout: A and B on one row; C spans the second row.
    fig = plt.figure(figsize=(20, 11))
    gs = GridSpec(2, 2, figure=fig, height_ratios=[1.35, 1.0], hspace=0.35, wspace=0.22)

    ax1 = fig.add_subplot(gs[0, 0])  # A
    ax2 = fig.add_subplot(gs[0, 1])  # B
    ax3 = fig.add_subplot(gs[1, :])  # C

    # Generate panels
    print("\nPanel A: Structure overview...")
    create_structure_overview(ax1)

    print("Panel B: Combined mechanism schematic...")
    create_combined_mechanism_panel(ax2)

    print("Panel C: Perturbation summary...")
    create_perturbation_summary(ax3)

    # Save
    plt.tight_layout()

    output_pdf = OUTPUT_DIR / "figure4_structure.pdf"
    output_png = OUTPUT_DIR / "figure4_structure.png"

    fig.savefig(output_pdf, dpi=300, bbox_inches='tight', pad_inches=0.3)
    fig.savefig(output_png, dpi=300, bbox_inches='tight', pad_inches=0.3)

    print(f"\n[OK] Saved: {output_pdf}")
    print(f"[OK] Saved: {output_png}")
    print("\n" + "="*60)
    print("Figure 4 complete!")
    print("="*60)

    plt.close()

if __name__ == "__main__":
    main()
