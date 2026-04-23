#!/usr/bin/env python3
"""
Phase 2: 敏感性分析（替代统计功效分析）
评估模型对数据子集和参数变化的稳健性
"""

import pandas as pd
import numpy as np
from scipy import stats
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler(f'logs/experiments/phase2_sensitivity_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)

def load_data():
    df = pd.read_csv('data/processed/real_literature_integrated.csv')
    df_quant = df[df['FC_numeric'].notna()].copy()
    df_quant['log10_FC'] = np.log10(df_quant['FC_numeric'])
    return df_quant

def sensitivity_by_context(df):
    """按Context分层分析"""
    logging.info("\n=== Sensitivity by Context ===")

    context_stats = df.groupby('Context')['log10_FC'].agg([
        ('count', 'count'),
        ('mean', 'mean'),
        ('std', 'std')
    ]).round(3)

    logging.info(context_stats.to_string())
    return context_stats

def sensitivity_by_quality(df):
    """按Quality分层分析"""
    logging.info("\n=== Sensitivity by Quality ===")

    quality_stats = df.groupby('Quality')['log10_FC'].agg([
        ('count', 'count'),
        ('mean', 'mean'),
        ('std', 'std')
    ]).round(3)

    logging.info(quality_stats.to_string())
    return quality_stats

def jackknife_analysis(df):
    """Jackknife留一分析"""
    logging.info("\n=== Jackknife Leave-One-Out ===")

    n = len(df)
    full_mean = df['log10_FC'].mean()

    jackknife_means = []
    for i in range(n):
        subset = df.drop(df.index[i])
        jackknife_means.append(subset['log10_FC'].mean())

    jackknife_means = np.array(jackknife_means)
    bias = (n - 1) * (jackknife_means.mean() - full_mean)
    se = np.sqrt((n - 1) * np.var(jackknife_means))

    logging.info(f"Full mean: {full_mean:.3f}")
    logging.info(f"Jackknife bias: {bias:.3f}")
    logging.info(f"Jackknife SE: {se:.3f}")
    logging.info(f"95% CI: [{full_mean - 1.96*se:.3f}, {full_mean + 1.96*se:.3f}]")

    return {'bias': bias, 'se': se, 'ci_lower': full_mean - 1.96*se, 'ci_upper': full_mean + 1.96*se}

def outlier_sensitivity(df):
    """异常值敏感性"""
    logging.info("\n=== Outlier Sensitivity ===")

    mean_all = df['log10_FC'].mean()
    std_all = df['log10_FC'].std()

    # 移除>3σ异常值
    df_no_outliers = df[np.abs(df['log10_FC'] - mean_all) <= 3 * std_all]
    mean_no_outliers = df_no_outliers['log10_FC'].mean()

    logging.info(f"Mean (all data): {mean_all:.3f}")
    logging.info(f"Mean (no outliers): {mean_no_outliers:.3f}")
    logging.info(f"Difference: {abs(mean_all - mean_no_outliers):.3f}")
    logging.info(f"Outliers removed: {len(df) - len(df_no_outliers)}")

    return {'mean_all': mean_all, 'mean_no_outliers': mean_no_outliers, 'n_outliers': len(df) - len(df_no_outliers)}

def subtype_robustness(df):
    """亚型稳健性检验"""
    logging.info("\n=== Subtype Robustness ===")

    subtype_counts = df['Subtype'].value_counts()
    logging.info(f"Subtype distribution:\n{subtype_counts}")

    # 对每个亚型进行leave-one-subtype-out
    subtypes = df['Subtype'].unique()
    results = []

    for subtype in subtypes:
        subset = df[df['Subtype'] != subtype]
        if len(subset) > 0:
            mean_without = subset['log10_FC'].mean()
            results.append({'subtype_excluded': subtype, 'mean': mean_without, 'n': len(subset)})

    results_df = pd.DataFrame(results)
    logging.info(f"\nLeave-one-subtype-out means:\n{results_df.to_string()}")

    return results_df

def main():
    logging.info("Starting Phase 2 Sensitivity Analysis")

    df = load_data()
    logging.info(f"Loaded {len(df)} quantitative records")

    # 各项敏感性分析
    context_stats = sensitivity_by_context(df)
    quality_stats = sensitivity_by_quality(df)
    jackknife_results = jackknife_analysis(df)
    outlier_results = outlier_sensitivity(df)
    subtype_results = subtype_robustness(df)

    # 保存结果
    context_stats.to_csv('results/phase2/sensitivity_context.csv')
    quality_stats.to_csv('results/phase2/sensitivity_quality.csv')
    subtype_results.to_csv('results/phase2/sensitivity_subtype.csv', index=False)

    with open('results/phase2/sensitivity_summary.txt', 'w') as f:
        f.write("Phase 2 Sensitivity Analysis Summary\n")
        f.write("="*50 + "\n\n")
        f.write(f"Jackknife bias: {jackknife_results['bias']:.3f}\n")
        f.write(f"Jackknife SE: {jackknife_results['se']:.3f}\n")
        f.write(f"Outliers removed: {outlier_results['n_outliers']}\n")
        f.write(f"Mean difference (outliers): {abs(outlier_results['mean_all'] - outlier_results['mean_no_outliers']):.3f}\n")

    logging.info("\nSensitivity analysis completed")

if __name__ == '__main__':
    main()
