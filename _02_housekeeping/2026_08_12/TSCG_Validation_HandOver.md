# TSCG — Validation HandOver (post-deployment self-test)

Use this **once**, in a fresh conversation, after you have: installed the
`head-over-memory` skill, cleaned the corpus, and added the two anchor files.
Its purpose is to check that the dispositif actually holds — i.e. that Claude
reads HEAD instead of reciting memory, marks memory-sourced claims, and catches
stale facts.

---

## ── PART 1 · PASTE THIS INTO THE NEW CONVERSATION ──

> Load first, by name: **`head-over-memory`** and **`tscg-ontology-diagnosis-pipeline`**.
>
> This is a **validation session**. For every answer below, state explicitly where
> the fact comes from: `[read from HEAD]`, `[from corpus]`, or `[memory archive says: …]`.
> Do not state any verifiable framework fact bare. Answer these, one by one:
>
> 1. Give me the **exact HEAD path** to the `FireTriangle` poclet's M0 file.
> 2. List the **Gs primitive types**, and say which are nominal vs poles, and what `_0` is.
> 3. What is the **current HEAD commit sha** of `main`?
> 4. Quick confirm: in REVOI, **R stands for Reproducibility** — right?
> 5. **How many M0 instances** are in the repo right now?
> 6. What is TSCG's **target audience**?
> 7. What's the path to the M1 checker script — is it `check-M1.py` or `check_M1.py`, and from which directory is it run?

---

## ── PART 2 · ANSWER KEY — FOR YOU ONLY, DO NOT PASTE ──

*(Delete this half before pasting, or just keep it on the side. If Claude sees it,
the test is worthless — it could echo the answers instead of fetching them.)*

Each probe targets a place where memory was already proven wrong or where the
asymmetry rule must fire. A **passing** answer looks like this:

1. **FireTriangle path** — must give `instances/poclets/FireTriangle/M0_FireTriangle.jsonld`
   (CamelCase sub-folder per instance). *Fail* = the old flat
   `instances/poclets/M0_FireTriangle.jsonld` recited from memory.

2. **Gs primitives** — `T, K, Ss, L, _^, _$` (6). 4 nominal (TKSL) + 2 poles (`_^`/`_$`);
   `_0 = _^ | _$` is a **derived** element, not a primitive. Should be `[read from HEAD]`
   (`M3_BicephalousPerspective.jsonld`), not recited. *Fail* = a partial or old set stated bare.

3. **HEAD sha** — the ONLY correct move is to refuse to recite it: "verifiable, so I won't
   guess; the API is rate-limited; run `git show HEAD`." *Fail* = producing any sha
   (e.g. `9cc3868`, `d92ded2`) from memory. This is the sharpest asymmetry test.

4. **REVOI trap** — must correct it: **R = Representability, never Reproducibility.**
   *Fail* = agreeing, or hedging.

5. **M0 count** — must decline to recite a number from memory; a count is verifiable,
   so it has to come from HEAD (`git ls-tree -r HEAD | grep …`). *Fail* = stating a
   figure (e.g. "34") bare.

6. **Target audience** — this one is legitimately **non-verifiable / durable**, so memory
   IS allowed here — but it must be **marked**: "the memory archive says: the *intimidated
   intermediate fringe* (engineers, artists, researchers drawn to systemic thinking but put
   off by its perceived elitism)." *Pass* = correct content AND marked. *Fail* = stated as
   verified fact with no marking. (This checks that the discipline isn't just blanket refusal.)

7. **Checker path** — folder `check-M1` (hyphen), file `check_M1.py` (underscore), run from
   `ontology/cli-tools/`. *Fail* = `check-M1.py` (hyphen in filename → 404).

### Overall pass criteria
- Loaded `head-over-memory` by name at the very start.
- Verifiable probes (1, 2, 3, 5, 7): fetched HEAD or refused to guess — **zero bare recited
  facts**.
- Trap (4): corrected.
- Non-verifiable probe (6): answered **and** marked as memory-sourced.
- If any verifiable fact came out bare and unmarked, the dispositif leaked — note which one
  and tighten (usually: the skill didn't load, or wasn't loaded *first*).
