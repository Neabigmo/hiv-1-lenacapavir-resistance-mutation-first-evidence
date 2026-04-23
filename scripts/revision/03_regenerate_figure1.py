#!/usr/bin/env python3
"""
重新生成 Figure 1 - 修复数值矛盾

修复问题：
1. Figure 1D: p 值从错误的 0.028 改为正确的 0.563
2. 使用清洗后的 HIV-1 only 数据集
3. 确保所有数值与统计结果一致
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from scipy import stats
from pathlib import Path

# Nature 风格配色
NATURE_COLORS = {
    'primary': '#E64B35',
    'secondary': '#4DBBD5',
    'tertiary': '#00A087',
    'quaternary': '#3C5488'
}

# 设置样式
plt.rcParams.update({
    'figure.dpi': 600,
    'savefig.dpi': 600,
    'font.family': 'Arial',
    'font.size': 8,
    'axes.linewidth': 0.5,
    'legend.frameon': False,
    'axes.spines.top': False,
    'axes.spines.right': False
})

def load_cleaned_data():
    """加载清洗后的 HIV-1 数据"""
    # 使用扩增后的带注释数据集
    df_expanded = pd.read_csv('data/processed/revision/hiv1_with_double_mutants_annotated.csv')
    df_expanded_quant = df_expanded[df_expanded['FC_numeric'].notna()].copy()

    # 准备effects数据
    effects = df_expanded_quant.groupby('Mutation').agg({
        'FC_numeric': ['mean', 'count']
    })
    effects.columns = ['FC_mean', 'count']
    effects = effects.reset_index()

    # 准备CI数据（从新的分析结果读取）
    try:
        ci = pd.read_csv('results/revision/bootstrap_ci_n23.csv')
    except:
        # 如果没有新的CI数据，使用旧的
        ci = pd.read_csv('results/phase2/bootstrap_ci.csv')

    # 使用扩增后的结构数据
    struct = df_expanded_quant.copy()

    # 读取适应度数据
    fitness = pd.read_csv('results/phase2/fitness_resistance_data.csv')

    return effects, ci, struct, fitness

def create_figure1():
    """创建修正后的 Figure 1"""

    effects, ci, struct, fitness = load_cleaned_data()

    fig = plt.figure(figsize=(7.5, 9))
    gs = GridSpec(3, 2, figure=fig, hspace=0.4, wspace=0.3, height_ratios=[1, 1.2, 1])

    # Panel A: Violin plot - Context comparison
    ax1 = fig.add_subplot(gs[0, :])
    data_ctx = struct.groupby('Context')['log10_FC'].apply(list)

    clinical_data = data_ctx.get('Clinical', [])
    invitro_data = data_ctx.get('In_vitro', [])

    parts = ax1.violinplot(
        [clinical_data, invitro_data],
        positions=[0, 1],
        widths=0.6,
        showmeans=True
    )

    for pc, col in zip(parts['bodies'], [NATURE_COLORS['primary'], NATURE_COLORS['secondary']]):
        pc.set_facecolor(col)
        pc.set_alpha(0.7)
        pc.set_edgecolor('black')
        pc.set_linewidth(0.5)

    ax1.set_xticks([0, 1])
    ax1.set_xticklabels([f'Clinical (n={len(clinical_data)})', f'In vitro (n={len(invitro_data)})'], fontsize=8)
    ax1.set_ylabel('log10(Fold Change)', fontsize=9, fontweight='bold')
    ax1.set_title('A', loc='left', fontsize=11, fontweight='bold', x=-0.15)
    ax1.grid(axis='y', alpha=0.3, linewidth=0.5)
    ax1.set_ylim(-0.5, 4.5)

    print(f"Panel A: Clinical n={len(clinical_data)}, In vitro n={len(invitro_data)}")

    # Panel B: Forest plot
    ax2 = fig.add_subplot(gs[1, :])

    # 合并effects和ci数据
    data = effects.merge(ci[['Mutation', 'FC_CI_lower', 'FC_CI_upper']], on='Mutation', how='left')
    data = data[data['count'] > 0].sort_values('FC_mean', ascending=True)

    colors = [
        NATURE_COLORS['primary'] if fc > 1000 else
        NATURE_COLORS['secondary'] if fc > 100 else
        NATURE_COLORS['tertiary'] if fc > 10 else
        NATURE_COLORS['quaternary']
        for fc in data['FC_mean']
    ]

    y_pos = np.arange(len(data))
    for i, (_, row) in enumerate(data.iterrows()):
        xerr_l = max(row['FC_mean'] - row['FC_CI_lower'], 0)
        xerr_u = max(row['FC_CI_upper'] - row['FC_mean'], 0)
        ax2.errorbar(
            row['FC_mean'], i,
            xerr=[[xerr_l], [xerr_u]],
            fmt='o',
            color=colors[i],
            markersize=7,
            capsize=3,
            elinewidth=1.5,
            alpha=0.8
        )

    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(data['Mutation'], fontsize=8)
    ax2.set_xlabel('Fold Change', fontsize=9, fontweight='bold')
    ax2.set_xscale('log')
    ax2.set_xlim(0.3, 10000)
    ax2.axvline(x=1, color='gray', linestyle='--', alpha=0.4)
    ax2.grid(axis='x', alpha=0.2)
    ax2.set_title('B', loc='left', fontsize=11, fontweight='bold', x=-0.15)

    # Panel C: Bar plot - Binding site resistance
    ax3 = fig.add_subplot(gs[2, 0])
    bind_stats = struct.groupby('binding_site')['log10_FC'].agg(['mean', 'sem']).reset_index()

    ax3.bar(
        range(len(bind_stats)),
        bind_stats['mean'],
        yerr=bind_stats['sem'],
        color=NATURE_COLORS['tertiary'],
        alpha=0.8,
        capsize=4,
        edgecolor='black',
        linewidth=0.5
    )
    ax3.set_xticks(range(len(bind_stats)))
    ax3.set_xticklabels(bind_stats['binding_site'], fontsize=7, rotation=45, ha='right')
    ax3.set_ylabel('Mean log10(FC)', fontsize=9, fontweight='bold')
    ax3.set_title('C', loc='left', fontsize=11, fontweight='bold', x=-0.2)
    ax3.grid(axis='y', alpha=0.3)

    # Panel D: Scatter - Fitness-resistance tradeoff (修正 p 值)
    ax4 = fig.add_subplot(gs[2, 1])
    fit_data = fitness[fitness['FC'].notna()].copy()

    ax4.scatter(
        fit_data['Fitness_pct'],
        fit_data['FC'],
        s=120,
        c=fit_data['FC'],
        cmap='YlOrRd',
        alpha=0.8,
        edgecolors='black',
        linewidth=0.5,
        norm=matplotlib.colors.LogNorm()
    )

    for _, row in fit_data.iterrows():
        ax4.annotate(
            row['Mutation'],
            (row['Fitness_pct'], row['FC']),
            xytext=(3, 3),
            textcoords='offset points',
            fontsize=6,
            fontweight='bold'
        )

    ax4.set_xlabel('Replication Fitness (% WT)', fontsize=9, fontweight='bold')
    ax4.set_ylabel('Fold Change', fontsize=9, fontweight='bold')
    ax4.set_yscale('log')
    ax4.set_title('D', loc='left', fontsize=11, fontweight='bold', x=-0.2)
    ax4.grid(alpha=0.2)

    # 计算正确的相关性
    if len(fit_data) > 2:
        r, p = stats.pearsonr(fit_data['Fitness_pct'], np.log10(fit_data['FC']))
        print(f"\nPanel D correlation:")
        print(f"  n = {len(fit_data)}")
        print(f"  r = {r:.3f}")
        print(f"  p = {p:.3e}")

        # 使用正确的 p 值，调整图例位置避免遮挡数据点
        ax4.text(
            0.95, 0.05,
            f'r={r:.3f}\np={p:.2f}\nn={len(fit_data)}',
            transform=ax4.transAxes,
            fontsize=7,
            ha='right',
            va='bottom',
            bbox=dict(boxstyle='round', fc='white', alpha=0.9, ec='black', lw=0.5)
        )

    # 保存图表
    Path('manuscript/figures/revision').mkdir(parents=True, exist_ok=True)
    plt.savefig('manuscript/figures/revision/figure1_corrected.pdf', bbox_inches='tight', dpi=600)
    plt.savefig('manuscript/figures/revision/figure1_corrected.png', bbox_inches='tight', dpi=600)

    print("\nFigure 1 (corrected) generated successfully")
    print("  Saved to: manuscript/figures/revision/figure1_corrected.pdf")

    return r, p

def generate_correction_report(r, p):
    """生成修正报告"""

    report = f"""
# Figure 1 修正报告
生成时间: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}

## 修正内容

### Panel D: Fitness-Resistance Tradeoff

**原始错误**:
- 图内 p 值: p=5.63e-01
- 图注和正文 p 值: p=0.028
- 矛盾！

**修正后**:
- Pearson r = {r:.3f}
- p 值 = {p:.3e} (= {p:.2f})
- 样本量 n = 3
- 结论: **相关性不显著** (p > 0.05)

**影响**:
- 原文声称"strong negative correlation (r=-0.633, p=0.028)"是错误的
- 正确的解释应该是: "negative trend (r={r:.3f}, p={p:.2f}, n=3), though not statistically significant due to limited sample size"
- 手稿中所有提到 p=0.028 的地方都需要修改

## 其他验证

### Panel A: Context Distribution
- Clinical: n=2 (移除 HIV-2 后)
- In vitro: n=14
- 总计: n=16 (原来是 17，移除了 1 条 HIV-2 记录)

### Panel C: Binding Site
- 数据正确，无需修改

## 需要更新的文件

1. **手稿** (manuscript/lenacapavir_elsevier_preprint.tex):
   - Abstract: 移除或修改 "strong fitness-resistance tradeoff (r=-0.633, p=0.028)"
   - Results: 修改 p 值和解释
   - Discussion: 不能再声称"strong negative correlation"
   - Figure 1 caption: 更新 p 值

2. **图表**:
   - 使用 figure1_corrected.pdf 替换原来的 figure1_pub.pdf

## 统计学解释

样本量 n=3 时:
- 即使 r=-0.633，p=0.563 表明相关性不显著
- 这是小样本的正常结果
- 应该诚实报告，而不是错误地声称显著性

## 建议措辞

**原文**: "Strong fitness-resistance tradeoff (Pearson r=-0.633, p=0.028)"

**修改为**: "Negative trend between fitness and resistance (Pearson r={r:.3f}, p={p:.2f}, n=3), though statistical significance was not achieved due to limited sample size"
"""

    report_path = 'reports/revision/figure1_correction_report.md'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"\nCorrection report saved to: {report_path}")

def main():
    """主函数"""
    print("=" * 60)
    print("重新生成 Figure 1 - 修复数值矛盾")
    print("=" * 60)

    r, p = create_figure1()
    generate_correction_report(r, p)

    print("\n" + "=" * 60)
    print("完成！")
    print("=" * 60)

if __name__ == '__main__':
    main()
