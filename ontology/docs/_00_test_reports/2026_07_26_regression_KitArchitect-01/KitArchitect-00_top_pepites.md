# Michel Top Pépites

1. `PEPITE-001` `/corpus/list` serializes graph IRIs as `<IRI>` and derives malformed names with trailing `>`.
2. `PEPITE-013` Non-numeric prose is typed as `xsd:float` in source JSON-LD and is queryable as such.
3. `PEPITE-005` `owl:inverseOf` objects are exposed in unresolved compact form (`m2:...`) rather than normalized IRIs.
4. `PEPITE-011` Corpus scope is highly configuration-sensitive; repo-root startup loads archives and fixtures, while the documented ontology-root still loads archives/docs recursively.
5. `PEPITE-003` Repeated core resources are mostly an archive-amplification/query-design hazard rather than automatically a conflicting-definition bug.