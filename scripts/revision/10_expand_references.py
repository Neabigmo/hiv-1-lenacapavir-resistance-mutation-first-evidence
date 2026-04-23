#!/usr/bin/env python3
"""
扩充参考文献列表
添加10-15篇高质量相关文献，确保真实性
"""

# 扩充后的完整参考文献列表（所有文献均为真实发表）
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
        'authors': 'Margot N, Naik V, Cheng AK, Rhee MS, Chiu A, Andreatta K.',
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
        'pmid': '39266540'
    },
    'Yant2022': {
        'authors': 'Yant SR, Mulato A, Hansen D, Tse WC, Niedziela-Majka A, Zhang JR, et al.',
        'title': 'Structural and mechanistic bases of viral resistance to HIV-1 capsid inhibitor lenacapavir',
        'journal': 'mBio',
        'year': '2022',
        'volume': '13',
        'issue': '5',
        'pages': 'e01804-22',
        'doi': '10.1128/mbio.01804-22',
        'pmid': '36154208'
    },
    'Rhee2016': {
        'authors': 'Rhee SY, Sankaran K, Varghese V, Winters MA, Hurt CB, Eron JJ, et al.',
        'title': 'HIV-1 protease, reverse transcriptase, and integrase variation',
        'journal': 'J Virol',
        'year': '2016',
        'volume': '90',
        'issue': '13',
        'pages': '6058-6070',
        'doi': '10.1128/JVI.00495-16',
        'pmid': '27099321'
    },
    # 新增文献 - HIV-1 capsid structure
    'Mattei2016': {
        'authors': 'Mattei S, Glass B, Hagen WJ, Kräusslich HG, Briggs JA.',
        'title': 'The structure and flexibility of conical HIV-1 capsids determined within intact virions',
        'journal': 'Science',
        'year': '2016',
        'volume': '354',
        'issue': '6318',
        'pages': '1434-1437',
        'doi': '10.1126/science.aah4972',
        'pmid': '27980210'
    },
    # 新增文献 - PF74 capsid inhibitor
    'Blair2010': {
        'authors': 'Blair WS, Pickford C, Irving SL, Brown DG, Anderson M, Bazin R, et al.',
        'title': 'HIV capsid is a tractable target for small molecule therapeutic intervention',
        'journal': 'PLoS Pathog',
        'year': '2010',
        'volume': '6',
        'issue': '12',
        'pages': 'e1001220',
        'doi': '10.1371/journal.ppat.1001220',
        'pmid': '21170360'
    },
    # 新增文献 - Epistasis in HIV resistance
    'Hinkley2011': {
        'authors': 'Hinkley T, Martins J, Chappey C, Haddad M, Stawiski E, Whitcomb JM, et al.',
        'title': 'A systems analysis of mutational effects in HIV-1 protease and reverse transcriptase',
        'journal': 'Nat Genet',
        'year': '2011',
        'volume': '43',
        'issue': '5',
        'pages': '487-489',
        'doi': '10.1038/ng.795',
        'pmid': '21441930'
    },
    # 新增文献 - Compensatory mutations
    'Martinez2008': {
        'authors': 'Martinez-Picado J, Martínez MA.',
        'title': 'HIV-1 reverse transcriptase inhibitor resistance mutations and fitness: a view from the clinic and ex vivo',
        'journal': 'Virus Res',
        'year': '2008',
        'volume': '134',
        'issue': '1-2',
        'pages': '104-123',
        'doi': '10.1016/j.virusres.2007.12.021',
        'pmid': '18289713'
    },
    # 新增文献 - HIV-1 diversity and subtypes
    'Hemelaar2019': {
        'authors': 'Hemelaar J, Elangovan R, Yun J, Dickson-Tetteh L, Fleminger I, Kirtley S, et al.',
        'title': 'Global and regional molecular epidemiology of HIV-1, 1990-2015: a systematic review, global survey, and trend analysis',
        'journal': 'Lancet Infect Dis',
        'year': '2019',
        'volume': '19',
        'issue': '2',
        'pages': '143-155',
        'doi': '10.1016/S1473-3099(18)30647-9',
        'pmid': '30509777'
    },
    # 新增文献 - Subtype-specific resistance
    'Kantor2005': {
        'authors': 'Kantor R, Katzenstein DA, Efron B, Carvalho AP, Wynhoven B, Cane P, et al.',
        'title': 'Impact of HIV-1 subtype and antiretroviral therapy on protease and reverse transcriptase genotype: results of a global collaboration',
        'journal': 'PLoS Med',
        'year': '2005',
        'volume': '2',
        'issue': '4',
        'pages': 'e112',
        'doi': '10.1371/journal.pmed.0020112',
        'pmid': '15839752'
    },
    # 新增文献 - Hierarchical modeling
    'Wensing2019': {
        'authors': 'Wensing AM, Calvez V, Ceccherini-Silberstein F, Charpentier C, Günthard HF, Paredes R, et al.',
        'title': 'Update of the drug resistance mutations in HIV-1',
        'journal': 'Top Antivir Med',
        'year': '2019',
        'volume': '27',
        'issue': '3',
        'pages': '111-121',
        'doi': '10.32873/unl.dc.tmr.27.3.111',
        'pmid': '31570887'
    },
    # 新增文献 - Capsid function
    'Ganser2019': {
        'authors': 'Ganser-Pornillos BK, Pornillos O.',
        'title': 'Restriction of HIV-1 and other retroviruses by TRIM5',
        'journal': 'Nat Rev Microbiol',
        'year': '2019',
        'volume': '17',
        'issue': '9',
        'pages': '546-556',
        'doi': '10.1038/s41579-019-0225-2',
        'pmid': '31267065'
    },
    # 新增文献 - Structure-based drug design
    'Rankovic2018': {
        'authors': 'Rankovic S, Ramalho R, Aiken C, Rousso I.',
        'title': 'PF74 reinforces the HIV-1 capsid to impair reverse transcription-induced uncoating',
        'journal': 'J Virol',
        'year': '2018',
        'volume': '92',
        'issue': '20',
        'pages': 'e00845-18',
        'doi': '10.1128/JVI.00845-18',
        'pmid': '30068653'
    }
}

def generate_latex_bibliography():
    """生成LaTeX格式的参考文献（Vancouver格式）"""
    latex = "\\begin{thebibliography}{99}\n"

    for key, ref in references.items():
        latex += f"\\bibitem{{{key}}} {ref['authors']} {ref['title']}. "
        latex += f"\\textit{{{ref['journal']}}} {ref['year']};{ref['volume']}"
        if 'issue' in ref:
            latex += f"({ref['issue']})"
        latex += f":{ref['pages']}. "
        latex += f"https://doi.org/{ref['doi']}\n\n"

    latex += "\\end{thebibliography}\n"
    return latex

if __name__ == '__main__':
    print("="*60)
    print("扩充参考文献列表")
    print("="*60)

    # 保存LaTeX格式
    latex = generate_latex_bibliography()
    with open('manuscript/references_expanded.txt', 'w', encoding='utf-8') as f:
        f.write(latex)
    print(f"LaTeX格式已保存到: manuscript/references_expanded.txt")

    print(f"\n总计文献数: {len(references)}")
    print("\n新增文献:")
    new_refs = ['Mattei2016', 'Blair2010', 'Hinkley2011', 'Martinez2008',
                'Hemelaar2019', 'Kantor2005', 'Wensing2019', 'Ganser2019', 'Rankovic2018']
    for i, key in enumerate(new_refs, 1):
        ref = references[key]
        print(f"{i}. {ref['authors'].split(',')[0]} et al. {ref['journal']} {ref['year']} (PMID: {ref['pmid']})")
