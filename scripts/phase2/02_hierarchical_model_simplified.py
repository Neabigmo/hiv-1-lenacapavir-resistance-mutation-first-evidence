#!/usr/bin/env python3
"""
Phase 2 精简版：层次混合效应模型
使用29条真实定量FC数据
"""

import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm
from statsmodels.formula.api import mixedlm
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler(f'logs/experiments/phase2_hierarchical_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)

def load_quantitative_data():
    """加载真实定量FC数据"""
    df = pd.read_csv('data/processed/real_literature_integrated.csv')

    # 筛选有效FC数据
    df_quant = df[df['FC_numeric'].notna()].copy()

    logging.info(f"Loaded {len(df_quant)} records with quantitative FC")

    return df_quant

def fit_hierarchical_model(df):
    """拟合层次混合效应模型"""

    # 准备数据
    df['log10_FC'] = np.log10(df['FC_numeric'])

    # 移除缺失值
    df_clean = df[['log10_FC', 'Mutation', 'Subtype']].dropna()

    logging.info(f"Clean data: {len(df_clean)} records")
    logging.info(f"Mutations: {df_clean['Mutation'].nunique()}")
    logging.info(f"Subtypes: {df_clean['Subtype'].nunique()}")

    # 拟合混合效应模型
    # log10(FC) ~ Mutation + (1|Subtype)
    try:
        model = mixedlm("log10_FC ~ C(Mutation)", df_clean, groups=df_clean["Subtype"])
        result = model.fit(method='powell')

        logging.info("\n=== Model Summary ===")
        logging.info(result.summary())

        # 提取随机效应方差
        re_var = result.cov_re.iloc[0, 0] if hasattr(result, 'cov_re') else 0
        logging.info(f"\nRandom effect variance (Subtype): {re_var:.4f}")

        return result, df_clean

    except Exception as e:
        logging.error(f"Model fitting failed: {e}")
        logging.info("Falling back to fixed effects model")

        # 固定效应模型
        X = pd.get_dummies(df_clean['Mutation'], drop_first=True)
        X = sm.add_constant(X)
        y = df_clean['log10_FC']

        model = sm.OLS(y, X)
        result = model.fit()

        logging.info("\n=== Fixed Effects Model ===")
        logging.info(result.summary())

        return result, df_clean

def calculate_mutation_effects(df):
    """计算突变效应"""
    mutation_stats = df.groupby('Mutation')['log10_FC'].agg([
        ('count', 'count'),
        ('mean', 'mean'),
        ('std', 'std'),
        ('min', 'min'),
        ('max', 'max')
    ]).round(3)

    # 转换回FC
    mutation_stats['FC_mean'] = 10 ** mutation_stats['mean']
    mutation_stats['FC_min'] = 10 ** mutation_stats['min']
    mutation_stats['FC_max'] = 10 ** mutation_stats['max']

    logging.info("\n=== Mutation Effects ===")
    logging.info(mutation_stats.to_string())

    return mutation_stats

def bootstrap_validation(df, n_bootstrap=1000):
    """Bootstrap验证"""
    logging.info(f"\nRunning bootstrap validation (n={n_bootstrap})")

    mutation_means = []

    for i in range(n_bootstrap):
        # 重采样
        sample = df.sample(n=len(df), replace=True)
        means = sample.groupby('Mutation')['log10_FC'].mean()
        mutation_means.append(means)

    # 计算95% CI
    bootstrap_df = pd.DataFrame(mutation_means)
    ci_lower = bootstrap_df.quantile(0.025)
    ci_upper = bootstrap_df.quantile(0.975)

    ci_results = pd.DataFrame({
        'CI_lower': ci_lower,
        'CI_upper': ci_upper,
        'FC_CI_lower': 10 ** ci_lower,
        'FC_CI_upper': 10 ** ci_upper
    }).round(3)

    logging.info("\n=== Bootstrap 95% CI ===")
    logging.info(ci_results.to_string())

    return ci_results

def main():
    logging.info("Starting Phase 2 Hierarchical Model (Simplified)")

    # 加载数据
    df = load_quantitative_data()

    # 拟合模型
    model_result, df_clean = fit_hierarchical_model(df)

    # 计算突变效应
    mutation_effects = calculate_mutation_effects(df_clean)

    # Bootstrap验证
    ci_results = bootstrap_validation(df_clean, n_bootstrap=1000)

    # 保存结果
    mutation_effects.to_csv('results/phase2/mutation_effects_simplified.csv')
    ci_results.to_csv('results/phase2/bootstrap_ci.csv')

    # 保存模型
    with open('results/phase2/model_summary.txt', 'w') as f:
        f.write(str(model_result.summary()))

    logging.info("\nPhase 2 hierarchical model completed")
    logging.info(f"Results saved to results/phase2/")

if __name__ == '__main__':
    main()
