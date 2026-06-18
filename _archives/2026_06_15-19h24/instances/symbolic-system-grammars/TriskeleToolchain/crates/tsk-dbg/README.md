# tsk-dbg — TriskeleVM DAP Debugger

**Author**: Echopraxium with the collaboration of Claude AI  
**Version**: 0.1.0  
**Date**: 2026-06-01

---

## Overview

`tsk-dbg` is a **DAP-compatible debugger** for TriskeleVM `.tvmx` binaries.
It connects to VS Code via TCP (port 4711) using the
[Debug Adapter Protocol](https://microsoft.github.io/debug-adapter-protocol/).

### Why tsk-dbg?

Debugging Wolf3D with `O_DUMP_REG` + trace files was painful:
- Regenerate `.tvmx` for each observation point
- Grep thousands of trace lines
- No interactive register inspection

With `tsk-dbg` + VS Code:
- Set breakpoints on **labels** (`ray_loop`, `draw_col`, `dda_step`)
- See all 32 registers in 4 formats: **hex / i64 / fixed 16.16 / f32**
- Step instruction by instruction
- Dump memory interactively (`mem 0x1000 64`)
- Inline disassembly around current PC

---

## Quick Start

### 1. Build

```cmd
cargo build -p tsk-dbg
```

### 2. Generate symbol table

Add `--emit-symbols` to `tsk-asm`:

```cmd
cargo run -p tsk-asm -- src\wolf3d_v2_clean.tasm --emit-symbols -o src\wolf3d_v2_clean.tvmx
```

This produces `wolf3d_v2_clean.sym`:
```
ray_loop 0x00A4
draw_col 0x01B8
sin_table 0x0400
...
```

### 3. Start tsk-dbg

```cmd
cargo run -p tsk-dbg -- src\wolf3d_v2_clean.tvmx --symbols src\wolf3d_v2_clean.sym
```

Output:
```
tsk-dbg: DAP server listening on 127.0.0.1:4711
         In VS Code: F5 → 'TriskeleVM Debug' launch config
```

### 4. Connect VS Code

Copy `vscode_launch.json` to `.vscode/launch.json`, then press **F5**.

VS Code will connect and show the debugger UI.

---

## Features

### Breakpoints

Set breakpoints by **label name** via VS Code's "Add Function Breakpoint" (Shift+F9):

```
ray_loop
draw_col
dda_step
```

Labels are resolved from the `.sym` file. Unresolved labels show a warning in the Breakpoints panel.

### Scopes in VS Code Variables panel

| Scope | Contents |
|---|---|
| **Registers** | R0–R31 + FLAGS. Each register expandable → hex / i64 / fixed 16.16 / f32 |
| **Stack** | Top 16 stack entries with address and value |
| **Disassembly** | Current PC ± 5 instructions with label annotations |

### Debug Console (REPL)

Type expressions in the VS Code Debug Console:

```
R4                    → R4 = 0x000000000000003C  i64=60  fixed=0.000916  f32=...
R12                   → R12 (ray_x, fixed 16.16) full display
pc                    → PC = 0x00A4  ; ray_loop
flags                 → ZF=0 SF=1 OF=0 CF=0
sym draw_col          → draw_col = 0x01B8
mem 0x0400 32         → hex dump of 32 bytes at sin_table
mem 0x1000 64         → dump framebuffer start
```

### Step controls

| Action | Key |
|---|---|
| Step Over (1 instruction) | F10 |
| Step Into (same as step over for VM) | F11 |
| Continue | F5 |
| Pause | Shift+F5 |

---

## Architecture

```
tsk-dbg/
├── src/
│   ├── main.rs        ← CLI: parse args, start DAP server
│   ├── dap/
│   │   ├── mod.rs
│   │   ├── types.rs   ← DAP message structs (Request/Response/Event)
│   │   └── server.rs  ← TCP server, DAP framing (Content-Length headers)
│   ├── session.rs     ← DebugSession: DAP dispatch → VM actions
│   ├── vm_runner.rs   ← VmRunner: VM state + debug hooks (step/break/trace)
│   ├── disasm.rs      ← Inline disassembler (PC ± N instructions)
│   └── symbols.rs     ← SymbolTable: .sym file loader (label → address)
└── vscode_launch.json ← Copy to .vscode/launch.json
```

---

## tsk-asm Changes Required

Add `--emit-symbols` flag to generate the `.sym` file.

In `tsk-asm/src/main.rs`, add:

```rust
#[arg(long, help = "Emit symbol table (.sym file alongside output)")]
emit_symbols: bool,
```

In `tsk-asm/src/assembler.rs`, after the pass-2 encoding loop:

```rust
if args.emit_symbols {
    let sym_path = output_path.with_extension("sym");
    let mut f = std::fs::File::create(&sym_path)?;
    for (label, addr) in &self.symbol_table {
        writeln!(f, "{} 0x{:04X}", label, addr)?;
    }
    log::info!("Symbol table written: {}", sym_path.display());
}
```

---

## Roadmap

| Version | Feature |
|---|---|
| 0.1.0 | DAP server, breakpoints by label, registers/stack/disassembly, REPL |
| 0.2.0 | Watchpoints (memory change detection), conditional breakpoints (`R4 == 60`) |
| 0.3.0 | SDL2 framebuffer preview in debug mode |
| 0.4.0 | Time-travel debugging (E_Snapshot / E_Restore) |

---

## TSCG Grounding

`tsk-dbg` mobilizes the **O_ (Observability)** dimension of the ISA:

| Opcode | Role in debugger |
|---|---|
| `O_Break` (0x85) | Inline breakpoint — triggers DAP `stopped` event |
| `O_DumpReg` (0x80) | Feeds the Registers scope |
| `O_DumpStk` (0x81) | Feeds the Stack scope |
| `O_TraceOn/Off` | Activates instruction trace |
| `O_Watch` (0x86) | Watchpoint on memory address |

The disassembler uses the **K_ (Knowledge)** dimension — reflection on running bytecode.

---

*tsk-dbg v0.1.0 — TriskeleToolchain Debugger*  
*Echopraxium with the collaboration of Claude AI — 2026-06-01*
