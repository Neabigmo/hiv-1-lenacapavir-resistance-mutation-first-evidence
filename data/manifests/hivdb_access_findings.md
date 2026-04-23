# HIVDB Data Access - Initial Findings

**Date**: 2026-04-21  
**Status**: Investigating access methods

## Identified Resources

### Sierra Web Service
- **GitHub**: https://github.com/hivdb/sierra
- **Client**: https://github.com/hivdb/sierra-client (Python, SierraPy 0.4.3)
- **GraphQL Endpoint**: Typically at `/sierra/rest/graphql` or `/WebApplications/rest/graphql`
- **Documentation**: PMC7068798 - "The HIVdb System for HIV-1 Genotypic Resistance Interpretation"

### Key Papers with Data
1. [Structural and Mechanistic Bases of Viral Resistance to HIV-1 Capsid Inhibitor Lenacapavir](https://pmc.ncbi.nlm.nih.gov/articles/PMC9600929/) - mBio 2022
2. [Recurrent and novel evolutionary pathways drive in vitro HIV-1 lenacapavir resistance](https://www.nature.com/articles/s41467-026-70119-6) - Nature Comms 2026
3. [Lenacapavir treatment-emergent HIV-1 capsid resistance mutations are frequently associated with replication defects](https://pubmed.ncbi.nlm.nih.gov/41499523/) - 2026
4. [Impact of HIV-1 capsid polymorphisms on viral infectivity and susceptibility to lenacapavir](https://pmc.ncbi.nlm.nih.gov/articles/PMC12077089/) - 2026

## Next Steps

1. **Test Sierra GraphQL API**: Query for capsid/lenacapavir data
2. **Extract data from key papers**: Download supplementary datasets
3. **Check LANL HIV Database**: For LEN-naïve sequences
4. **Contact HIVDB team**: If bulk data access needed

## Blockers

- HIVDB website pages return minimal content (may need direct API access)
- GraphQL schema unknown (need introspection query)
- Unclear if lenacapavir data is in public HIVDB or only in papers

## Data Sources to Prioritize

1. Published papers with supplementary data (immediate access)
2. Sierra API (if capsid data available)
3. LANL HIV Sequence Database (for natural polymorphism)
4. Direct author contact for unpublished datasets
