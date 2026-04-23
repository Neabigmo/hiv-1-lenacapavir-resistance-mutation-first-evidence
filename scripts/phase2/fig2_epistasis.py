import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from matplotlib.patches import Rectangle

plt.rcParams.update({'figure.dpi': 600, 'savefig.dpi': 600, 'font.size': 8, 'axes.linewidth': 0.5})

mutations = ['Q67H', 'N74D', 'K70R', 'M66I', 'N57H', 'L56V']
matrix = np.full((6, 6), np.nan)
mut_idx = {m: i for i, m in enumerate(mutations)}
matrix[mut_idx['Q67H'], mut_idx['Q67H']] = 5.2
matrix[mut_idx['Q67H'], mut_idx['N74D']] = 150.0
matrix[mut_idx['Q67H'], mut_idx['K70R']] = 0.59
matrix[mut_idx['N74D'], mut_idx['N74D']] = 20.0
matrix[mut_idx['M66I'], mut_idx['M66I']] = 3200.0
matrix[mut_idx['N57H'], mut_idx['N57H']] = 4890.0
matrix[mut_idx['L56V'], mut_idx['L56V']] = 72.0

fig, ax = plt.subplots(figsize=(5, 4.5))
mask = np.isnan(matrix)
im = ax.imshow(matrix, cmap='RdYlBu_r', aspect='auto', norm=LogNorm(vmin=0.5, vmax=5000), interpolation='nearest')

for i in range(6):
    for j in range(6):
        if mask[i, j]:
            ax.add_patch(Rectangle((j-0.5, i-0.5), 1, 1, fill=True, facecolor='lightgray', alpha=0.3))
        else:
            ax.text(j, i, f'{matrix[i, j]:.1f}', ha="center", va="center", color="black", fontsize=7, fontweight='bold')

ax.set_xticks(range(6)); ax.set_yticks(range(6))
ax.set_xticklabels(mutations, fontsize=9); ax.set_yticklabels(mutations, fontsize=9)
ax.set_xlabel('Second Mutation', fontsize=10, fontweight='bold')
ax.set_ylabel('First Mutation', fontsize=10, fontweight='bold')
cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
cbar.set_label('Fold Change', fontsize=9, fontweight='bold')
plt.title('Epistatic Interactions', fontsize=11, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig('manuscript/figures/figure2_epistasis_pub.pdf', bbox_inches='tight', dpi=600)
plt.savefig('manuscript/figures/figure2_epistasis_pub.png', bbox_inches='tight', dpi=600)
print("Figure 2 generated")
