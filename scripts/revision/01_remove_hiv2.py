#!/usr/bin/env python3
"""
数据清洗脚本：修复 HIV-2 分组错误和统一亚型命名

根据同行评审意见：
1. 移除所有 HIV-2 记录（HIV-2 不是 HIV-1 的 subtype）
2. 统一亚型命名（B vs Subtype_B）
3. 创建 HIV-1 only 数据集用于主分析
4. 将 HIV-2 数据保存到单独文件用于补充分析
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler(f'logs/revision/data_cleaning_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)

def load_data():
    """加载原始数据"""
    df = pd.read_csv('data/processed/real_literature_integrated.csv')
    logging.info(f"Loaded {len(df)} total records")
    return df

def identify_hiv2_records(df):
    """识别所有 HIV-2 记录"""
    hiv2_mask = df['Subtype'].str.contains('HIV-2', case=False, na=False)
    hiv2_records = df[hiv2_mask].copy()

    logging.info(f"\n=== HIV-2 Records Identified ===")
    logging.info(f"Total HIV-2 records: {len(hiv2_records)}")

    if len(hiv2_records) > 0:
        logging.info("\nHIV-2 records details:")
        for idx, row in hiv2_records.iterrows():
            logging.info(f"  - {row['Source']}: {row['Mutation']}, FC={row.get('FC_numeric', 'N/A')}, Subtype={row['Subtype']}")

    return hiv2_records, hiv2_mask

def standardize_subtype_names(df):
    """统一亚型命名"""

    # 创建亚型映射表
    subtype_mapping = {
        'Subtype_B': 'B',
        'Subtype_C': 'C',
        'Subtype_D': 'D',
        'Subtype_A': 'A',
        'Subtype_A1': 'A1',
        'CRF02_AG': 'CRF02_AG',
        'CRF01_AE': 'CRF01_AE',
        'Mixed': 'Mixed',
        'B': 'B',
        'C': 'C',
        'D': 'D',
        'A': 'A',
        'A1': 'A1'
    }

    logging.info("\n=== Standardizing Subtype Names ===")
    logging.info("Original subtype distribution:")
    logging.info(df['Subtype'].value_counts().to_string())

    # 应用映射
    df['Subtype_original'] = df['Subtype'].copy()
    df['Subtype'] = df['Subtype'].map(subtype_mapping).fillna(df['Subtype'])

    logging.info("\nStandardized subtype distribution:")
    logging.info(df['Subtype'].value_counts().to_string())

    # 检查未映射的亚型
    unmapped = df[~df['Subtype'].isin(subtype_mapping.values()) & df['Subtype'].notna()]
    if len(unmapped) > 0:
        logging.warning(f"\nWarning: {len(unmapped)} records with unmapped subtypes:")
        logging.warning(unmapped['Subtype'].unique())

    return df

def create_hiv1_dataset(df, hiv2_mask):
    """创建 HIV-1 only 数据集"""
    df_hiv1 = df[~hiv2_mask].copy()

    logging.info(f"\n=== HIV-1 Dataset Created ===")
    logging.info(f"Total HIV-1 records: {len(df_hiv1)}")
    logging.info(f"Records with quantitative FC: {df_hiv1['FC_numeric'].notna().sum()}")

    # 统计信息
    logging.info("\nHIV-1 dataset statistics:")
    logging.info(f"  Unique mutations: {df_hiv1['Mutation'].nunique()}")
    logging.info(f"  Unique subtypes: {df_hiv1['Subtype'].nunique()}")
    logging.info(f"  Unique sources: {df_hiv1['Source'].nunique()}")

    logging.info("\nSubtype distribution in HIV-1 dataset:")
    logging.info(df_hiv1['Subtype'].value_counts().to_string())

    logging.info("\nContext distribution:")
    logging.info(df_hiv1['Context'].value_counts().to_string())

    return df_hiv1

def save_datasets(df_hiv1, df_hiv2):
    """保存数据集"""

    # 创建输出目录
    Path('data/processed/revision').mkdir(parents=True, exist_ok=True)

    # 保存 HIV-1 数据集（主分析）
    output_hiv1 = 'data/processed/revision/hiv1_only_dataset.csv'
    df_hiv1.to_csv(output_hiv1, index=False)
    logging.info(f"\n✓ HIV-1 dataset saved to: {output_hiv1}")

    # 保存 HIV-2 数据集（补充分析）
    if len(df_hiv2) > 0:
        output_hiv2 = 'data/processed/revision/hiv2_supplementary.csv'
        df_hiv2.to_csv(output_hiv2, index=False)
        logging.info(f"✓ HIV-2 dataset saved to: {output_hiv2}")

    # 保存仅包含定量 FC 的 HIV-1 数据
    df_hiv1_quant = df_hiv1[df_hiv1['FC_numeric'].notna()].copy()
    output_quant = 'data/processed/revision/hiv1_quantitative_only.csv'
    df_hiv1_quant.to_csv(output_quant, index=False)
    logging.info(f"✓ HIV-1 quantitative dataset saved to: {output_quant}")
    logging.info(f"  Contains {len(df_hiv1_quant)} records with FC values")

def generate_summary_report(df_original, df_hiv1, df_hiv2):
    """生成摘要报告"""

    report = f"""
# 数据清洗报告
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 原始数据
- 总记录数: {len(df_original)}
- 包含定量 FC 的记录: {df_original['FC_numeric'].notna().sum()}

## HIV-2 记录（已移除）
- HIV-2 记录数: {len(df_hiv2)}
- 包含定量 FC 的 HIV-2 记录: {df_hiv2['FC_numeric'].notna().sum() if len(df_hiv2) > 0 else 0}

## HIV-1 数据集（主分析）
- HIV-1 记录数: {len(df_hiv1)}
- 包含定量 FC 的记录: {df_hiv1['FC_numeric'].notna().sum()}
- 唯一突变数: {df_hiv1['Mutation'].nunique()}
- 唯一亚型数: {df_hiv1['Subtype'].nunique()}
- 唯一来源数: {df_hiv1['Source'].nunique()}

## 亚型分布（HIV-1）
{df_hiv1['Subtype'].value_counts().to_string()}

## 上下文分布（HIV-1）
{df_hiv1['Context'].value_counts().to_string()}

## 关键变化
1. ✓ 移除了所有 HIV-2 记录（生物学分类错误）
2. ✓ 统一了亚型命名（Subtype_B → B）
3. ✓ 创建了纯 HIV-1 数据集用于主分析
4. ✓ 保存了 HIV-2 数据到单独文件用于补充材料

## 下一步
- 使用 hiv1_quantitative_only.csv 重新运行混合效应模型
- 验证核心结论是否仍然成立
- 更新所有图表和统计结果
"""

    report_path = 'reports/revision/data_cleaning_report.md'
    Path('reports/revision').mkdir(parents=True, exist_ok=True)
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)

    logging.info(f"\n✓ Summary report saved to: {report_path}")
    print(report)

def main():
    """主函数"""

    logging.info("=" * 60)
    logging.info("数据清洗：修复 HIV-2 分组错误")
    logging.info("=" * 60)

    # 创建日志目录
    Path('logs/revision').mkdir(parents=True, exist_ok=True)

    # 1. 加载数据
    df = load_data()
    df_original = df.copy()

    # 2. 识别 HIV-2 记录
    df_hiv2, hiv2_mask = identify_hiv2_records(df)

    # 3. 统一亚型命名
    df = standardize_subtype_names(df)

    # 4. 创建 HIV-1 数据集
    df_hiv1 = create_hiv1_dataset(df, hiv2_mask)

    # 5. 保存数据集
    save_datasets(df_hiv1, df_hiv2)

    # 6. 生成摘要报告
    generate_summary_report(df_original, df_hiv1, df_hiv2)

    logging.info("\n" + "=" * 60)
    logging.info("数据清洗完成！")
    logging.info("=" * 60)

if __name__ == '__main__':
    main()
