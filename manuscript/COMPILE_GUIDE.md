# LaTeX编译指南

## 论文文件
- **主文件**: `manuscript/lenacapavir_resistance_revised.tex`
- **图表**: `manuscript/figures/figure[1-4]_*.pdf`

## 编译方法

### 方法1: 在线编译（推荐）
使用Overleaf (https://www.overleaf.com):
1. 上传 `lenacapavir_resistance_revised.tex`
2. 上传 `figures/` 文件夹中的所有PDF图表
3. 点击"Recompile"

### 方法2: 本地编译
需要安装TeX发行版：
- **Windows**: MiKTeX (https://miktex.org/download)
- **Mac**: MacTeX (https://www.tug.org/mactex/)
- **Linux**: TeX Live (`sudo apt-get install texlive-full`)

安装后运行：
```bash
cd manuscript
pdflatex lenacapavir_resistance_revised.tex
pdflatex lenacapavir_resistance_revised.tex  # 运行两次以更新引用
```

### 方法3: Docker编译
```bash
docker run --rm -v ${PWD}/manuscript:/data texlive/texlive pdflatex lenacapavir_resistance_revised.tex
```

## 输出文件
编译成功后生成: `lenacapavir_resistance_revised.pdf`

## 当前状态
✅ LaTeX源文件已完成
✅ 所有图表已生成（PDF格式）
⏸️ 等待编译（需要TeX环境）

## 快速预览
如果只想查看内容，可以：
1. 直接阅读 `.tex` 源文件
2. 查看 `figures/` 中的PNG图表
3. 阅读 `reports/phase2/PHASE2_COMPLETE_REPORT.md` 获取完整分析结果
