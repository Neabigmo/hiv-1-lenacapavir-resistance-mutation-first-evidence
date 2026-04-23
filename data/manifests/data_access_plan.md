# HIVDB Data Access Plan

**Project**: Lenacapavir Resistance Interpretability  
**Created**: 2026-04-21

## Data Sources

### Stanford HIVDB
- URL: https://hivdb.stanford.edu/
- Primary resource for HIV drug resistance data

## Required Datasets

### 1. Capsid Phenotype Data
**Endpoint**: Likely via HIVDB download page or API
**Content**: 
- Mutation-phenotype associations for lenacapavir
- Fold-change (FC) in susceptibility
- IC50 values
- Mutation combinations

**Access method**:
- Check HIVDB download page: https://hivdb.stanford.edu/pages/download.html
- Check for API: https://hivdb.stanford.edu/page/webservice/
- If restricted: contact HIVDB team for data sharing agreement

### 2. Inhibitor-Mutation Data
**Content**:
- Mutations selected under LEN pressure in vitro
- Selection frequency
- Genetic barriers
- Reversion patterns

**Access method**:
- HIVDB mutation comments/notes
- Published selection studies linked from HIVDB
- Supplementary data from key papers

### 3. In Vitro Selection Data
**Content**:
- Serial passage experiments
- Mutation emergence timelines
- Fitness measurements
- Replication kinetics

**Access method**:
- Literature extraction (from search strategy)
- Direct data requests to authors if needed
- Supplementary datasets

## HIVDB API/Download Options

### Option 1: Bulk Download
- Check for CSV/TSV exports of capsid mutation data
- Download resistance interpretation rules
- Download mutation prevalence data

### Option 2: API Access
- Sierra GraphQL API (if available for capsid)
- Programmatic access for large-scale queries
- Rate limiting considerations

### Option 3: Manual Extraction
- If no bulk/API: systematic manual extraction
- Use structured templates
- Double-entry validation

## Data Validation

### Quality checks:
1. Cross-reference with published literature
2. Check for missing values
3. Verify mutation nomenclature (HXB2 reference)
4. Validate fold-change ranges (biological plausibility)

### Provenance tracking:
- Record download date
- Record HIVDB version/release
- Save raw files in `data/raw/hivdb/`
- Document any transformations in `data/metadata/`

## Global Sequence Collection

### LEN-Naïve Sequences
**Sources**:
- Los Alamos HIV Sequence Database (LANL)
- GenBank
- GISAID (if available for HIV)

**Criteria**:
- Capsid gene (gag p24) sequences
- Pre-2022 (before widespread LEN use)
- Subtype/CRF annotated
- Geographic diversity

**Access**:
- LANL: https://www.hiv.lanl.gov/
- GenBank: NCBI Nucleotide database
- Bulk download via API or web interface

### Sample Size Target
- Minimum 1000 sequences per major subtype (A, B, C, D, CRF01_AE, CRF02_AG)
- Include rare subtypes if n>50

## Data Registry

Maintain in: `data/manifests/download_registry.csv`

Columns:
- Source
- Dataset name
- Download date
- URL
- Local path
- File size
- Checksum (if available)
- Access method
- License/terms
- Status (pending/complete/blocked)

## Blockers and Escalation

### Potential blockers:
1. HIVDB data requires institutional access
2. API rate limits
3. Sequence databases require registration
4. Data use agreements needed

### Escalation path:
If blocked, create: `reports/handoff/USER_ACTION_REQUIRED.md`

Document:
- Exact resource
- Access barrier
- Required credentials/approvals
- Expected timeline

## Timeline

- Week 1 Day 1-2: Explore HIVDB access options
- Week 1 Day 3-4: Download/extract HIVDB data
- Week 1 Day 5-7: Collect global sequences from LANL/GenBank
- Week 2: Validate and document all data sources
