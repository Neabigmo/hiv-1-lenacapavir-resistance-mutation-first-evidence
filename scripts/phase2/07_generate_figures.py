#!/usr/bin/env python3
"""
生成Phase 2图表
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # 非交互式后端
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# 设置样式
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.size'] = 10

def figure1_mutation_effects():
    """Figure 1: 突变效应森林图"""

    # 加载数据
    effects = pd.read_csv('results/phase2/mutation_effects_simplified.csv')
    ci = pd.read_csv('results/phase2/bootstrap_ci.csv')

    # 合并数据
    data = effects.merge(ci, left_index=True, right_index=True)
    data = data[data['count'] > 0].sort_values('FC_mean', ascending=True)

    fig, ax = plt.subplots(figsize=(8, 6))

    y_pos = np.arange(len(data))

    # 绘制误差线
    xerr_lower = np.maximum(data['FC_mean'] - data['FC_CI_lower'], 0)
    xerr_upper = np.maximum(data['FC_CI_upper'] - data['FC_mean'], 0)

    ax.errorbar(data['FC_mean'], y_pos,
                xerr=[xerr_lower, xerr_upper],
                fmt='o', capsize=5, capthick=2, markersize=8)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(data.index)
    ax.set_xlabel('Fold Change (FC)')
    ax.set_xscale('log')
    ax.set_title('Lenacapavir Resistance: Mutation Effects with 95% CI')
    ax.axvline(x=1, color='gray', linestyle='--', alpha=0.5)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('manuscript/figures/figure1_mutation_effects.pdf')
    plt.savefig('manuscript/figures/figure1_mutation_effects.png')
    print("Figure 1 saved")

def figure2_epistasis_heatmap():
    """Figure 2: 协同效应热图"""

    # 协同数据
    epistasis_data = {
        'Q67H': {'Q67H': 5.2, 'N74D': np.nan, 'K70R': np.nan},
        'N74D': {'Q67H': 150.0, 'N74D': 20.0, 'K70R': np.nan},
        'K70R': {'Q67H': 0.59, 'N74D': np.nan, 'K70R': np.nan}
    }

    df = pd.DataFrame(epistasis_data)

    fig, ax = plt.subplots(figsize=(6, 5))

    sns.heatmap(df, annot=True, fmt='.1f', cmap='YlOrRd',
                cbar_kws={'label': 'Fold Change'},
                linewidths=1, linecolor='white',
                mask=df.isna(), ax=ax)

    ax.set_title('Epistatic Interactions: Double Mutations')
    ax.set_xlabel('Second Mutation')
    ax.set_ylabel('First Mutation')

    plt.tight_layout()
    plt.savefig('manuscript/figures/figure2_epistasis.pdf')
    plt.savefig('manuscript/figures/figure2_epistasis.png')
    print("Figure 2 saved")

def figure3_structure_resistance():
    """Figure 3: 结构-耐药关联"""

    struct_data = pd.read_csv('results/phase2/structure_resistance_merged.csv')

    fig, ax = plt.subplots(figsize=(8, 5))

    # 按结合位点分组
    binding_groups = struct_data.groupby('binding_site')['log10_FC'].apply(list)

    positions = []
    values = []
    labels = []

    for i, (site, vals) in enumerate(binding_groups.items()):
        positions.extend([i] * len(vals))
        values.extend(vals)
        labels.append(site)

    ax.scatter(positions, values, alpha=0.6, s=100)
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=45, ha='right')
    ax.set_ylabel('log10(Fold Change)')
    ax.set_title('Resistance by Binding Site Location')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('manuscript/figures/figure3_structure.pdf')
    plt.savefig('manuscript/figures/figure3_structure.png')
    print("Figure 3 saved")

def figure4_fitness_tradeoff():
    """Figure 4: 适应度-耐药权衡"""

    fitness_data = pd.read_csv('results/phase2/fitness_resistance_data.csv')
    fitness_data = fitness_data[fitness_data['FC'].notna()]

    fig, ax = plt.subplots(figsize=(7, 6))

    ax.scatter(fitness_data['Fitness_pct'], fitness_data['FC'],
               s=150, alpha=0.7, edgecolors='black', linewidth=1.5)

    # 标注突变名称
    for idx, row in fitness_data.iterrows():
        ax.annotate(row['Mutation'],
                   (row['Fitness_pct'], row['FC']),
                   xytext=(5, 5), textcoords='offset points',
                   fontsize=9)

    ax.set_xlabel('Fitness (% of WT)')
    ax.set_ylabel('Fold Change (FC)')
    ax.set_yscale('log')
    ax.set_title('Fitness-Resistance Tradeoff')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('manuscript/figures/figure4_fitness.pdf')
    plt.savefig('manuscript/figures/figure4_fitness.png')
    print("Figure 4 saved")

def main():
    Path('manuscript/figures').mkdir(parents=True, exist_ok=True)

    print("Generating figures...")
    figure1_mutation_effects()
    figure2_epistasis_heatmap()
    figure3_structure_resistance()
    figure4_fitness_tradeoff()
    print("\nAll figures generated successfully!")

if __name__ == '__main__':
    main()
