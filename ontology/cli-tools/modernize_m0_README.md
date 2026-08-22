# `modernize_m0.py` — M0 instance modernizer (check-M0, Path B) · v2

**Author:** Echopraxium with the collaboration of Claude AI
**Location:** `ontology/cli-tools/modernize_m0.py`
**Companion gate:** `ontology/cli-tools/check-M0/check_m0_instances.py`

A batch-remediation helper that brings an older, non-conformant `M0_*.jsonld`
instance toward **check-M0** conformance — **without polluting the shared
`M0_Common` namespace**. It handles the *mechanical* modernization; it never
invents semantics.

---

## Why it exists

A repo-wide scan showed most instances failing the check-M0 gate for the same
recurring, structural reasons: the `m0:` prefix pointed at the **instance file**
instead of `M0_Common#`, the local alias `m0.<inst>:` was missing, `owl:imports`
lacked `M0_Common`, retired `@context` aliases (`m1core:`, `m1chem:`, `sm:`,
`*_score`) lingered, scores were inline-typed or nested, and enum values were
plain strings. Fixing these by hand, instance by instance, is slow and
error-prone. This tool encodes the fix once.

## The core decision it implements — **Path B**

When `m0:` is repointed to `M0_Common#`, every ad-hoc property an instance
invented under `m0:` (e.g. `m0:effector`, `m0:guytonModel`) would suddenly
resolve into the **shared** `M0_Common#` namespace. That passes the gate (the
IRIs are absolute) but is semantically wrong: it dumps instance-specific
concepts into the joinable shared vocabulary, risking cross-instance collisions.

**Path B** avoids that. A property stays under `m0:` **only if its first segment
is in the shared whitelist** read live from the check-M0 SHACL schema
(`scoreA…scoreV`, `asfidMean`, `revoiMean`, `epistemicGap`, `domain`, `focal*`,
`facet`, `roleGrounding`, `scoringStatus`, `spectralClass`, `version`,
`illustratesConcept`, the enum classes `Facet`/`FocalClass`/… etc.). **Everything
else is instance-local and is reclassified to `m0.<inst>:`.** The whitelist is
never hard-coded — it is extracted from the schema at run time, so it tracks the
schema.

## What it does, step by step

1. **`@context` surgery**
   - `m0:` → `https://…/ontology/M0_Common.jsonld#` (fixes **C02**).
   - adds `m0.<camelInstance>:` → the instance file's URL (fixes **C03**). The
     camel form matches the gate's own `_camel()` (e.g. `BloodPressureControl`
     → `m0.bloodPressureControl`).
   - **migrates or deletes** retired aliases (fixes **C07/C08**). Crucially it
     *migrates* an alias that is still used in the body rather than deleting it
     (deleting a used alias would leave unresolved, non-absolute IRIs and fail
     C15): `m1core:` → `m1:`, and any `m1<domain>:` short alias → `m1.ext:<domain>:`
     (e.g. `m1phys:` → `m1.ext:physics:`). Unused aliases (and `sm:`, `*_score`)
     are dropped.
   - forces `m1`/`m2`/`m3` prefixes to absolute HTTPS if they were relative
     (fixes **C05**).

2. **`owl:imports`** — rewritten to absolute URLs, `M0_Common.jsonld` added if
   missing (fixes **C09**).

3. **Path B reclassification** — every `m0:X` token (property keys *and* `@id`
   values, including the double-colon `m0:<Inst>:Y` form) is kept under `m0:`
   if `X`'s first segment is in the whitelist, otherwise rewritten to
   `m0.<inst>:X`.

4. **Score normalization**
   - **C10** — score props stored as `{"@value":…,"@type":"xsd:float"}` are
     de-wrapped to bare numerics.
   - **C15 (nested)** — obsolete `m0:asfidScores{}` / `m0:revoiScores{}`
     sub-objects are flattened to the flat root props `m0:scoreA…m0:scoreIm`
     (bare). Their `mean` becomes `m0:asfidMean` / `m0:revoiMean`, and
     `m0:epistemicGap` is (re)computed as `|asfidMean − revoiMean| / √2` when
     absent. (The retired `It_score` slot inside a `revoiScores` block maps to
     `m0:scoreIm`.)

5. **Enum → IRI (C11)** — string enum values are converted to IRI nodes using
   the schema's dotted convention: `"m0:spectralClass": "OnCriticalLine"` →
   `{"@id": "m0:spectralClass.OnCriticalLine"}`. Covers `spectralClass`,
   `focalClass`, `scoringStatus`.

6. **`ontologyType` dedup (C13)** — `m3:ontologyType` is stripped from every
   `@graph` node except `@graph[0]` (it must live only on the ontology node).

7. **Tensor reform hook (guarded, no-op when absent)** — renames the retired
   formula property `m0:tensorFormula` / `m0:hasStructuralGrammarFormula` to the
   canonical `m2:hasStructuralGrammarFormula`. *(The `⊗`→`×` reform of formula
   **values** is not yet wired in — see Limitations.)*

8. **ORIVE hygiene** — replaces the vestige acronym `ORIVE` with `REVOI` in
   prose values (the gate tolerates it inside a string, but the notation rule
   forbids it).

9. **Reports, never guesses** — prints a JSON summary: `reclassified_local`,
   `alias_migrations`, `debared_scores`, `flattened_nested`, `enum_iris`,
   `ontologyType_stripped`, `residual_orive`, and a `semantic_gaps` list flagging
   anything it will **not** fill in (`m1:domain`, `m3:ontologyType`). Two
   safety flags may also appear: `CASING_WARNING` and `UNRESOLVED_PREFIXES`.

## Two safety nets

- **`m1core` dangling-alias migration.** `m1core:` is a universally retired alias
  for `M1_CoreConcepts`. The tool migrates `m1core:` → `m1:` in the body **even
  when it was never declared in `@context`** (a dangling prefix such as
  `m1core:simulationTitle`, which would otherwise fail C15 as a non-absolute IRI).

- **Unresolved-prefix detector.** After all migrations, the tool checks every
  `"<prefix>:` still used in the body against the declared/standard prefixes and
  reports any leftovers as **`UNRESOLVED_PREFIXES`** — so a dangling alias is
  surfaced in the report instead of silently failing the gate.

## Casing guardrail (folder vs file)

The gate derives an instance's name from its **file** stem (`M0_<name>` →
`<name>`). A folder may hold several instances (e.g. `Bmc/` has `M0_Bmc` **and**
`M0_BmcSimulation`), so the file stem — not the folder — is the identity. The
only real hazard is a **case-only** drift of the *same* name: folder `Vco` with
file `M0_VCO.jsonld` resolves to `VCO` on case-sensitive Linux/CI but `Vco` on
case-insensitive Windows, so the expected `m0.<inst>:` alias disagrees across
platforms.

The tool detects exactly that case (folder and file stem equal
case-insensitively but differ in case), takes the **folder** casing as canonical,
and emits a **`CASING_WARNING`** with the exact case-safe two-step `git mv` to
rename the file to `M0_<folder>.jsonld`. Rename the file, then re-gate — the
alias will match on every platform. When folder and file names simply differ
(multiple instances per folder), no warning is raised and the file stem is used.

## What it does NOT do (by design)

- It never invents **semantic** content. Missing `m1:domain` or
  `m3:ontologyType`, and the **content** of formulas, are the Head Chef's
  decisions — the tool flags them in `semantic_gaps`, you supply them.
- It does not transform `⊗` inside formula **values** (see Limitations).

## Usage

Run from **anywhere** (the schema is resolved relative to the script), passing
the instance path:

```bash
python ontology/cli-tools/modernize_m0.py instances/poclets/PhaseTransition/M0_PhaseTransition.jsonld
```

It **rewrites the file in place**, then prints its report. Always re-gate after
(both must be green):

```bash
python ontology/cli-tools/check-M0/check_m0_instances.py --instance PhaseTransition
python ontology/TSCG_InstanceGrammar/validate_m0_instance.py instances/poclets/PhaseTransition/M0_PhaseTransition.jsonld
```

Then `git add` the single file by path and commit.

> **In place** means: work on a clean git tree so `git diff` shows exactly what
> changed, and you can `git checkout --` to revert if a report flags something
> you want to review first. If the report shows a `CASING_WARNING`, do the
> `git mv` it prints **before** committing.

## Provenance / safety notes

- Encoding-safe: writes with `ensure_ascii=False` (never escapes operators or
  glyphs); JSON validity is preserved.
- ORIVE-safe: the tool runs locally and writes locally — no server write-path,
  so it cannot silently corrupt `REVOI → ORIVE`. Still, it greps for `orive`
  and reports the residual count.

## Limitations / roadmap

- **Formula values (`⊗`→`×`)** are not yet transformed. Instances that fail
  **C12** on `⊗` inside values (Groups A and C of the campaign) need that step
  added and validated on the colour lot (CMY/CMYK/HSL) before generalizing,
  under **Politique 1** (mechanical `⊗`→`×`, atoms `S→St`/`It`; Map-segment
  `I→Im` reviewed case by case).
- **Known data bug:** `TscgOntologyAPIServer` stores prose text in `xsd:float`
  fields — a separate authoring fix, not something this tool should paper over.
- **Special structures** (e.g. `BmcSimulation`, a simulation-config instance)
  may need bespoke handling beyond the mechanical passes.
- Always **re-gate**; a green report from this tool is a claim, the gate is the
  proof.
