# Cleanup chantier — 2026-09-23

**Author**: Echopraxium with the collaboration of Claude AI
**Nature**: a running list of low-priority *structural* debts. None is urgent or
blocking; they are gathered here so they are not lost. Resolve them in a dedicated
tidy-up worksite, not opportunistically. Anything touching ontology tooling is
governed by the `tscg-ontology-diagnosis-pipeline` skill.

---

## 1. Tooling-directory duplication (the reason this note exists)

There are **two tool directories**, distinguished today only by their separator:

- `cli_tools/` — **root, underscore** — root-level tools (linter, migration,
  reasoning tests, the simulation-gallery generator, the Compendium build).
  Referenced by **~25** files on HEAD.
- `ontology/cli-tools/` — **hyphen** — the gate / checker tools
  (`run_all_layers.py`, `check-M1`, `check-M0`, golden values, metrics).
  Referenced by **~49** files on HEAD.

The separator currently acts as a *useful signal* that tells the two apart, but
the near-identical name is a standing source of confusion (and a documented
404-trap in `TSCG_ReferenceCorpus.md`).

**Do NOT** rename `cli_tools` → `cli-tools`: that removes the distinguishing
signal and creates two `cli-tools` dirs at different depths — *worse* confusion,
not better, and it breaks ~25 path references at once.

The real fix is *semantic*, not typographic — pick one when ready:
- **merge** the two into a single tools tree, or
- **rename by role**, e.g. `ontology/cli-tools/` → `ontology/gates/` (these are
  the validation/gate tools), which removes the collision by meaning.

Either is a real refactor (path references, `.bat` launchers, READMEs, corpus
docs, and the new `pages.yml`), so it belongs in its own worksite.

## 2. `m1core` → `m1` vestige

`m1core:` is a dead alias prefix: it resolves to the **same URL** as `m1:`
(`…/ontology/M1_CoreConcepts.jsonld#`), and the two are often co-defined. Safe,
mechanical rename (no IRI changes): rewrite `m1core:` → `m1:` and drop the
`m1core` `@context` definition. Scope: ~32 `.jsonld` (excluding backups) + a
secondary sweep of ~30 prose/tooling mentions. Fits `migrate_properties.py`.

## 3. `ORIVE` → `REVOI` in `poclet_terminology.md`

`docs/reboot-kit/poclet_terminology.md` still uses the old **ORIVE** acronym; the
current invariant is **REVOI** (R = Representability, never Reproducibility).
Reconcile the source doc so the durable corpus matches HEAD.

---

*Reminder, not an execution plan. Open a dedicated tidy-up worksite (WS-n) when
you choose to act; keep the deployment and modelling work uncoupled from it.*
