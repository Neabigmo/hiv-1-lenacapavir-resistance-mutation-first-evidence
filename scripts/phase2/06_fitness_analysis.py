#!/usr/bin/env python3
"""
Phase 2: 适应度-耐药关联分析
分析耐药突变的适应度代价
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler(f'logs/experiments/phase2_fitness_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)

def load_data():
    df = pd.read_csv('data/processed/real_literature_integrated.csv')
    return df

def extract_fitness_data(df):
    """提取适应度数据"""

    # 从Notes中提取适应度信息
    fitness_data = []

    for idx, row in df.iterrows():
        mutation = row['Mutation']
        notes = str(row['Notes'])
        fc = row.get('FC_numeric', np.nan)

        # 提取复制能力百分比
        if 'replication capacity' in notes.lower():
            import re
            match = re.search(r'(\d+\.?\d*)%', notes)
            if match:
                fitness_pct = float(match.group(1))
                fitness_data.append({
                    'Mutation': mutation,
                    'FC': fc,
                    'Fitness_pct': fitness_pct,
                    'Type': 'Replication_capacity'
                })

        # 提取感染性百分比
        if 'infectivity' in notes.lower() and 'WT' in notes:
            import re
            match = re.search(r'(\d+\.?\d*)%', notes)
            if match:
                fitness_pct = float(match.group(1))
                fitness_data.append({
                    'Mutation': mutation,
                    'FC': fc,
                    'Fitness_pct': fitness_pct,
                    'Type': 'Infectivity'
                })

    # 手动添加已知数据
    known_fitness = [
        {'Mutation': 'M66I', 'FC': 3200, 'Fitness_pct': 1.5, 'Type': 'Replication_capacity'},
        {'Mutation': 'N57H', 'FC': 4890, 'Fitness_pct': 12.0, 'Type': 'Infectivity'},
        {'Mutation': 'L56V', 'FC': 72, 'Fitness_pct': 0.6, 'Type': 'Infectivity'},
    ]

    fitness_data.extend(known_fitness)

    return pd.DataFrame(fitness_data).drop_duplicates()

def analyze_fitness_resistance_tradeoff(df_fitness):
    """分析适应度-耐药权衡"""

    logging.info("\n=== Fitness-Resistance Tradeoff ===")

    df_fitness['log10_FC'] = np.log10(df_fitness['FC'])

    # 计算相关性
    if len(df_fitness) > 2:
        corr = df_fitness[['log10_FC', 'Fitness_pct']].corr().iloc[0, 1]
        logging.info(f"Correlation (log10_FC vs Fitness): {corr:.3f}")

    logging.info("\nFitness-Resistance data:")
    logging.info(df_fitness.to_string(index=False))

    return df_fitness

def compensatory_mutations():
    """补偿性突变分析"""

    logging.info("\n=== Compensatory Mutations ===")

    compensatory_data = {
        'A105T': {
            'primary_mutation': 'M66I+N74D',
            'effect': 'Restores >90% WT fitness',
            'mechanism': 'Stabilizes capsid structure'
        }
    }

    for mut, info in compensatory_data.items():
        logging.info(f"{mut}: {info['effect']}")
        logging.info(f"  Primary: {info['primary_mutation']}")
        logging.info(f"  Mechanism: {info['mechanism']}")

    return compensatory_data

def main():
    logging.info("Starting Phase 2 Fitness-Resistance Analysis")

    df = load_data()
    df_fitness = extract_fitness_data(df)

    logging.info(f"Extracted {len(df_fitness)} fitness records")

    df_analyzed = analyze_fitness_resistance_tradeoff(df_fitness)
    comp_data = compensatory_mutations()

    # 保存结果
    df_analyzed.to_csv('results/phase2/fitness_resistance_data.csv', index=False)

    logging.info("\nFitness-resistance analysis completed")

if __name__ == '__main__':
    main()
