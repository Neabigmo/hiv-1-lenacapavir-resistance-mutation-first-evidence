#!/usr/bin/env python3
"""
Figure 3: Interactions & Context-Dependent Combinations
Focused 3-panel layout: context variability, combination network, and evidence labels.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.gridspec import GridSpec
import matplotlib.patches as mpatches
import networkx as nx
from pathlib import Path

# Setup
BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "data" / "processed" / "revision_v2"
RESULTS_DIR = BASE_DIR / "results" / "revision_v2"
OUTPUT_DIR = BASE_DIR / "manuscript" / "figures" / "revision_v2"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

plt.style.use('seaborn-v0_8-paper')

def create_observed_vs_expected(ax):
    """Panel A: Observed vs expected scatter for double mutants"""

    # Load epistasis data
    epi_df = pd.read_csv(RESULTS_DIR / "epistasis_matrix.csv")
    epi_df = epi_df[epi_df['expected_log10fc'].notna()].copy()

    # Scatter plot
    colors = []
    for itype in epi_df['interaction_type']:
        if itype == 'positive_synergy':
            colors.append('#E74C3C')
        elif itype == 'additive':
            colors.append('#95A5A6')
        else:
            colors.append('#3498DB')

    ax.scatter(epi_df['expected_log10fc'], epi_df['observed_log10fc'],
              c=colors, s=150, alpha=0.7, edgecolors='black', linewidth=1.5)

    # Add labels
    for _, row in epi_df.iterrows():
        ax.annotate(row['combination'],
                   (row['expected_log10fc'], row['observed_log10fc']),
                   xytext=(8, 8), textcoords='offset points',
                   fontsize=6, alpha=0.8, rotation=15, clip_on=False)

    # Diagonal line (additive expectation)
    max_val = max(epi_df['expected_log10fc'].max(), epi_df['observed_log10fc'].max())
    ax.plot([0, max_val], [0, max_val], 'k--', alpha=0.5, linewidth=2, label='Additive')

    # Shaded regions
    ax.fill_between([0, max_val], [0, max_val], [0, max_val*1.5],
                    alpha=0.1, color='red', label='Positive synergy')
    ax.fill_between([0, max_val], [0, 0], [0, max_val],
                    alpha=0.1, color='blue', label='Negative synergy')

    ax.set_xlabel('Expected log10(FC)\n(Additive)', fontsize=9, weight='bold')
    ax.set_ylabel('Observed log10(FC)', fontsize=9, weight='bold')
    ax.set_title('A. Epistasis: Observed vs Expected', fontsize=10, weight='bold', loc='left')
    ax.legend(fontsize=7, loc='upper left')
    ax.grid(alpha=0.3)

def create_interaction_heatmap(ax):
    """Panel B: Epistasis summary bar chart"""

    # Load epistasis data
    epi_df = pd.read_csv(RESULTS_DIR / "epistasis_matrix.csv")
    epi_df = epi_df[epi_df['interaction_residual'].notna()].copy()
    epi_df = epi_df.sort_values('interaction_residual', ascending=True)

    # Create horizontal bar chart
    colors = ['#3498DB' if res < -0.3 else '#E74C3C' if res > 0.3 else '#95A5A6'
              for res in epi_df['interaction_residual']]

    bars = ax.barh(range(len(epi_df)), epi_df['interaction_residual'],
                   color=colors, alpha=0.8, edgecolor='black', linewidth=1)

    ax.set_yticks(range(len(epi_df)))
    ax.set_yticklabels(epi_df['combination'], fontsize=7)
    ax.set_xlabel('Epistatic Residual (log10 scale)', fontsize=9, weight='bold')
    ax.set_title('B. Epistatic Interactions', fontsize=10, weight='bold', loc='left')
    ax.axvline(x=0, color='black', linestyle='-', linewidth=1.5, alpha=0.5)
    ax.axvline(x=0.3, color='red', linestyle='--', linewidth=1, alpha=0.5)
    ax.axvline(x=-0.3, color='blue', linestyle='--', linewidth=1, alpha=0.5)
    ax.grid(axis='x', alpha=0.3)

    # Add legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#E74C3C', label='Positive synergy (>0.3)'),
        Patch(facecolor='#3498DB', label='Compensatory (<-0.3)'),
        Patch(facecolor='#95A5A6', label='Additive (-0.3 to 0.3)')
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=6)

def create_context_specific_plot(ax):
    """Panel A: Q67H+K70R context-specific observations"""

    # Load context-specific data
    context_df = pd.read_csv(RESULTS_DIR / "context_specific_combinations.csv")
    q67h_k70r = context_df[context_df['combination'] == 'Q67H+K70R'].copy()

    if len(q67h_k70r) == 0:
        ax.text(0.5, 0.5, 'No Q67H+K70R data', ha='center', va='center')
        ax.set_title('A. Context-Dependent: Q67H+K70R', fontsize=11, weight='bold', loc='left')
        return

    # Sort by FC
    q67h_k70r = q67h_k70r.sort_values('FC')

    # Create bar plot
    colors = {'clinical': '#E74C3C', 'in_vitro': '#3498DB', 'natural_polymorphism': '#2ECC71'}
    bar_colors = [colors.get(ctx, 'gray') for ctx in q67h_k70r['context']]

    bars = ax.bar(range(len(q67h_k70r)), q67h_k70r['FC'], color=bar_colors, alpha=0.8,
                  edgecolor='black', linewidth=1.5)

    # Add labels
    labels = [f"{row['study']}\n({row['context']})"
              for _, row in q67h_k70r.iterrows()]
    ax.set_xticks(range(len(q67h_k70r)))
    ax.set_xticklabels(labels, fontsize=8, rotation=0)

    # Add FC values on bars
    for i, (bar, fc) in enumerate(zip(bars, q67h_k70r['FC'])):
        ax.text(bar.get_x() + bar.get_width()/2, fc + 2,
               f'{fc:.1f}×', ha='center', fontsize=9, weight='bold')

    ax.set_ylabel('Fold-Change', fontsize=9, weight='bold')
    ax.set_title('A. Context-Dependent: Q67H+K70R', fontsize=10, weight='bold', loc='left')
    ax.set_ylim(0, max(q67h_k70r['FC']) * 1.2)
    ax.grid(axis='y', alpha=0.3)

    # Add range annotation
    fc_range = q67h_k70r['FC'].max() / q67h_k70r['FC'].min()
    ax.text(0.5, 0.95, f'{fc_range:.1f}-fold variation across contexts',
           transform=ax.transAxes, ha='center', va='top',
           bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.3),
           fontsize=8, weight='bold')

def create_m66i_network(ax):
    """Panel B: M66I-centered combination network"""

    # Load compensatory data
    comp_df = pd.read_csv(RESULTS_DIR / "compensatory_patterns.csv")

    # Create network
    G = nx.Graph()

    # Add M66I as central node
    G.add_node('M66I', node_type='primary', fc=3200)

    # Add combinations
    for _, row in comp_df.iterrows():
        combo = row['combination']
        fc = row['observed_fc']
        pattern = row['pattern']

        # Parse combination
        parts = combo.split('+')
        if 'M66I' in parts:
            other_muts = [p for p in parts if p != 'M66I']
            combo_name = '+'.join(other_muts)

            G.add_node(combo_name, node_type='compensatory' if 'compensatory' in pattern else 'other',
                      fc=fc)
            G.add_edge('M66I', combo_name, weight=fc)

    # Layout
    pos = nx.spring_layout(G, k=2, iterations=50)

    # Draw nodes
    node_colors = []
    node_sizes = []
    for node in G.nodes():
        if node == 'M66I':
            node_colors.append('#E74C3C')
            node_sizes.append(2000)
        elif G.nodes[node]['node_type'] == 'compensatory':
            node_colors.append('#2ECC71')
            node_sizes.append(1500)
        else:
            node_colors.append('#3498DB')
            node_sizes.append(1500)

    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes,
                          alpha=0.8, edgecolors='black', linewidths=2, ax=ax)

    # Draw edges
    nx.draw_networkx_edges(G, pos, width=2, alpha=0.5, ax=ax)

    # Draw labels - use original positions to ensure visibility
    nx.draw_networkx_labels(G, pos, font_size=8, font_weight='bold', ax=ax,
                           bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                                    edgecolor='none', alpha=0.7))

    # Add FC labels on edges
    edge_labels = {}
    for u, v, data in G.edges(data=True):
        fc = data['weight']
        edge_labels[(u, v)] = f"{fc:.0f}×"

    nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=6, ax=ax)

    ax.set_title('B. M66I Combination Network', fontsize=10, weight='bold', loc='left')
    ax.axis('off')

    # Legend - move to upper left to avoid data
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#E74C3C', label='Primary resistant'),
        Patch(facecolor='#2ECC71', label='Putative compensatory'),
        Patch(facecolor='#3498DB', label='Other combination')
    ]
    ax.legend(handles=legend_elements, loc='upper left', fontsize=7)

def create_claim_labels(ax):
    """Panel C: Mutation classification by evidence strength"""

    # Load classifications
    class_df = pd.read_csv(RESULTS_DIR / "mutation_classifications.csv")

    # Count by category and evidence
    summary = class_df.groupby(['category', 'evidence_strength']).size().reset_index(name='count')

    # Create grouped bar chart
    categories = summary['category'].unique()
    evidence_levels = ['strong', 'moderate', 'hypothesis_generating']
    evidence_colors = {'strong': '#27AE60', 'moderate': '#F39C12', 'hypothesis_generating': '#E74C3C'}

    x = np.arange(len(categories))
    width = 0.25

    for i, evidence in enumerate(evidence_levels):
        counts = []
        for cat in categories:
            subset = summary[(summary['category'] == cat) & (summary['evidence_strength'] == evidence)]
            counts.append(subset['count'].sum() if len(subset) > 0 else 0)

        ax.bar(x + i*width, counts, width, label=evidence.replace('_', ' ').title(),
              color=evidence_colors[evidence], alpha=0.8, edgecolor='black', linewidth=1)

    ax.set_xlabel('Mutation Category', fontsize=9, weight='bold')
    ax.set_ylabel('Count', fontsize=9, weight='bold')
    ax.set_title('C. Evidence Strength by Category', fontsize=10, weight='bold', loc='left')
    ax.set_xticks(x + width)
    ax.set_xticklabels([c.replace('_', ' ').title() for c in categories],
                       rotation=45, ha='right', fontsize=7)
    ax.legend(fontsize=7, title='Evidence Strength')
    ax.grid(axis='y', alpha=0.3)

def main():
    """Generate Figure 3"""
    print("="*60)
    print("Generating Figure 3: Interactions & Context")
    print("="*60)

    # Create figure: keep only high-information panels in one row.
    fig = plt.figure(figsize=(20, 6.8), constrained_layout=True)
    gs = GridSpec(1, 3, figure=fig, hspace=0.25, wspace=0.35)

    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    ax3 = fig.add_subplot(gs[0, 2])

    # Generate panels
    print("\nPanel A: Q67H+K70R context...")
    create_context_specific_plot(ax1)

    print("Panel B: M66I network...")
    create_m66i_network(ax2)

    print("Panel C: Claim labels...")
    create_claim_labels(ax3)

    # Save
    output_pdf = OUTPUT_DIR / "figure3_interactions.pdf"
    output_png = OUTPUT_DIR / "figure3_interactions.png"

    fig.savefig(output_pdf, dpi=300, bbox_inches='tight', pad_inches=0.3)
    fig.savefig(output_png, dpi=300, bbox_inches='tight', pad_inches=0.3)

    print(f"\n[OK] Saved: {output_pdf}")
    print(f"[OK] Saved: {output_png}")
    print("\n" + "="*60)
    print("Figure 3 complete!")
    print("="*60)

    plt.close()

if __name__ == "__main__":
    main()
