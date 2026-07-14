# CLAUDE.md — TriskeleToolchain

This file provides guidance to Claude Code when working in the TriskeleToolchain
workspace. It **complements** the repository-root `CLAUDE.md` (tscg conventions);
in case of conflict on toolchain matters, this file wins.

Workspace path (Windows):
`E:\_00_Michel\_00_Lab\_00_GitHub\tscg\instances\symbolic-system-grammars\TriskeleToolchain\`

## Project Overview

**TriskeleToolchain** is a Rust toolchain and virtual machine whose ISA is grounded
in the TSCG M3 basis (16 opcode categories = Base16 Triskele: `A_ St_ F_ It_ D_ R_
E_ V_ O_ Im_ T_ _^_ _$_ K_ Ss_ L_`). Components:

| Crate | Role |
|-------|------|
| `triskele-common` | Shared types, ISA definitions, `.tvm`/`.tvmx` formats |
| `triskele-vm` | Register-based VM interpreter (32 × 64-bit registers) |
| `tsk-cc` | C compiler front-end (parser + codegen) |
| `tsk-asm` / `tsk-dis` | Assembler / disassembler |
| `tsk-link` | Linker |
| `tsk-build` | Build orchestrator |

Current version line: **v0.3.14+** (WASM porting in progress toward Z-Machine support).

**MANDATORY READ before any opcode-related work:**
`TriskeleVM_ISA_Reference_v020.md` (in this directory).
Key rule: indexed notation `St_ It_ Ss_ Im_` — NEVER `S_` or `I_`.

## Common Commands

```bash
# Full validation suite — the canonical acceptance gate
python run_all_tests.py --clean

# Build the workspace
cargo build            # debug
cargo build --release  # release (lto, panic=abort)

# Run a single pipeline manually
cargo run -p tsk-build -- <program.c>

# VM execution trace (primary diagnostic for runtime faults)
cargo run -p triskele-vm -- <program.tvmx> --trace

# WASM dev server (COOP/COEP headers required for SharedArrayBuffer)
python server.py       # then open the hub index.html
```

## Validation Discipline: SEPTUPLE VALIDATION

The acceptance gate is the seven-program test suite. Reference values (v0.3.8,
2026-06-09) — any regression against these is a blocker:

| Program | Expected result |
|---------|-----------------|
| test_main | 31 |
| wolf3d | 15 |
| test_patterns | 15 |
| test_select | 9 |
| doom_fixed | 127 |
| doom_alloc | 255 |
| doom_zzone | 255 |

Rules:
- Run `python run_all_tests.py --clean` after **every** change to tsk-cc, tsk-link,
  or triskele-vm. Never declare a fix validated without a full clean run.
- Progress is tracked as a **milestone ladder** (binary checkpoints M0→M7 in
  `PORTING_PROGRESS.md`), never as percentage estimates.
- **Honest negative results are preferred over enthusiastic validation.** If a fix
  is partial or a test regresses, say so explicitly and first.

## Architecture Decisions (ADRs)

ADRs live in this directory (`ADR-WASM-001/002/003`). Read them before touching
the WASM layer. Key locked decisions:

- **Worker + Atomics over async/Closure** for interactive stdin: single VM Web
  Worker, `SharedArrayBuffer` + `Atomics.wait` for blocking `fgets`/`getchar`
  semantics. This eliminates recurring wasm-bindgen closure lifetime debt.
  Do not reintroduce async-based input paths.
- `postMessage` is the default inter-worker channel; Monitoring/Debug workers
  are deferred (single VM worker for now).
- **`HostIo` HAL trait** replaces `Box<dyn Write>` for all host I/O. New syscalls
  go through `HostIo` (`fgets`, `getchar`, ...), with native and `SabHost` (WASM)
  implementations.
- Technical debt awareness is an explicit design criterion: when proposing an
  implementation, state the debt it creates or retires.

## WASM / Z-Machine Roadmap

Milestone ladder M0→M7 in `PORTING_PROGRESS.md`. Status as of 2026-07-02:
- M0–M2b validated.
- **M2c (interactive `fgets` in browser) blocked** on tsk-cc alloca fix
  confirmation.
- Open issue: `F_TRAP: exception code 255` appearing post-codegen-fix.
  Next diagnostic step: run with `--trace`.
- M3 target: **Z-Machine v3** running Colossal Cave Adventure (Graham Nelson
  port, public domain). Infocom/Zork titles are under copyright — never bundle
  or fetch them.

Next priorities (from v0.3.8 plan):
1. Complete z_zone.c (DoomGeneric)
2. tsk-libc `malloc` with free-list
3. Spill handling on `Z_ClearZone`

## Known tsk-cc Patches (do not regress)

- `parser.rs` (0.3.1): missing `nonnull` in `skip_flags` — fixed.
- `codegen.rs` (0.3.4): dead-alloca eliminator for `-O0` return-value slot — fixed;
  suspected interaction with the trap-255 issue above.

## Coding Conventions

- All source, comments, commit messages, ADRs, reports: **English**.
  (Conversation with Michel is in French.)
- Prefer **surgical edits** (str_replace-style minimal diffs) over file rewrites.
- Error propagation: `anyhow::Result` at boundaries, `thiserror` enums in
  `triskele-common` (`VmError`); traps surface as `F_TRAP: exception code N`.
- Mark all `unsafe` blocks explicitly and justify them (SDL2 FFI, libloading,
  SharedArrayBuffer views).
- `_^_` / `_$_` symmetry: any creation opcode/API must have its destruction dual.
- Versioning: bump the patch component per validated fix; record it in the
  affected crate and in `PORTING_PROGRESS.md`.
- Deliverables for chat round-trips (if any) are `.zip` files matching the exact
  workspace arborescence — but under Claude Code, edit files in place instead.

## Workflow Expectations

1. **Validate the conceptual approach with Michel before writing code** for any
   architectural change (new HAL surface, worker topology, ISA extension).
   Bug fixes within locked architecture may proceed directly.
2. For debugging sessions: reproduce first (`run_all_tests.py --clean` or the
   failing program with `--trace`), state the hypothesis, apply the minimal
   patch, re-run the full suite.
3. When a session ends mid-investigation, write the current hypothesis and next
   diagnostic step into `PORTING_PROGRESS.md` so the next session resumes cleanly.

## Related Skills (if available)

- `tscg-rust-vm` — implementation patterns (workspace layout, ISA encoding,
  arena allocator, fixed-point 16.16, FFI).
- `tscg-triskelevm-debug` — diagnostic pipeline for failed runs
  (`pipeline_report.txt`, `.tvmx`, `.ll` analysis).

Ontology work (JSON-LD, SHACL, M0–M3) is **out of scope** for this workspace —
follow the repository-root `CLAUDE.md` and its dedicated skills instead.

---

**Version**: 1.0.0 (initial, aligned with toolchain v0.3.14)
**Last updated**: July 2026
**Maintained by**: Echopraxium with the collaboration of Claude AI
