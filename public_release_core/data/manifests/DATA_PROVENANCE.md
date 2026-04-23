# 数据溯源清单

**最后更新**: 2026-04-22

## 原始数据文件 (data/raw/papers/)

### 临床试验数据
| 文件名 | 来源 | 论文/来源 | 提取日期 | 记录数 | 说明 |
|--------|------|-----------|----------|--------|------|
| capella_2year_resistance_data.csv | PMID39873394 | CAPELLA 2年数据 | 2026-04-21 | 13 | 治疗经验者耐药突变出现率 |
| capella_hiv2_clinical_isolates.csv | CAPELLA试验 | 临床分离株 | 2026-04-21 | 17 | HIV-2临床样本数据 |
| calibrate_week28_resistance.csv | CALIBRATE试验 | 28周耐药数据 | 2026-04-21 | 5 | Q67H+K70R临床出现 |
| clinical_trials_extracted_data.csv | 多来源 | 临床试验汇总 | 2026-04-21 | 7 | CAPELLA/CALIBRATE综合数据 |
| sunlenca_clinical_efficacy.csv | Sunlenca上市数据 | 临床疗效 | 2026-04-21 | 6 | 商品名Sunlenca疗效数据 |

### 体外实验数据
| 文件名 | 来源 | 论文/来源 | 提取日期 | 记录数 | 说明 |
|--------|------|-----------|----------|--------|------|
| mbio_2022_extracted_data.csv | mBio 2022 | Q67H/N74D结合亲和力 | 2026-04-21 | 11 | Kd和EC50数据 |
| pmc12077089_2026_extracted_data.csv | PMC12077089 | L56V/N57H高倍耐药 | 2026-04-21 | 8 | 72倍和4890倍FC |
| pmc12077089_extended_fitness.csv | PMC12077089 | 扩展适应度数据 | 2026-04-21 | 17 | 54个多态性变异 |
| pmc12077089_full_fitness_data.csv | PMC12077089 | 完整适应度 | 2026-04-21 | 9 | 感染性测定 |
| pmc11995365_2026_extracted_data.csv | PMC11995365 | RevLun表型分析 | 2026-04-21 | 9 | 多位点RAMs |

### 结构与机制数据
| 文件名 | 来源 | 论文/来源 | 提取日期 | 记录数 | 说明 |
|--------|------|-----------|----------|--------|------|
| pmc9600929_structural_mechanistic_data.csv | PMC9600929 | M66I结构机制 | 2026-04-21 | 13 | 空间位阻机制 |
| pmc9600929_structural_extended.csv | PMC9600929 | 扩展结构数据 | 2026-04-21 | 11 | 结合口袋分析 |
| structural_pk_data.csv | 多来源 | 结构-PK关联 | 2026-04-21 | 7 | 药代动力学 |
| pf74_compensatory_mutations.csv | PF74研究 | 补偿性突变 | 2026-04-21 | 7 | A105T补偿机制 |

### 自然多态性数据
| 文件名 | 来源 | 论文/来源 | 提取日期 | 记录数 | 说明 |
|--------|------|-----------|----------|--------|------|
| uganda_natural_polymorphisms.csv | JAC 2025 | 乌干达A1/D亚型 | 2026-04-21 | 3 | 0%主要RAMs |
| uganda_subtype_a1_d_2025.csv | JAC 2025 | A1/D详细数据 | 2026-04-21 | 11 | 546名参与者 |
| uganda_hiv2_quantitative.csv | 乌干达研究 | 定量多态性 | 2026-04-21 | 12 | HIV-2数据 |
| angola_diversity_data.csv | 安哥拉研究 | 遗传多样性 | 2026-04-21 | 7 | 非洲亚型分布 |
| subtype_polymorphism_data.csv | 多来源 | 亚型多态性汇总 | 2026-04-21 | 12 | 跨亚型比较 |
| global_subtype_distribution.csv | 全球监测 | 亚型分布 | 2026-04-21 | 8 | 全球流行病学 |

### 交叉耐药与药物相互作用
| 文件名 | 来源 | 论文/来源 | 提取日期 | 记录数 | 说明 |
|--------|------|-----------|----------|--------|------|
| pmc8092519_cross_resistance.csv | PMC8092519 | 交叉耐药 | 2026-04-21 | 8 | 与其他ARV类别 |
| pmc8092519_gcsm_data.csv | PMC8092519 | GCSM模型数据 | 2026-04-21 | 16 | 遗传背景模型 |
| drug_interactions_synergy.csv | PMC9229705 | 药物协同作用 | 2026-04-21 | 12 | LEN+ISL/RPV/CAB |

### 其他数据
| 文件名 | 来源 | 论文/来源 | 提取日期 | 记录数 | 说明 |
|--------|------|-----------|----------|--------|------|
| backbone_annotated_phenotypes.csv | 多来源 | 亚型标注表型 | 2026-04-21 | 7 | 遗传骨架分析 |
| subtype_annotated_resistance.csv | 多来源 | 亚型标注耐药 | 2026-04-21 | 12 | 耐药-亚型关联 |
| capsid_diversity_data.csv | 多来源 | 衣壳多样性 | 2026-04-21 | 17 | CA序列变异 |
| natap_lenacapavir_resistance_2022.csv | NATAP 2022 | 综述数据 | 2026-04-21 | 9 | 早期耐药报告 |
| natap_review_data.csv | NATAP | 综述汇总 | 2026-04-21 | 6 | 机制综述 |
| pharmacokinetics_data.csv | 多来源 | 药代动力学 | 2026-04-21 | 16 | PK参数 |
| lenacapavir_potency_data.csv | 多来源 | 效价数据 | 2026-04-21 | 2 | IC50/EC50 |
| additional_studies_extracted.csv | 补充研究 | 额外文献 | 2026-04-21 | 11 | 其他来源 |

## 数据质量评分

- **高质量 (3分)**: 同行评审期刊，定量FC数据，明确亚型标注
- **中等质量 (2分)**: 会议摘要，定性描述，部分亚型信息
- **低质量 (1分)**: 综述引用，缺失关键元数据

## 缺失数据识别

根据审稿人意见，以下数据需补充：
1. **L56V定量数据** - 已有72倍FC，需更多样本
2. **K70R临床数据** - CALIBRATE提到但缺乏FC数据
3. **自然多态性** - 当前仅8条记录，需扩充至50+
4. **多突变组合** - 需系统收集双突变/三突变数据
5. **适应度代价** - 需独立的复制能力测定数据

## 数据整合状态

- ✓ 原始CSV文件: 31个文件，309条记录
- ✓ 中间汇总: evidence_atlas_v3_summary.md
- ⏳ 统一格式数据集: 待创建
- ⏳ 分析就绪数据: 待创建
