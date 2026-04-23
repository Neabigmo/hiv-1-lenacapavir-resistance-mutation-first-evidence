#!/usr/bin/env python3
"""
Figure 4: Structure-Informed Mechanism (Integrated with HTML renders)
3 panels: A+B from HTML, C perturbation summary
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
HTML_RENDER_DIR = OUTPUT_DIR / "html_renders"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

plt.style.use('seaborn-v0_8-paper')

def create_perturbation_summary(ax):
    """Panel C: Structural perturbation summary scores"""

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

    # Create figure with 2 panels (A+B from HTML, C from matplotlib)
    fig = plt.figure(figsize=(20, 12))
    gs = GridSpec(2, 1, figure=fig, hspace=0.4, height_ratios=[1.2, 1])

    ax1 = fig.add_subplot(gs[0, :])
    ax2 = fig.add_subplot(gs[1, :])

    # Panel A+B: Load HTML render
    print("\nPanel A+B: Loading HTML render...")
    html_render = HTML_RENDER_DIR / "figure4_ab.png"
    if html_render.exists():
        img = Image.open(html_render)
        ax1.imshow(img)
        ax1.axis('off')
        print("[OK] HTML render loaded")
    else:
        ax1.text(0.5, 0.5, 'HTML render not found\nRun render_html_figures.py first',
                ha='center', va='center', transform=ax1.transAxes, fontsize=12)
        ax1.axis('off')
        print("[WARN] HTML render not found")

    # Panel C: Perturbation summary
    print("Panel C: Perturbation summary...")
    create_perturbation_summary(ax2)

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
