# HIV-1 Lenacapavir Resistance: Mutation-First Evidence Synthesis

This repository contains code and data assets for a systematic evidence synthesis and comparative modeling study of HIV-1 lenacapavir (LEN) resistance.

## Recommended Public Entry Point

Use the minimal public release folder:

- `public_release_core/`

This folder is designed for clean reproducibility and includes:

- Rewritten core scripts (`public_release_core/code/`)
- Minimal processed data (`public_release_core/data/processed/revision_v2/`)
- Key raw-source subset (`public_release_core/data/raw_key/`)
- Audit mapping files (`public_release_core/metadata/`)

## Quick Reproduction

```bash
cd public_release_core
python code/01_build_harmonized_dataset.py
python code/02_model_comparison.py
python code/03_epistasis_and_context.py
python code/04_generate_main_figures.py
```

## Scientific Scope

- Current evidence boundary: 11 source records, 26 total observations, 23 complete-case observations for model fitting.
- Core interpretation: under current compiled phenotypic evidence, mutation identity is the most stable explanatory level; subtype contribution remains unresolved at current data depth.
- Validation framing: leave-one-source-record-out (LOSO), epistasis context checks, and structure/evolution support lines.

## Data/Source Documentation

- `DATA_SOURCES.md`
- `public_release_core/metadata/source_id_to_bibkey.csv`
- `public_release_core/metadata/source_to_claim_mapping.csv`
- `public_release_core/metadata/reproducibility_manifest.csv`
