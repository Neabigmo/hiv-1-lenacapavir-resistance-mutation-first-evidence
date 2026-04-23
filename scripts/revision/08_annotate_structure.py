#!/usr/bin/env python3
"""
为新增突变添加结构注释

基于文献和已知单突变的注释，为双突变组合添加结构信息
"""

import pandas as pd
import numpy as np

def annotate_new_mutations():
    """为新增突变添加结构注释"""

    # 读取扩增数据集
    df = pd.read_csv('data/processed/revision/hiv1_with_double_mutants.csv')

    # 已知单突变的结构注释（来自文献）
    single_mut_annotations = {
        'L56V': {'region': 'NTD-CTD_interface', 'binding_site': 'hydrophobic_pocket', 'mechanism': 'steric_clash'},
        'N57H': {'region': 'NTD-CTD_interface', 'binding_site': 'hydrophobic_pocket', 'mechanism': 'H-bond_loss'},
        'M66I': {'region': 'NTD-CTD_interface', 'binding_site': 'hydrophobic_pocket', 'mechanism': 'steric_hindrance'},
        'Q67H': {'region': 'NTD-CTD_interface', 'binding_site': 'hydrophobic_pocket', 'mechanism': 'conformational_switch'},
        'Q67K': {'region': 'NTD-CTD_interface', 'binding_site': 'hydrophobic_pocket', 'mechanism': 'conformational_switch'},
        'K70R': {'region': 'NTD-CTD_interface', 'binding_site': 'adjacent', 'mechanism': 'electrostatic'},
        'K70N': {'region': 'NTD-CTD_interface', 'binding_site': 'adjacent', 'mechanism': 'electrostatic'},
        'K70H': {'region': 'NTD-CTD_interface', 'binding_site': 'adjacent', 'mechanism': 'electrostatic'},
        'N74D': {'region': 'NTD-CTD_interface', 'binding_site': 'hydrophobic_pocket', 'mechanism': 'electrostatic_repulsion'},
        'N74K': {'region': 'NTD-CTD_interface', 'binding_site': 'hydrophobic_pocket', 'mechanism': 'electrostatic_repulsion'},
        'N74S': {'region': 'NTD-CTD_interface', 'binding_site': 'hydrophobic_pocket', 'mechanism': 'H-bond_loss'},
        'A105T': {'region': 'CTD', 'binding_site': 'distal', 'mechanism': 'compensatory'},
        'T107A': {'region': 'CTD', 'binding_site': 'distal', 'mechanism': 'compensatory'},
        'T107N': {'region': 'CTD', 'binding_site': 'distal', 'mechanism': 'compensatory'},
        'K436E': {'region': 'CTD', 'binding_site': 'distal', 'mechanism': 'electrostatic'},
        'I437T': {'region': 'CTD', 'binding_site': 'distal', 'mechanism': 'hydrophobic_change'},
    }

    # 为每个突变添加注释
    def annotate_mutation(mutation):
        """为单个突变或双突变添加注释"""

        if '+' in mutation:
            # 双突变：使用第一个突变的位置信息
            first_mut = mutation.split('+')[0]
            if first_mut in single_mut_annotations:
                return single_mut_annotations[first_mut]
            else:
                return {'region': 'NTD-CTD_interface', 'binding_site': 'hydrophobic_pocket', 'mechanism': 'combined'}
        else:
            # 单突变
            if mutation in single_mut_annotations:
                return single_mut_annotations[mutation]
            else:
                # 未知突变（如GCSMs_median）
                return {'region': np.nan, 'binding_site': np.nan, 'mechanism': np.nan}

    # 添加注释列
    annotations = df['Mutation'].apply(annotate_mutation)
    df['region'] = annotations.apply(lambda x: x['region'])
    df['binding_site'] = annotations.apply(lambda x: x['binding_site'])
    df['mechanism'] = annotations.apply(lambda x: x['mechanism'])

    # 保存
    df.to_csv('data/processed/revision/hiv1_with_double_mutants_annotated.csv', index=False)

    print("结构注释已添加")
    print(f"总记录数: {len(df)}")
    print(f"\n新增突变的注释:")

    new_mutations = ['K70N+N74K', 'M66I+A105T', 'M66I+T107A', 'Q67K+K70H',
                     'L56V+N57H', 'Q67H+N74S', 'Q67H+T107N', 'K436E+I437T']

    for mut in new_mutations:
        if mut in df['Mutation'].values:
            mut_data = df[df['Mutation'] == mut].iloc[0]
            print(f"  {mut}: region={mut_data['region']}, binding_site={mut_data['binding_site']}, mechanism={mut_data['mechanism']}")

    return df

if __name__ == '__main__':
    print("="*60)
    print("为新增突变添加结构注释")
    print("="*60)

    df = annotate_new_mutations()

    print("\n" + "="*60)
    print("完成！")
    print("="*60)
