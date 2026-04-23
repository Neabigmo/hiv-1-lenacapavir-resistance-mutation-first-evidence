import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from scipy import stats
from pathlib import Path

NATURE_COLORS = {'primary': '#E64B35', 'secondary': '#4DBBD5', 'tertiary': '#00A087', 'quaternary': '#3C5488'}

plt.rcParams.update({'figure.dpi': 600, 'savefig.dpi': 600, 'font.family': 'Arial', 'font.size': 8, 
                     'axes.linewidth': 0.5, 'legend.frameon': False, 'axes.spines.top': False, 'axes.spines.right': False})

effects = pd.read_csv('results/phase2/mutation_effects_simplified.csv')
ci = pd.read_csv('results/phase2/bootstrap_ci.csv')
struct = pd.read_csv('results/phase2/structure_resistance_merged.csv')
fitness = pd.read_csv('results/phase2/fitness_resistance_data.csv')

fig = plt.figure(figsize=(7.5, 9))
gs = GridSpec(3, 2, figure=fig, hspace=0.4, wspace=0.3, height_ratios=[1, 1.2, 1])

# Panel A: Violin plot
ax1 = fig.add_subplot(gs[0, :])
data_ctx = struct.groupby('Context')['log10_FC'].apply(list)
parts = ax1.violinplot([data_ctx.get('Clinical', []), data_ctx.get('In_vitro', [])], positions=[0, 1], widths=0.6, showmeans=True)
for pc, col in zip(parts['bodies'], [NATURE_COLORS['primary'], NATURE_COLORS['secondary']]):
    pc.set_facecolor(col); pc.set_alpha(0.7); pc.set_edgecolor('black'); pc.set_linewidth(0.5)
ax1.set_xticks([0, 1]); ax1.set_xticklabels(['Clinical (n=3)', 'In vitro (n=14)'], fontsize=8)
ax1.set_ylabel('log₁₀(Fold Change)', fontsize=9, fontweight='bold')
ax1.set_title('A', loc='left', fontsize=11, fontweight='bold', x=-0.15)
ax1.grid(axis='y', alpha=0.3, linewidth=0.5); ax1.set_ylim(-0.5, 4.5)

# Panel B: Forest plot
ax2 = fig.add_subplot(gs[1, :])
data = effects.merge(ci, left_index=True, right_index=True)
data = data[data['count'] > 0].sort_values('FC_mean', ascending=True)
colors = [NATURE_COLORS['primary'] if fc>1000 else NATURE_COLORS['secondary'] if fc>100 else NATURE_COLORS['tertiary'] if fc>10 else NATURE_COLORS['quaternary'] for fc in data['FC_mean']]
y_pos = np.arange(len(data))
for i, (idx, row) in enumerate(data.iterrows()):
    xerr_l = max(row['FC_mean'] - row['FC_CI_lower'], 0); xerr_u = max(row['FC_CI_upper'] - row['FC_mean'], 0)
    ax2.errorbar(row['FC_mean'], i, xerr=[[xerr_l], [xerr_u]], fmt='o', color=colors[i], markersize=7, capsize=3, elinewidth=1.5, alpha=0.8)
ax2.set_yticks(y_pos); ax2.set_yticklabels(data.index, fontsize=8)
ax2.set_xlabel('Fold Change', fontsize=9, fontweight='bold'); ax2.set_xscale('log'); ax2.set_xlim(0.3, 10000)
ax2.axvline(x=1, color='gray', linestyle='--', alpha=0.4); ax2.grid(axis='x', alpha=0.2)
ax2.set_title('B', loc='left', fontsize=11, fontweight='bold', x=-0.15)

# Panel C: Bar plot
ax3 = fig.add_subplot(gs[2, 0])
bind_stats = struct.groupby('binding_site')['log10_FC'].agg(['mean', 'sem']).reset_index()
ax3.bar(range(len(bind_stats)), bind_stats['mean'], yerr=bind_stats['sem'], color=NATURE_COLORS['tertiary'], alpha=0.8, capsize=4, edgecolor='black', linewidth=0.5)
ax3.set_xticks(range(len(bind_stats))); ax3.set_xticklabels(bind_stats['binding_site'], fontsize=7)
ax3.set_ylabel('Mean log₁₀(FC)', fontsize=9, fontweight='bold')
ax3.set_title('C', loc='left', fontsize=11, fontweight='bold', x=-0.2); ax3.grid(axis='y', alpha=0.3)

# Panel D: Scatter
ax4 = fig.add_subplot(gs[2, 1])
fit_data = fitness[fitness['FC'].notna()]
ax4.scatter(fit_data['Fitness_pct'], fit_data['FC'], s=120, c=fit_data['FC'], cmap='YlOrRd', alpha=0.8, edgecolors='black', linewidth=0.5, norm=matplotlib.colors.LogNorm())
for _, row in fit_data.iterrows():
    ax4.annotate(row['Mutation'], (row['Fitness_pct'], row['FC']), xytext=(3,3), textcoords='offset points', fontsize=6, fontweight='bold')
ax4.set_xlabel('Replication Fitness (% WT)', fontsize=9, fontweight='bold')
ax4.set_ylabel('Fold Change', fontsize=9, fontweight='bold'); ax4.set_yscale('log')
ax4.set_title('D', loc='left', fontsize=11, fontweight='bold', x=-0.2); ax4.grid(alpha=0.2)
if len(fit_data) > 2:
    r, p = stats.pearsonr(fit_data['Fitness_pct'], np.log10(fit_data['FC']))
    ax4.text(0.05, 0.95, f'r={r:.3f}\np={p:.2e}', transform=ax4.transAxes, fontsize=7, va='top', bbox=dict(boxstyle='round', fc='white', alpha=0.8, ec='black', lw=0.5))

Path('manuscript/figures').mkdir(parents=True, exist_ok=True)
plt.savefig('manuscript/figures/figure1_pub.pdf', bbox_inches='tight', dpi=600)
plt.savefig('manuscript/figures/figure1_pub.png', bbox_inches='tight', dpi=600)
print("✓ Figure 1 generated (600 DPI, Nature-style)")
