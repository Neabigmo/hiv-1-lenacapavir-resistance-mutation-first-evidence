# 数据整合清单

**创建日期**: 2026-04-22  
**数据来源**: 真实文献提取

## 已提取数据文件

1. `pmc9039614_capsid_diversity_extracted.csv` - 8条（保守性、流行率）
2. `natap2022_extracted_quantitative.csv` - 11条（EC50、临床疗效）
3. `pmc_extracted_batch1.csv` - 13条（Gag突变、大规模序列）
4. `pmc_extracted_batch2.csv` - 10条（PF74、GS-CA1、CypA结合）
5. `multi_source_batch_2026.csv` - 12条（HIV-2、PK、全球分布）
6. `resistance_trends_uganda_2025.csv` - 10条（耐药趋势、乌干达）
7. `clinical_trials_2025_extracted.csv` - 4条（临床试验）
8. `structural_mechanism_2025.csv` - 6条（结构、DDI、机制）
9. `assembly_calibrate_2025.csv` - 6条（IP6组装、CALIBRATE）
10. `data_expansion_summary.csv` - 3条（汇总）

## 数据统计

- **总记录数**: 约83条新提取数据
- **原始31文件**: 约309条
- **合计**: 约392条真实文献数据
- **数据源**: PMC/PubMed/Nature/Lancet/Oxford Academic
- **质量**: 全部Quality ≥ 2

## 关键突变覆盖

- M66I: 1950-3200倍
- N57H: 2951-4890倍
- L56V: 72倍
- Q67H: 5-7倍
- N74D: 10-20倍
- N73D (HIV-2): 30倍
- K70R: 临床出现

## 亚型覆盖

- Subtype A, A1, B, C, D, F, G
- CRF01_AE, CRF02_AG, CRF06_cpx
- HIV-2

## 数据类型

- 表型数据: fold change, EC50, IC50
- 临床数据: 出现率、抑制率
- 结构数据: PDB ID, 结合位点
- 药代动力学: 半衰期、Cmax
- 流行病学: 全球分布、流行率

## 下一步

1. 合并所有CSV文件
2. 去重与质控
3. 统一格式
4. 创建分析就绪数据集
