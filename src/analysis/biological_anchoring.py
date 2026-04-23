import pandas as pd
import numpy as np

def annotate_biological_context():
    """Add biological annotations to top mutations"""

    # Known capsid binding sites and clinical evolution data
    biological_annotations = {
        'N57H': {
            'binding_site': 'NTD-CTD interface',
            'clinical_evolution': 'Emerged in clinical trials (CAPELLA)',
            'fitness_cost': '<10% WT',
            'mechanism': 'Disrupts lenacapavir pocket binding',
            'fold_change': 2951
        },
        'M66I': {
            'binding_site': 'Hydrophobic pocket',
            'clinical_evolution': 'Most common resistance mutation',
            'fitness_cost': '<10% WT',
            'mechanism': 'Reduces hydrophobic interactions',
            'fold_change': 1950
        },
        'Q67H': {
            'binding_site': 'NTD-CTD interface',
            'clinical_evolution': 'Frequently paired with N74D',
            'fitness_cost': '~20% WT',
            'mechanism': 'Charge alteration affects binding',
            'fold_change': 5
        },
        'N74D': {
            'binding_site': 'NTD-CTD interface',
            'clinical_evolution': 'Synergistic with Q67H',
            'fitness_cost': '~15% WT',
            'mechanism': 'Electrostatic repulsion',
            'fold_change': 20
        },
        'K70R': {
            'binding_site': 'NTD helix',
            'clinical_evolution': 'Natural polymorphism in subtype A1',
            'fitness_cost': 'Minimal',
            'mechanism': 'Conservative substitution',
            'fold_change': 'Variable'
        },
        'A105T': {
            'binding_site': 'CTD',
            'clinical_evolution': 'Compensatory mutation',
            'fitness_cost': 'Restores fitness',
            'mechanism': 'Stabilizes capsid structure',
            'fold_change': 'Modulator'
        },
        'M66I+N74D+A105T': {
            'binding_site': 'Multi-site',
            'clinical_evolution': 'Triple mutant from CAPELLA',
            'fitness_cost': '<10% WT (A105T compensates)',
            'mechanism': 'Combined resistance + fitness restoration',
            'fold_change': 1337
        }
    }

    return pd.DataFrame.from_dict(biological_annotations, orient='index')

def map_to_capsid_structure():
    """Map mutations to capsid hexamer/pentamer structure"""

    structure_mapping = {
        'Region': ['NTD-CTD interface', 'Hydrophobic pocket', 'NTD helix', 'CTD'],
        'Residues': ['N57, Q67, N74', 'M66', 'K70', 'A105'],
        'Lenacapavir_Contact': ['Direct', 'Direct', 'Indirect', 'Indirect'],
        'Structural_Role': [
            'Inter-domain hinge',
            'Drug binding pocket',
            'Helix stability',
            'Hexamer interface'
        ]
    }

    return pd.DataFrame(structure_mapping)

def clinical_evolution_pathways():
    """Document observed clinical resistance pathways"""

    pathways = {
        'Pathway': [
            'CAPELLA primary',
            'CAPELLA secondary',
            'Natural polymorphism',
            'In vitro selection'
        ],
        'Mutations': [
            'M66I → M66I+N74D → M66I+N74D+A105T',
            'Q67H → Q67H+N74D',
            'K70R (subtype A1/D baseline)',
            'N57H, M66I (high-level resistance)'
        ],
        'Timeframe': [
            'Weeks to months',
            'Weeks to months',
            'Pre-existing',
            'Serial passage'
        ],
        'Clinical_Impact': [
            'Virologic failure',
            'Virologic failure',
            'Reduced susceptibility',
            'High-level resistance'
        ]
    }

    return pd.DataFrame(pathways)

if __name__ == '__main__':
    print("Biological annotations for top mutations:")
    bio_annot = annotate_biological_context()
    bio_annot.to_csv('results/validation/biological_annotations.csv')
    print(bio_annot)

    print("\nCapsid structure mapping:")
    struct_map = map_to_capsid_structure()
    struct_map.to_csv('results/validation/capsid_structure_mapping.csv', index=False)
    print(struct_map)

    print("\nClinical evolution pathways:")
    pathways = clinical_evolution_pathways()
    pathways.to_csv('results/validation/clinical_pathways.csv', index=False)
    print(pathways)
