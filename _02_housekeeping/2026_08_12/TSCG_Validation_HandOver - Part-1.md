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

