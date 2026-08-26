# TSCG — Test HandOver (project bootstrap smoke-test)

> Paste this as the **first message** of a fresh TSCG project (e.g. "TSCG (test)")
> to verify the project is correctly bootstrapped. Same two rules as any HandOver:
> load skills **by name**, and carry **no authoritative content** — read every fact
> from HEAD or from the two resident corpus files, never from memory.

---

## 1. Load first — by name

- **`head-over-memory`** — authority discipline (verify at source; never recite a
  verifiable fact from memory or corpus).
- **`tscg-ontology-diagnosis-pipeline`** — validation pipeline.

*(Optional, to extend the test to actual modelling: also load `tscg-instance-pipeline`.)*

Naming a skill **is a direct instruction, not a heuristic match.**

---

## 2. The one rule

**HEAD is the only authority** (`github.com/Echopraxium/tscg`). Do not recite
framework facts from memory or corpus — read them from HEAD (raw CDN:
`https://raw.githubusercontent.com/Echopraxium/tscg/main/…`) or from the two
resident corpus files. Durable invariants live in `TSCG_ReferenceCorpus_Bootstrap.md`;
the routing table in `TSCG_ReferenceCorpus.md`.

---

## 3. Smoke-test — run each check and report **PASS / FAIL** with one line of evidence

1. **Resident set present (four files).** Confirm the project knowledge holds all of:
   `TSCG_ReferenceCorpus_Bootstrap.md`, `TSCG_ReferenceCorpus.md`,
   `_00_UserGuide/UserGuide.md`, `docs/reboot-kit/TSCG_FileTree.md`. Exercises are
   **not** resident (they are read from HEAD — check 4). Then, *reading from the
   Bootstrap* (not from memory), state: the REVOI expansion (what R stands for) and the
   three structural operators. → PASS if the four files are present and the values match.
2. **Smart Prompt applied automatically.** Confirm the session loader ran **without a
   paste** — i.e. `TSCG_SmartPrompt.md` is in the project's custom instructions (or,
   as fallback, a resident file). Evidence: the skills below loaded on their own.
   → FAIL if you had to be told to load anything.
3. **Skills loaded by name.** Confirm `head-over-memory` and
   `tscg-ontology-diagnosis-pipeline` actually loaded. State **how** they are
   provisioned in this project (enabled skills vs uploaded `SKILL.md`). → FAIL if
   either did not load — that tells us the provisioning mode is wrong.
4. **HEAD reachable (the lazy-load path).** Fetch
   `https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_GenesisGrammar.jsonld`
   and report its `version`. Then fetch one exercise the same way, e.g.
   `.../main/_00_UserGuide/exercises/LogicGates/LogicGates.md`, and confirm it loads.
   → PASS if both fetch; FAIL if you cannot reach them — that means **web fetch is OFF**,
   so ontologies and exercises can't be read on demand.
5. **Invariant sanity.** From the Bootstrap, confirm two things: `M3_GenesisSpace.jsonld`
   is a **dead vestige** (must not be used) and the operator `⊗` must **never** appear.
   → PASS if both are stated correctly *from the Bootstrap*.

---

## 4. Fresh session state (perishable — supplied here, never from memory)

- **Current HEAD**: `<sha>` — *treat as unverified; confirm with `git show HEAD`.*
- **Active worksite**: `TEST` — bootstrap smoke-test only, no repo changes.
- **Today's goal**: verify this project is correctly bootstrapped (the four §3 checks).
- **Working copy in flight**: none.
- **Gates pending my decision**: none.

---

## 5. Expected outcome

- **All five PASS** → the project is correctly bootstrapped and ready for real work.
- **Check 1 FAIL** → a resident file is missing; re-add it.
- **Check 2 FAIL** → the Smart Prompt isn't applied automatically; put it in the
  project's custom instructions (or keep it as a resident file).
- **Check 3 FAIL** → skills are not provisioned; fix the provisioning mode.
- **Check 4 FAIL** → web fetch is off; either enable it, or plan to paste
  ontology files on demand.
- **Check 5 FAIL** → the Bootstrap in the project is stale; reload the current one.

Report the four results as a short table, then stop. No modelling, no repo changes.
