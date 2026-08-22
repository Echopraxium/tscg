# `modernize_m0.py` — M0 instance modernizer (check-M0, Path B)

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
lacked `M0_Common`, and retired `@context` aliases (`m1core:`, `m1chem:`, `sm:`,
`*_score`) lingered. Fixing these by hand, instance by instance, is slow and
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
   - `m0:` → `https://…/ontology/M0_Common.jsonld#` (fixes C02).
   - adds `m0.<camelInstance>:` → the instance file's URL (fixes C03). The
     camel form matches the gate's own `_camel()` (e.g. `BloodPressureControl`
     → `m0.bloodPressureControl`, `VCO` → `m0.vCO`).
   - **migrates or deletes** retired aliases (fixes C07/C08). Crucially it
     *migrates* an alias that is still used in the body rather than deleting it
     (deleting a used alias would leave unresolved, non-absolute IRIs and fail
     C15): `m1core:` → `m1:`, and any `m1<domain>:` short alias → `m1.ext:<domain>:`
     (e.g. `m1phys:` → `m1.ext:physics:`). Unused aliases (and `sm:`, `*_score`)
     are dropped.
   - forces `m1`/`m2`/`m3` prefixes to absolute HTTPS if they were relative.

2. **`owl:imports`** — rewritten to absolute URLs and `M0_Common.jsonld` added
   if missing (fixes C09).

3. **Path B reclassification** — every `m0:X` token (property keys *and* `@id`
   values, including the double-colon `m0:<Inst>:Y` form) is kept under `m0:`
   if `X`'s first segment is in the whitelist, otherwise rewritten to
   `m0.<inst>:X`.

4. **Tensor reform hooks (guarded, no-op when absent)** — renames the retired
   formula property `m0:tensorFormula` / `m0:hasStructuralGrammarFormula` to the
   canonical `m2:hasStructuralGrammarFormula`. *(The `⊗`→`×` reform of formula
   **values** is not yet wired in here — see Limitations.)*

5. **ORIVE hygiene** — replaces the vestige acronym `ORIVE` with `REVOI` in
   prose values (the gate tolerates it inside a string, but the notation rule
   forbids it).

6. **Reports, never guesses** — prints a JSON summary: how many properties were
   reclassified, which aliases were migrated, residual `orive` count, and a
   `semantic_gaps` list flagging anything it will **not** fill in
   (`m1:domain`, `m3:ontologyType`).

## Casing guardrail (folder vs file)

The gate derives an instance's name from its **file** stem (`M0_<name>` →
`<name>`), so a file whose casing differs from its folder — e.g. folder `Vco`
with file `M0_VCO.jsonld` — resolves to `VCO` on case-sensitive Linux/CI but
`Vco` on case-insensitive Windows. The two disagree on the expected
`m0.<inst>:` alias, so the instance passes on one OS and fails on the other.

To prevent this, the tool takes the instance identity from the **folder** (the
stable identity per the repo layout `instances/<Cat>/<Instance>/M0_<Instance>.jsonld`)
and computes the alias from it. If the file name is not the canonical
`M0_<folder>.jsonld`, the report includes a **`CASING_WARNING`** with the exact
case-safe two-step `git mv` to rename the file. Rename the file, then re-gate —
the alias will match on every platform.

## What it does NOT do (by design)

- It never invents **semantic** content. Missing `m1:domain` or
  `m3:ontologyType`, and the **content** of formulas, are the Head Chef's
  decisions — the tool flags them, you supply them.
- It does not flatten nested `asfidScores`/`revoiScores` (none of the piloted
  instances had them; add that step if you meet one, per the FireTriangle pass).

## Usage

Run from **anywhere** (the schema is resolved relative to the script), passing
the instance path:

```bash
python ontology/cli-tools/modernize_m0.py instances/poclets/PhaseTransition/M0_PhaseTransition.jsonld
```

It **rewrites the file in place**, then prints its report. Always re-gate after:

```bash
python ontology/cli-tools/check-M0/check_m0_instances.py --instance PhaseTransition
python ontology/TSCG_InstanceGrammar/validate_m0_instance.py instances/poclets/PhaseTransition/M0_PhaseTransition.jsonld
```

Both must be green (C01–C15 OK / `VALIDATION PASSED`). Then `git add` the single
file by path and commit.

> **In place** means: work on a clean git tree so `git diff` shows exactly what
> changed, and you can `git checkout --` to revert if a report flags something
> you want to review first.

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
- Always **re-gate**; a green report from this tool is a claim, the gate is the
  proof.
