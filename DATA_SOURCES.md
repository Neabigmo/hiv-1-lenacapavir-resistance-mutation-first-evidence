# Data Sources

This repository contains code, processed data, and source records used for the LEN resistance evidence synthesis project.

## Primary Data Origin
- Publicly available peer-reviewed publications and trial reports on HIV-1 lenacapavir resistance.
- Public sequence and annotation resources (including HIV sequence compendia and regulatory prescribing information where referenced in manuscript methods).
- Extracted source tables are stored under `data/raw/papers/`.

## Data Layers In This Repository
- `data/raw/`: source extraction files and structural inputs.
- `data/interim/`: intermediate merged/annotated tables.
- `data/processed/`: analysis-ready datasets, including `revision_v2/` harmonized phenotype tables.
- `results/`: model outputs, sensitivity analyses, epistasis matrices, and structural/evolutionary summary outputs.

## Provenance Files
- `data/manifests/DATA_PROVENANCE.md`
- `data/manifests/DATA_MANIFEST.csv`
- `data/manifests/EXTRACTED_DATA_INVENTORY.md`
- `data/manifests/download_registry.csv`

## Public Reproducibility Entry Point
- Public minimal release: `public_release_core/`
- Rewritten core scripts: `public_release_core/code/`
- Minimal processed dataset: `public_release_core/data/processed/revision_v2/`
- Key raw-source subset (11 source records + controls): `public_release_core/data/raw_key/`
- Audit mapping: `public_release_core/metadata/source_id_to_bibkey.csv` and `public_release_core/metadata/source_to_claim_mapping.csv`

## Full Internal Workspace (Not Required For Public Reproduction)
- Historical analysis scripts: `scripts/revision_v2/`, `scripts/phase2/`, `scripts/revision/`
- Internal source modules: `src/`
- Submission packaging workspace: `submission_antiviral_research_single_folder/`

## Notes
- All data in this repository are from public sources and compiled for secondary analysis.
- No newly collected human-subject data are included.
