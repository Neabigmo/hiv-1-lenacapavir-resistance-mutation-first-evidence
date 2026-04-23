#!/usr/bin/env python3
"""
混合分析框架：整合定量和定性数据
将临床出现率、适应度代价、保守性转换为半定量指标
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def convert_prevalence_to_risk_score(prevalence_str):
    """
    临床出现率 → 风险评分 (0-10)

    规则:
    - <0.1%: 1 (极低风险)
    - 0.1-1%: 3 (低风险)
    - 1-5%: 5 (中等风险)
    - 5-10%: 7 (高风险)
    - >10%: 9 (极高风险)
    """
    if pd.isna(prevalence_str):
        return np.nan

    try:
        # 提取数值
        if isinstance(prevalence_str, str):
            if '<' in prevalence_str:
                val = float(prevalence_str.replace('<', '').replace('%', ''))
                return 1 if val < 0.1 else 3
            elif '>' in prevalence_str:
                val = float(prevalence_str.replace('>', '').replace('%', ''))
                return 9 if val > 10 else 7
            else:
                val = float(prevalence_str.replace('%', ''))
        else:
            val = float(prevalence_str)

        if val < 0.1:
            return 1
        elif val < 1:
            return 3
        elif val < 5:
            return 5
        elif val < 10:
            return 7
        else:
            return 9
    except:
        return np.nan

def convert_fitness_to_selection_pressure(fitness_str):
    """
    适应度代价 → 选择压力指数 (0-10)

    规则:
    - >90% WT: 1 (低选择压力，易传播)
    - 50-90% WT: 3 (中低选择压力)
    - 10-50% WT: 5 (中等选择压力)
    - 1-10% WT: 7 (高选择压力)
    - <1% WT: 9 (极高选择压力，难传播)
    """
    if pd.isna(fitness_str):
        return np.nan

    try:
        if isinstance(fitness_str, str):
            # 提取百分比
            if '%' in fitness_str:
                val = float(fitness_str.replace('%', '').split()[0])
            else:
                return np.nan
        else:
            val = float(fitness_str)

        if val > 90:
            return 1
        elif val > 50:
            return 3
        elif val > 10:
            return 5
        elif val > 1:
            return 7
        else:
            return 9
    except:
        return np.nan

def convert_conservation_to_tolerance(conservation_str):
    """
    保守性 → 突变容忍度 (0-10)

    规则:
    - >95% conservation: 1 (低容忍度，突变有害)
    - 90-95%: 3
    - 80-90%: 5
    - 70-80%: 7
    - <70%: 9 (高容忍度，突变可耐受)
    """
    if pd.isna(conservation_str):
        return np.nan

    try:
        if isinstance(conservation_str, str):
            val = float(conservation_str.replace('%', ''))
        else:
            val = float(conservation_str)

        if val > 95:
            return 1
        elif val > 90:
            return 3
        elif val > 80:
            return 5
        elif val > 70:
            return 7
        else:
            return 9
    except:
        return np.nan

def estimate_fc_from_qualitative(row):
    """
    基于定性指标估算FC范围

    组合规则:
    - 高风险 + 高选择压力 + 低容忍度 → 高FC (>100x)
    - 中等组合 → 中FC (10-100x)
    - 低风险 + 低选择压力 + 高容忍度 → 低FC (<10x)
    """
    risk = row.get('risk_score', np.nan)
    pressure = row.get('selection_pressure', np.nan)
    tolerance = row.get('mutation_tolerance', np.nan)

    if pd.isna(risk) and pd.isna(pressure) and pd.isna(tolerance):
        return np.nan, np.nan

    # 计算综合评分
    scores = [s for s in [risk, pressure, tolerance] if not pd.isna(s)]
    if not scores:
        return np.nan, np.nan

    avg_score = np.mean(scores)

    # 映射到FC范围
    if avg_score >= 7:
        return 100, 1000  # 高耐药
    elif avg_score >= 5:
        return 10, 100    # 中等耐药
    elif avg_score >= 3:
        return 2, 10      # 低耐药
    else:
        return 0.5, 2     # 极低耐药

def process_mixed_data(input_csv):
    """处理混合数据集"""
    df = pd.read_csv(input_csv)

    logging.info(f"Loaded {len(df)} records")

    # 转换定性指标
    df['risk_score'] = df['Prevalence'].apply(convert_prevalence_to_risk_score)
    df['selection_pressure'] = df['Replication_Capacity'].apply(convert_fitness_to_selection_pressure)

    # 从Notes中提取保守性信息
    def extract_conservation(notes):
        if pd.isna(notes):
            return np.nan
        if 'conservation' in str(notes).lower():
            # 尝试提取百分比
            import re
            match = re.search(r'(\d+)%', str(notes))
            if match:
                return float(match.group(1))
        return np.nan

    df['conservation'] = df['Notes'].apply(extract_conservation)
    df['mutation_tolerance'] = df['conservation'].apply(convert_conservation_to_tolerance)

    # 估算FC范围
    fc_estimates = df.apply(estimate_fc_from_qualitative, axis=1)
    df['estimated_fc_min'] = fc_estimates.apply(lambda x: x[0] if isinstance(x, tuple) else np.nan)
    df['estimated_fc_max'] = fc_estimates.apply(lambda x: x[1] if isinstance(x, tuple) else np.nan)
    df['estimated_fc_mid'] = (df['estimated_fc_min'] + df['estimated_fc_max']) / 2

    # 统计
    quantitative = df['FC_numeric'].notna().sum()
    semi_quantitative = df['estimated_fc_mid'].notna().sum()

    logging.info(f"Quantitative FC: {quantitative}")
    logging.info(f"Semi-quantitative estimates: {semi_quantitative}")
    logging.info(f"Total usable: {quantitative + semi_quantitative}")

    return df

def main():
    input_file = 'data/processed/real_literature_integrated.csv'
    output_file = 'data/processed/mixed_quantitative_dataset.csv'

    df = process_mixed_data(input_file)
    df.to_csv(output_file, index=False)

    logging.info(f"Saved to {output_file}")

    # 生成报告
    report = f"""
# 混合分析框架处理报告

## 数据转换统计
- 原始记录: {len(df)}
- 定量FC数据: {df['FC_numeric'].notna().sum()}
- 半定量估算: {df['estimated_fc_mid'].notna().sum()}
- 总可用数据: {df['FC_numeric'].notna().sum() + df['estimated_fc_mid'].notna().sum()}

## 转换规则
1. 临床出现率 → 风险评分 (1-9)
2. 适应度代价 → 选择压力指数 (1-9)
3. 保守性 → 突变容忍度 (1-9)
4. 综合评分 → FC范围估算

## 输出文件
- {output_file}
"""

    with open('reports/status/MIXED_ANALYSIS_REPORT.md', 'w', encoding='utf-8') as f:
        f.write(report)

    return df

if __name__ == '__main__':
    df = main()
