# TSCG User Guide

**Author:** Echopraxium with the collaboration of Claude AI
**Audience:** newcomers — no prior background in Systems Thinking required
**What this guide is:** the complete, hands-on journey of turning an everyday
system into a small TSCG model (a *poclet*) — and, if you want, an interactive
simulation — working together with Claude.

> This is the **human onboarding journey**. It is deliberately non-technical.
> The JSON-LD / SHACL mechanics live in
> `instances/poclets/POCLET_CREATION_GUIDE.md`, and the step-by-step modelling
> logic lives in the `tscg-instance-pipeline` skill. This guide tells *you*
> what to do at each stage and what to expect from Claude.

---

## 1. The kitchen metaphor — who does what

Building a poclet is like running a kitchen. Three roles, one dish:

| Role | Who | Responsibility |
|---|---|---|
| **Head Chef** | **You** | Decides *what* to cook and *whether the dish is good*. Chooses the system, judges every modelling decision, keeps or rejects it. Nothing is served without your say-so. |
| **Commis + Cook + Logistics** | **Claude** | Does the prep and the cooking *under your direction*: proposes ingredients (GenericConcepts), writes the recipe (the M0 ontology), plates it (the simulation), and handles the dishes (files, validation, versions). |
| **The Kitchen** | **TSCG** | The equipment and the pantry: the four ontology layers (M3 → M2 → M1 → M0) and the reusable building blocks you cook with. |

The single most important habit: **you pilot, Claude cooks.** Claude will
propose, draft, and explain — but it can be wrong, and it never decides the
*meaning* of your model. When a choice feels off, push back and ask why.

---

## 2. One-time setup

You do this once. After that, every new exercise starts at Section 3.

### 2.1 Install the TSCG repository locally

You need [Git](https://git-scm.com/downloads) installed. Then:

```bash
git clone https://github.com/Echopraxium/tscg.git
cd tscg
```

This gives you the whole kitchen on your machine: the ontologies under
`ontology/`, existing poclets under `instances/poclets/`, and the tools under
`cli_tools/`. You will keep this folder; it is where your finished poclets go.

### 2.2 Open a Claude AI **Pro** account

The workflow relies on **Claude Projects** (persistent project knowledge, custom
instructions, and Claude's memory), which require a paid plan. At the time of
writing, **Claude Pro** is the practical minimum and there is no free
equivalent. Sign up at [claude.ai](https://claude.ai).

> Honest note: this is a real cost. It is the one prerequisite you cannot work
> around today. Everything else in this guide is free and open-source.

### 2.3 Create and configure the **"TSCG Cyclop v0"** project

In your Claude account, create a new **Project** named **`TSCG Cyclop v0`**.
This is your dedicated TSCG kitchen inside Claude — it keeps every session
oriented and stops Claude from drifting or inventing framework facts.

Set it up **once** so that afterwards you never have to load anything into a
conversation. The exact set is defined in `TSCG_ReferenceCorpus_Bootstrap.md` under
*"Minimal project corpus"* (the single source of truth). In short:

1. **Project custom instructions** — this is the project's **instructions** field (the
   standing prompt applied to *every* conversation), **not** the short "description"
   label. Paste this directive into it:

   ```
   This is a TSCG project. At the very start of every conversation, before anything else:
   1. Fetch https://raw.githubusercontent.com/Echopraxium/tscg/main/docs/reboot-kit/TSCG_SmartPrompt.md
      and follow it as your session loader (it names the skills to load and the corpus to read).
   2. Governing rule: HEAD is the only authority — read framework facts from HEAD or the
      resident corpus, never from memory.
   ```

   This keeps the field small and the Smart Prompt always current, and it applies
   automatically — no per-session paste. (Fetching the prompt is not the same as
   applying it; this directive is what makes Claude adopt it.)
2. **Project Knowledge (resident, loaded once — four files):** `TSCG_ReferenceCorpus_Bootstrap.md`,
   `TSCG_ReferenceCorpus.md`, `_00_UserGuide/UserGuide.md`, `docs/reboot-kit/TSCG_FileTree.md`.
3. **Skills (provisioned once).** Four skills drive the workflow: `head-over-memory`
   and `tscg-ontology-diagnosis-pipeline` (always), plus `tscg-instance-pipeline`
   (to model) and `tscg-create-instance-simulation` (to simulate). They live in the
   repo at `.claude/skills/<name>/SKILL.md`. Provision them in your project **either**
   as enabled project skills, **or** — if your setup has no skills panel — by uploading
   each `SKILL.md` into Project Knowledge. Either way, the Smart Prompt loads them by
   name; if they aren't present, its first step fails.
4. **Enable web fetch** — the one unavoidable dependency: the **exercises** and the
   live ontologies (M3/M2/M1/M0) are read from HEAD on demand (the File Tree gives the
   path), so web fetch lets Claude pull them itself — still with zero action from you,
   and without bulk-loading 15 exercise files into the project.

(The project owner refreshes the one drift-prone resident copy — the File Tree —
after structural changes. Never your concern as a user.)

> **Why "Cyclop"?** TSCG reads a system through *two eyes* (Territory + Map).
> A fresh project with no context is one-eyed — it needs the corpus to gain
> depth perception. Loading the corpus is what turns Cyclop into a proper
> stereoscopic reader.

### 2.4 Verify the setup before your first task

Two things can silently be wrong: the **skills** may not be provisioned, and **web
fetch** may be off (so Claude can't read exercises or ontologies from HEAD). Check
both in one go: open a conversation and paste **`TSCG_Test_HandOver.md`** (in the
repo root). Claude runs five checks and returns a PASS/FAIL table —

- **check 3** confirms the four skills loaded (and tells you *how* they're provisioned);
- **check 4** confirms Claude can fetch from HEAD (i.e. web fetch is on).

If either fails, fix it before proceeding — the table says exactly what to do. For a
quick manual web-fetch test without the HandOver, just ask: *"Fetch
`https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_GenesisGrammar.jsonld`
and tell me its version."* If Claude can't reach it, web fetch is off.

You are now ready to cook.

---

## 3. The per-exercise journey

Everything below repeats for each system you model. It maps onto the four-step
`tscg-instance-pipeline` — **Proposition → Analysis → Modeling → Simulation** —
with **you as Head Chef** at every decision point.

### Step 1 — Choose an exercise

Pick one from `_00_UserGuide/exercises/` (each has its own folder). The catalogue
is grouped by theme — the **Starter** rows are the gentlest first dishes:

| Exercise | Domain | Level | What it teaches |
|---|---|---|---|
| **Logic Gates** | Digital electronics | Starter | Tiny, exact — a truth table you can verify by hand (Information-dominant) |
| **Bubble Sort** | Computer science | Starter | A process converging to a "sorted" attractor |
| **Maze Generator & Solver** | Graph algorithms | Intermediate | Build a structure, then search it — Map/Territory (path vs space) |
| **Rubik's Cube** | Combinatorics / puzzles | Intermediate | A huge state space, one solved attractor — natural **3D** |
| **Capacitor** | Electronics | Starter | Charge/discharge relaxation to equilibrium |
| **Osmosis / Reverse Osmosis** | Chemistry / Biology | Intermediate | A gradient, a flow, and a driven reversal |
| **Dice Simulator** | Probability | Starter | Convergence to a distribution (LLN / CLT) |
| **Game of Life** | Cellular automata | Starter | Emergence: global patterns from simple local rules |
| **Truchet Patterns** | Generative art / tiling | Starter | Emergence again — a generative (non-convergent) poclet |
| **Fractal Explorer** | Mathematics | Intermediate | Iteration, self-similarity; a finite Map of an infinite Territory |
| **QR / DataMatrix Decoding** | Coding theory | Intermediate | Redundancy and error-correction as robustness |
| **Image Processing** | Image processing | Starter | Successive lossy reductions (colour → gray → ANSI) |
| **Mini Alchemy** | Game / crafting | Starter | Combination and reachable-set closure |
| **Stroboscopic Yin-Yang** ★ | Perception | Intermediate | Map vs Territory made visible — a *worked* example (sample run in `workflow_run_sample/`) |

> ★ **Stroboscopic Yin-Yang** is the one exercise shipped *with* a sample run: it exists
> to **illustrate the workflow end to end**. Its `workflow_run_sample/` folder holds
> *one* example resolution — a spoiler, and **not** a definitive answer (in TSCG another
> modeller could legitimately model it differently). Do the exercise first if you want
> the practice.

> Only three of these land in an existing M1 domain (`electronics`,
> `chemistry`/`biology`); the rest have **no domain yet** — so they let you meet
> the "is there a domain? / is this an M2 candidate?" question for real. Several
> also **cluster** (algorithms: Bubble Sort · Rubik's Cube · Maze; emergence:
> Game of Life · Truchet), which is useful evidence when weighing a new concept.

Or bring **your own** system. A good first poclet is **minimal** (3–5 essential
parts) and **complete** (it clearly has all five ASFID facets: an Attractor it
tends toward, a Structure, a Flow, Information, and Dynamics).

### Step 2 — Propose it, with documentation

Start a session in `TSCG Cyclop v0` and describe the system in a few sentences,
attaching whatever reference material you have (a Wikipedia page, a course note,
a datasheet — the exercise folders already include a source). Then ask the
open question the pipeline expects:

> *"Here is [system] with this documentation — what do you think?"*

Claude answers with a **feasibility diagnostic**: which ASFID facets are active,
which GenericConcepts look relevant, and a verdict — **valid instance**, **too
trivial**, or **too complex**. If it's borderline, Claude proposes a reduced
scope (e.g. "a single logic gate" instead of "a whole CPU"). **You decide**
whether to proceed.

### Step 3 — Ask for the analysis (the key thinking step)

Now the real work. Ask Claude to analyse the fit, and steer it toward two
questions in particular:

- **Are the existing M2 GenericConcepts enough**, or does this system reveal a
  *new pattern* — an **M2 candidate**? (A candidate is a genuine contribution to
  the framework, not a failure. It must later prove itself across several
  unrelated domains before it's admitted.)
- **Is there already an M1 domain** for this system? Extensions exist for
  *biology, chemistry, economics, education, electronics, energy_generators,
  geology, music, mythology, optics, photography, physics, business_modeling,
  systemic_modeling*. If yours isn't there (as with Bubble Sort or Rubik's
  Cube), that's a finding — you may be opening a new domain.

Claude produces an `analysis.md`. **Read it critically.** Ask "why this concept
and not that one?" until the reasoning is clear to you. This is where you learn
the framework, and where you catch mistakes.

### Step 4 — Delegate the modelling, and pilot it

When the analysis is settled, hand the cooking to Claude:

> *"Model this as an M0 instance — the `M0_<Name>.jsonld` and its
> `M0_<Name>_README.md`."*

Claude writes the ontology and its documentation following the FireTriangle
reference pattern. Your job is to **pilot**: validate each choice, ask for
explanations, and reject anything that doesn't match the system as *you*
understand it. Two ground rules protect you here:

- **The model must pass SHACL validation** before anything else happens. Claude
  runs `python ontology/TSCG_Grammar/validate_m0_instance.py <path>` and fixes
  violations until it reports *Conforms: True*. A model that doesn't validate is
  not done.
- **Semantic decisions are yours.** Claude proposes the *structure*; you own the
  *meaning*.

### Step 5 — Optionally, craft a simulation or a tool

If you want to *see* the system move, ask Claude to build one:

- **A serverless HTML simulation** — a single `.html` file that opens in any
  browser. Start from the template at `instances/poclets/_00_template/`
  (`M0_Template.html` + the `src/tscg-shell.*` shell). Use **p5.js** when the
  system is best shown in **2D** (a truth table, a charge curve, sorting bars,
  a membrane) and **BabylonJS** when it wants **3D** (a Rubik's Cube).
- **A utility (a TscgTool)** — a small **Python** script or an **ElectronJS**
  app, when the deliverable is a tool rather than a single visual.

Simulations are built iteratively — one round for interactivity, one for
teaching clarity, one for polish. You decide how many rounds and what matters.

### Step 6 — If it's good, offer it to the public repository

When you're happy with the dish, you can propose it for the public TSCG
repository. The friendly way in is to **open an issue** on
[github.com/Echopraxium/tscg](https://github.com/Echopraxium/tscg/issues)
describing your poclet and attaching your files, rather than pushing directly.
That lets a maintainer review it and place it correctly. Contributions —
especially new domains or well-argued M2 candidates — are the whole point of the
game.

> **Publish poclets, not exercise answers.** If you solved one of the catalogue
> exercises, **don't** publish your model beside its statement — that hands everyone an
> answer and spoils the exercise. When a catalogue exercise ships an illustrative run, it
> goes in a spoiler-marked `workflow_run_sample/` folder, framed as *one* example
> resolution rather than *the* solution (TSCG has no single correct model — see
> *Stroboscopic Yin-Yang* for the pattern). Only **out-of-catalogue** poclets — systems
> you modelled that aren't in the exercise list — are published as normal contributions.

### See it in action

A full run of this workflow on the *Stroboscopic Yin-Yang* exercise — Claude loading
itself from HEAD, then Proposition → Analysis → Modeling → Simulation — is shared here:
**{{SHARE_URL}}**. Treat it as an illustrative snapshot (dated, may lag the current
framework), not as authoritative reference — to *reproduce* it you still follow the
project setup in section 2.


---

## 4. Quick reference — your checklist

1. **Setup (once):** clone the repo · get Claude Pro · create & load `TSCG Cyclop v0`.
2. **Propose** a system with documentation → get a feasibility verdict.
3. **Analyse** → M2 sufficient or a candidate? existing M1 domain or a new one?
4. **Model** M0 + README → *pilot every choice* → **must pass SHACL**.
5. **Simulate** (optional) → HTML (p5.js 2D / BabylonJS 3D) or a Python/Electron tool.
6. **Publish** (optional) → open an issue on the public repo.

## 5. Where to look next

- `instances/poclets/POCLET_CREATION_GUIDE.md` — the technical how-to (JSON-LD, SHACL, templates).
- `instances/poclets/FireTriangle/` — the canonical reference poclet.
- `instances/poclets/_00_template/` — the simulation starter shell.
- `docs/reboot-kit/TSCG_ReferenceCorpus.md` — where the authoritative files live.

---

*Remember: you pilot, Claude cooks, TSCG is the kitchen. Nothing is served
without the Head Chef's approval.*
