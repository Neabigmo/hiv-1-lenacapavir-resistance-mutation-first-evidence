#!/usr/bin/env python3
"""
Phase 2: 结构-功能关联分析
分析突变位点与LEN结合口袋的空间关系
"""

import pandas as pd
import numpy as np
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler(f'logs/experiments/phase2_structure_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)

def load_data():
    df = pd.read_csv('data/processed/real_literature_integrated.csv')
    df_quant = df[df['FC_numeric'].notna()].copy()
    df_quant['log10_FC'] = np.log10(df_quant['FC_numeric'])
    return df_quant

def annotate_structural_regions():
    """根据文献标注突变的结构区域"""

    # 基于PMC9600929和结构数据
    structural_annotations = {
        'L56V': {'region': 'NTD-CTD_interface', 'binding_site': 'hydrophobic_pocket', 'mechanism': 'steric_clash'},
        'N57H': {'region': 'NTD-CTD_interface', 'binding_site': 'hydrophobic_pocket', 'mechanism': 'H-bond_loss'},
        'M66I': {'region': 'NTD-CTD_interface', 'binding_site': 'hydrophobic_pocket', 'mechanism': 'steric_hindrance'},
        'Q67H': {'region': 'NTD-CTD_interface', 'binding_site': 'hydrophobic_pocket', 'mechanism': 'conformational_switch'},
        'K70R': {'region': 'NTD-CTD_interface', 'binding_site': 'adjacent', 'mechanism': 'electrostatic'},
        'N74D': {'region': 'NTD-CTD_interface', 'binding_site': 'hydrophobic_pocket', 'mechanism': 'electrostatic_repulsion'},
        'A105T': {'region': 'CTD', 'binding_site': 'distal', 'mechanism': 'compensatory'},
        'T107N': {'region': 'CTD', 'binding_site': 'distal', 'mechanism': 'unknown'},
    }

    return pd.DataFrame.from_dict(structural_annotations, orient='index')

def analyze_structure_resistance_correlation(df, struct_df):
    """分析结构位置与耐药程度的关联"""

    logging.info("\n=== Structure-Resistance Correlation ===")

    # 合并数据
    df_merged = df.merge(struct_df, left_on='Mutation', right_index=True, how='left')

    # 按结合位点分组
    binding_site_stats = df_merged.groupby('binding_site')['log10_FC'].agg([
        ('count', 'count'),
        ('mean', 'mean'),
        ('std', 'std')
    ]).round(3)

    logging.info("Resistance by binding site:")
    logging.info(binding_site_stats.to_string())

    # 按机制分组
    mechanism_stats = df_merged.groupby('mechanism')['log10_FC'].agg([
        ('count', 'count'),
        ('mean', 'mean'),
        ('std', 'std')
    ]).round(3)

    logging.info("\nResistance by mechanism:")
    logging.info(mechanism_stats.to_string())

    return df_merged, binding_site_stats, mechanism_stats

def pdb_structures():
    """记录相关PDB结构"""

    structures = {
        '6VKV': 'LEN bound to CA hexamer',
        '7RAO': 'Apo CA(M66I) hexamer',
        '9N0V': 'KFA-027 vs M66I'
    }

    logging.info("\n=== Related PDB Structures ===")
    for pdb_id, desc in structures.items():
        logging.info(f"{pdb_id}: {desc}")

    return structures

def main():
    logging.info("Starting Phase 2 Structure-Function Analysis")

    df = load_data()
    struct_df = annotate_structural_regions()

    logging.info(f"\nStructural annotations:")
    logging.info(struct_df.to_string())

    df_merged, binding_stats, mechanism_stats = analyze_structure_resistance_correlation(df, struct_df)
    pdb_info = pdb_structures()

    # 保存结果
    struct_df.to_csv('results/phase2/structural_annotations.csv')
    binding_stats.to_csv('results/phase2/binding_site_resistance.csv')
    mechanism_stats.to_csv('results/phase2/mechanism_resistance.csv')
    df_merged.to_csv('results/phase2/structure_resistance_merged.csv', index=False)

    logging.info("\nStructure-function analysis completed")

if __name__ == '__main__':
    main()
