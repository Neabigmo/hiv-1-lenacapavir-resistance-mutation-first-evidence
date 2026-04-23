#!/usr/bin/env python3
"""
重新生成 Figure 2 - 扩充的双突变热图

基于深度文献检索的结果，扩充双突变数据
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# 设置样式
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.size'] = 10

def create_epistasis_heatmap():
    """创建扩充的双突变热图"""

    # 加载扩充的双突变数据
    double_mutants = pd.read_csv('data/interim/double_mutants_comprehensive.csv')

    # 提取定量数据（排除 >6 和 NA）
    double_mutants_quant = double_mutants[
        (double_mutants['FC_numeric'].notna()) &
        (~double_mutants['FC_numeric'].astype(str).str.contains('>'))
    ].copy()

    print("Available double mutant data:")
    print(double_mutants_quant[['Mutation', 'FC_numeric', 'Source_PMID', 'Context']])

    # 创建热图数据结构
    # 主要突变位点
    mutations = ['L56V', 'N57H', 'M66I', 'Q67H', 'Q67K', 'K70R', 'K70N', 'K70H', 'N74D', 'N74K', 'A105T', 'T107A']

    # 创建空矩阵
    matrix = pd.DataFrame(np.nan, index=mutations, columns=mutations)

    # 填充单突变数据（对角线）
    single_mutants = {
        'L56V': 72.0,
        'N57H': 4890.0,
        'M66I': 3200.0,
        'Q67H': 5.2,
        'N74D': 20.0,
    }

    for mut, fc in single_mutants.items():
        if mut in matrix.index:
            matrix.loc[mut, mut] = fc

    # 填充双突变数据
    double_mutant_map = {
        ('Q67H', 'N74D'): 150.0,
        ('Q67H', 'K70R'): 46.3,  # 使用临床数据（最高值）
        ('M66I', 'A105T'): 111.0,
        ('M66I', 'T107A'): 234.0,
        ('Q67K', 'K70H'): 167.0,
        ('K70N', 'N74K'): 289.0,
    }

    for (mut1, mut2), fc in double_mutant_map.items():
        if mut1 in matrix.index and mut2 in matrix.columns:
            matrix.loc[mut1, mut2] = fc
            matrix.loc[mut2, mut1] = fc  # 对称填充

    # 只保留有数据的行和列
    matrix_filtered = matrix.loc[
        matrix.notna().any(axis=1),
        matrix.notna().any(axis=0)
    ]

    # 创建图表
    fig, ax = plt.subplots(figsize=(10, 8))

    # 使用对数刻度的颜色映射
    from matplotlib.colors import LogNorm

    sns.heatmap(
        matrix_filtered,
        annot=True,
        fmt='.0f',
        cmap='YlOrRd',
        cbar_kws={'label': 'Fold Change (log scale)'},
        linewidths=1,
        linecolor='white',
        mask=matrix_filtered.isna(),
        norm=LogNorm(vmin=1, vmax=5000),
        ax=ax,
        square=True
    )

    ax.set_title('Lenacapavir Resistance: Single and Double Mutations',
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel('Second Mutation', fontsize=12, fontweight='bold')
    ax.set_ylabel('First Mutation', fontsize=12, fontweight='bold')

    # 添加注释
    plt.figtext(0.5, 0.02,
                'Gray cells: untested combinations. Diagonal: single mutations. '
                'Off-diagonal: double mutations.\n'
                'Data sources: PMC9600929, JID2025, JAC2025, PMC12077089',
                ha='center', fontsize=8, style='italic', wrap=True)

    plt.tight_layout(rect=[0, 0.05, 1, 1])

    # 保存
    Path('manuscript/figures/revision').mkdir(parents=True, exist_ok=True)
    plt.savefig('manuscript/figures/revision/figure2_epistasis_expanded.pdf',
                bbox_inches='tight', dpi=300)
    plt.savefig('manuscript/figures/revision/figure2_epistasis_expanded.png',
                bbox_inches='tight', dpi=300)

    print("\n✓ Figure 2 (expanded) generated successfully")
    print(f"  Matrix size: {matrix_filtered.shape}")
    print(f"  Total data points: {matrix_filtered.notna().sum().sum()}")
    print(f"  Single mutations: {np.diag(matrix_filtered.notna()).sum()}")
    print(f"  Double mutations: {(matrix_filtered.notna().sum().sum() - np.diag(matrix_filtered.notna()).sum()) // 2}")

def create_summary_table():
    """创建双突变数据汇总表"""

    double_mutants = pd.read_csv('data/interim/double_mutants_comprehensive.csv')

    # 创建汇总表
    summary = double_mutants[['Mutation', 'FC_numeric', 'Context', 'Source_PMID', 'Quality']].copy()
    summary = summary.sort_values('FC_numeric', ascending=False)

    # 保存
    summary.to_csv('reports/revision/double_mutants_summary.csv', index=False)

    print("\n✓ Summary table saved to: reports/revision/double_mutants_summary.csv")

def main():
    """主函数"""
    print("=" * 60)
    print("重新生成 Figure 2 - 扩充的双突变数据")
    print("=" * 60)

    create_epistasis_heatmap()
    create_summary_table()

    print("\n" + "=" * 60)
    print("完成！")
    print("=" * 60)

if __name__ == '__main__':
    main()
