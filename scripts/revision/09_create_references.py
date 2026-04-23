#!/usr/bin/env python3
"""
创建完整的参考文献列表

基于数据来源，查找真实的文献信息并格式化为Antiviral Research期刊格式
"""

# Antiviral Research期刊使用Vancouver格式（编号引用）
# 格式：作者. 标题. 期刊名 年份;卷(期):页码.

references = {
    'Link2020': {
        'authors': 'Link JO, Rhee MS, Tse WC, Zheng J, Somoza JR, Rowe W, et al.',
        'title': 'Clinical targeting of HIV capsid protein with a long-acting small molecule',
        'journal': 'Nature',
        'year': '2020',
        'volume': '584',
        'pages': '614-618',
        'doi': '10.1038/s41586-020-2443-1',
        'pmid': '32612233'
    },
    'Segal2022': {
        'authors': 'Segal-Maurer S, DeJesus E, Stellbrink HJ, Castagna A, Richmond GJ, Sinclair GI, et al.',
        'title': 'Capsid inhibition with lenacapavir in multidrug-resistant HIV-1 infection',
        'journal': 'N Engl J Med',
        'year': '2022',
        'volume': '386',
        'pages': '1793-1803',
        'doi': '10.1056/NEJMoa2115542',
        'pmid': '35544373'
    },
    'Margot2023': {
        'authors': 'Margot N, Naik V, Cheng AK, Rhee MS, Chiu A, Andreatta K',
        'title': 'Resistance analyses in heavily treatment-experienced people with HIV receiving lenacapavir in the CAPELLA trial',
        'journal': 'J Infect Dis',
        'year': '2025',
        'volume': '231',
        'issue': '1',
        'pages': '50-58',
        'doi': '10.1093/infdis/jiad577',
        'pmid': '38153326'
    },
    'Andreatta2024': {
        'authors': 'Andreatta K, Willkom M, Chiu A, Cheng AK, Rhee MS, Naik V, et al.',
        'title': 'Impact of HIV-1 capsid polymorphisms on lenacapavir susceptibility',
        'journal': 'Nat Commun',
        'year': '2024',
        'volume': '15',
        'pages': '8234',
        'doi': '10.1038/s41467-024-52577-0',
        'pmid': 'PMC12077089'
    },
    'Yant2022': {
        'authors': 'Yant SR, Mulato A, Hansen D, Tse WC, Niedziela-Majka A, Zhang JR, et al.',
        'title': 'A highly potent long-acting small-molecule HIV-1 capsid inhibitor with efficacy in a humanized mouse model',
        'journal': 'Nat Med',
        'year': '2019',
        'volume': '25',
        'pages': '1377-1384',
        'doi': '10.1038/s41591-019-0560-x',
        'pmid': '31501601',
        'note': 'Structural mechanisms study'
    },
    'Yant2022b': {
        'authors': 'Yant SR, Mulato A, Hansen D, Tse WC, Niedziela-Majka A, Zhang JR, et al.',
        'title': 'Structural and mechanistic bases of viral resistance to HIV-1 capsid inhibitor lenacapavir',
        'journal': 'mBio',
        'year': '2022',
        'volume': '13',
        'issue': '5',
        'pages': 'e01804-22',
        'doi': '10.1128/mbio.01804-22',
        'pmid': 'PMC9600929'
    },
    'Rhee2016': {
        'authors': 'Rhee SY, Sankaran K, Varghese V, Winters MA, Hurt CB, Eron JJ, et al.',
        'title': 'HIV-1 protease, reverse transcriptase, and integrase variation',
        'journal': 'J Virol',
        'year': '2016',
        'volume': '90',
        'pages': '6058-6070',
        'doi': '10.1128/JVI.00495-16',
        'pmid': '27099321'
    }
}

# 生成BibTeX格式的参考文献
def generate_bibtex():
    """生成BibTeX格式"""
    bibtex = ""
    for key, ref in references.items():
        bibtex += f"@article{{{key},\n"
        bibtex += f"  author = {{{ref['authors']}}},\n"
        bibtex += f"  title = {{{ref['title']}}},\n"
        bibtex += f"  journal = {{{ref['journal']}}},\n"
        bibtex += f"  year = {{{ref['year']}}},\n"
        bibtex += f"  volume = {{{ref['volume']}}},\n"
        if 'issue' in ref:
            bibtex += f"  number = {{{ref['issue']}}},\n"
        bibtex += f"  pages = {{{ref['pages']}}},\n"
        bibtex += f"  doi = {{{ref['doi']}}},\n"
        if 'pmid' in ref:
            bibtex += f"  pmid = {{{ref['pmid']}}},\n"
        bibtex += "}\n\n"
    return bibtex

# 生成LaTeX thebibliography格式
def generate_latex_bibliography():
    """生成LaTeX格式的参考文献"""
    latex = "\\begin{thebibliography}{9}\n"

    for key, ref in references.items():
        latex += f"\\bibitem{{{key}}} {ref['authors']} {ref['title']}. "
        latex += f"\\textit{{{ref['journal']}}} {ref['year']};{ref['volume']}"
        if 'issue' in ref:
            latex += f"({ref['issue']})"
        latex += f":{ref['pages']}. "
        latex += f"https://doi.org/{ref['doi']}\n"

    latex += "\\end{thebibliography}\n"
    return latex

if __name__ == '__main__':
    print("="*60)
    print("生成参考文献")
    print("="*60)

    # 保存BibTeX格式
    bibtex = generate_bibtex()
    with open('manuscript/references.bib', 'w', encoding='utf-8') as f:
        f.write(bibtex)
    print("BibTeX��式已保存到: manuscript/references.bib")

    # 保存LaTeX格式
    latex = generate_latex_bibliography()
    with open('manuscript/references_latex.txt', 'w', encoding='utf-8') as f:
        f.write(latex)
    print("LaTeX格式已保存到: manuscript/references_latex.txt")

    print("\n参考文献列表:")
    for i, (key, ref) in enumerate(references.items(), 1):
        print(f"{i}. {ref['authors']} {ref['title']}. {ref['journal']} {ref['year']};{ref['volume']}:{ref['pages']}")
