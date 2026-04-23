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

## Reproducibility Entry Points
- Analysis scripts: `scripts/revision_v2/` and `scripts/phase2/`
- Source modules: `src/`
- Submission-ready package: `submission_antiviral_research_single_folder/`

## Notes
- All data in this repository are from public sources and compiled for secondary analysis.
- No newly collected human-subject data are included.
