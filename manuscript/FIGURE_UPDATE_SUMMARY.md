# HTML图片插入论文总结

## 完成的工作

### 1. HTML转图片
使用Playwright成功将7个HTML文件转换为高质量的PNG和PDF图片：

**生成的文件位置**: `manuscript/figures/revision_v2/html_renders/`

- `prisma_flow.pdf/png` (121KB/170KB)
- `harmonization_pipeline.pdf/png` (103KB/176KB)
- `surveillance_framework.pdf/png` (140KB/194KB)
- `resistance_pathway.pdf/png` (157KB/113KB)
- `figure4_structure_mechanisms.pdf/png` (92KB/194KB)
- `figure5_resistance_pathway.pdf/png` (124KB/78KB)
- `figure6_framework_bc.pdf/png` (109KB/198KB)

### 2. LaTeX文件更新

已更新 `manuscript/lenacapavir_revised_v2.tex`，包括：

#### 添加的包
```latex
\usepackage{subcaption}  % 支持子图
```

#### 更新的图片引用

**Figure 1 - Evidence Landscape**
- 原始: `figure1_evidence_landscape.pdf`
- 更新为: 使用subfigure组合
  - (A) `html_renders/prisma_flow.pdf` - PRISMA流程图
  - (B) `html_renders/harmonization_pipeline.pdf` - 数据协调管道

**Figure 4 - Structure-informed Mechanism**
- 原始: `figure4_structure.pdf`
- 更新为: `html_renders/figure4_structure_mechanisms.pdf`

**Figure 5 - Evolutionary and Fitness Context**
- 原始: `figure5_evolution.pdf`
- 更新为: `html_renders/figure5_resistance_pathway.pdf`

**Figure 6 - Claim Grading Framework**
- 原始: `figure6_framework.pdf`
- 更新为: `html_renders/figure6_framework_bc.pdf`

### 3. 其他HTML图片

以下HTML渲染图片已生成但未直接插入（可根据需要添加）：
- `surveillance_framework.pdf/png` - 监测框架
- `resistance_pathway.pdf/png` - 耐药路径

## 下一步

要编译更新后的LaTeX文档，请运行：

```bash
cd manuscript
pdflatex lenacapavir_revised_v2.tex
pdflatex lenacapavir_revised_v2.tex  # 第二次编译以更新引用
```

或使用XeLaTeX/LuaLaTeX：
```bash
xelatex lenacapavir_revised_v2.tex
```

## 文件结构

```
manuscript/
├── lenacapavir_revised_v2.tex (已更新)
└── figures/
    └── revision_v2/
        ├── html_renders/  (新增)
        │   ├── prisma_flow.pdf/png
        │   ├── harmonization_pipeline.pdf/png
        │   ├── figure4_structure_mechanisms.pdf/png
        │   ├── figure5_resistance_pathway.pdf/png
        │   ├── figure6_framework_bc.pdf/png
        │   ├── surveillance_framework.pdf/png
        │   └── resistance_pathway.pdf/png
        ├── figure1_evidence_landscape.pdf (原始)
        ├── figure2_core_evidence.pdf
        ├── figure3_interactions.pdf
        ├── figure4_structure.pdf (原始)
        ├── figure5_evolution.pdf (原始)
        └── figure6_framework.pdf (原始)
```

## 注意事项

1. 所有HTML渲染的图片都已生成为PDF和PNG两种格式
2. LaTeX文档中使用PDF格式以获得最佳打印质量
3. 原始的PDF图片文件仍然保留，可以随时恢复
4. 如需调整图片大小或布局，可以修改LaTeX中的width参数
