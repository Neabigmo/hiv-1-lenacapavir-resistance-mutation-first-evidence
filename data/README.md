# 数据目录组织规范

## 目录结构

```
data/
├── raw/                    # 原始数据（不可变）
│   └── papers/            # 从文献提取的数据
├── interim/               # 中间处理结果
├── processed/             # 分析就绪数据
├── external/              # 外部数据库下载
├── curated/               # 人工整理数据
├── metadata/              # 数据集元数据
└── manifests/             # 数据清单和溯源
    ├── DATA_MANIFEST.csv      # 主数据清单
    └── DATA_PROVENANCE.md     # 详细溯源文档
```

## 数据不可变性原则

- `raw/` 目录下的文件**永不修改**
- 所有处理通过脚本生成新文件到 `interim/` 或 `processed/`
- 每次处理记录到 `logs/downloads/` 或 `logs/analysis/`

## 文件命名规范

### 原始数据
格式: `{source}_{topic}_{date}.csv`
- 示例: `pmc12077089_resistance_20260421.csv`

### 处理数据
格式: `{dataset}_{version}_{processing}.csv`
- 示例: `resistance_v2_cleaned.csv`

## 元数据要求

每个数据文件必须在 `DATA_MANIFEST.csv` 中有记录：
- file_path: 相对路径
- source: 数据来源（PMID/DOI/URL）
- download_date: 获取日期
- description: 简要说明
- status: complete/partial/path_issue

## 当前状态

- ✓ 原始数据: 31个CSV文件，309条记录
- ✓ 溯源文档: DATA_PROVENANCE.md 已创建
- ⏳ 统一格式数据集: 待创建
- ⏳ 质量控制检查: 待执行
