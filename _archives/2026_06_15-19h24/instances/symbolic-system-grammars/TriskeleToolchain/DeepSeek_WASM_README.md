# TriskeleVM – A Structural Virtual Machine

**TriskeleVM** is a 256‑opcode virtual machine designed around the **TSCG (Territory‑Stereopsis‑Map) Structural Grammar**.  
It provides a regular, monoid‑grounded instruction set suitable for systems programming, retro game engines (e.g., Wolfenstein 3D), and embedded scripting.

This repository contains:

- `triskele-common` – ISA definitions (categories, opcodes, base‑16 Triskele literals)
- `triskele-vm` – VM core (CPU, memory, decoder, execution loop)
- `tsk-asm` – One‑pass assembler for `.tasm` source files
- `triskele-wasm` – (planned) WebAssembly target for running the VM in a browser

## Features

- **256 opcodes** – fully covered 8‑bit encoding  
- **16 semantic categories** – grouped by the three TSCG monoids (`Gt` ×, `Gm` +, `Gs` |)  
- **Symmetrical life‑cycle operators** – `_^_` (positive pole) / `_$_` (negative pole) for resource management  
- **Rich set of primitives** – stack, heap, control flow, bitwise, arithmetic, conversions, reflection, events, coroutines, temporal operations, FFI, and debugging  
- **One‑pass assembler** – with label fixup, multiple sections (`.code`, `.rodata`, `.data`, `.bss`), and expressive pseudo‑instructions  
- **Native execution** – works as a standalone VM on any platform supported by Rust  
- **WebAssembly ready** – can be compiled to WASM and run inside a browser (see roadmap)

## ISA Overview

The instruction set is organised into 16 categories, each occupying a 4‑bit high nibble (0x0 … 0xF).  
Every category answers a specific M3 grammar question and belongs to one of the three monoids:

| Category | Name               | Monoid | Question                                    |
|----------|--------------------|--------|---------------------------------------------|
| 0x0      | `A_` – Attractor   | Gt     | *Where do data converge?*                   |
| 0x1      | `St_` – Structure  | Gt     | *How organised?*                            |
| 0x2      | `F_` – Flow        | Gt     | *How does execution flow?*                  |
| 0x3      | `It_` – Information| Gt     | *What is the info state?*                   |
| 0x4      | `D_` – Dynamics    | Gt     | *What modifies data?*                       |
| 0x5      | `R_` – Representability| Gm | *Encodable in another form?*              |
| 0x6      | `E_` – Evolvability| Gm     | *Generates novelty?*                        |
| 0x7      | `V_` – Verifiability| Gm    | *Verifiable / falsifiable?*                 |
| 0x8      | `O_` – Observability| Gm    | *Measurable internally?*                    |
| 0x9      | `Im_` – Interoperability| Gm | *Interfaceable?*                         |
| 0xA      | `T_` – Temporality | Gs     | *When?*                                     |
| 0xB      | `_^_` – Positive Pole | Gs   | *Onset / activation*                        |
| 0xC      | `_$_` – Negative Pole | Gs   | *Terminus / dissolution*                    |
| 0xD      | `K_` – Knowledge   | Gs     | *What is known?*                            |
| 0xE      | `Ss_` – Symbol     | Gs     | *What is the sign?*                         |
| 0xF      | `L_` – Localizability| Gs   | *Converging toward?*                        |

Instructions are encoded in 32‑bit words with three types:  

- **Type R** – `[opcode:8] [dst:5] [src1:5] [src2:5] [flags:9]`  
- **Type I** – `[opcode:8] [dst:5] [imm:19]`  (signed immediate)  
- **Type J** – `[opcode:8] [offset:24]`  (signed PC‑relative jump)

A complete reference of all 256 opcodes can be found in `triskele-common/src/isa.rs`.

## Assembler – `tsk-asm`

The assembler translates `.tasm` source files into Triskele object files (`.tobj`), libraries (`.tvml`), or executables (`.tvmx`).

### Example Source

```asm
.module  hello
.type    executable
.section .code
.entry   main

main:
    PRINT "Hello, World!\n"
    D_MOV_I  R0, 0
    F_HALT
Directives
Directive	Description
.module <name>	Set module name
.type <kind>	executable / library / object / archive
.section <name>	Switch to .code, .rodata, .data, .bss
.byte <expr>	Emit a single byte
.word <expr>	Emit 16‑bit little‑endian word
.dword <expr>	Emit 32‑bit word
.qword <expr>	Emit 64‑bit word
.string "..."	Emit null‑terminated string
.ascii "..."	Emit raw bytes without null terminator
.align <n>	Pad current section to next multiple of n
.entry <label>	Set the program entry point (must be in .code)
#define ...	Simple preprocessor constant
Pseudo‑instructions
The assembler recognises several high‑level mnemonics that expand to efficient sequences:

PRINT "string" – places the string in .rodata and emits a L_LEA + O_LOG_S pair.

D_MUL Rdst, Ra, Rb – maps to fixed‑point 16.16 multiplication (R_FIXMUL).

D_IMUL Rdst, Ra, Rb – integer multiply (D_Mul).

D_AND, D_OR, D_XOR – bitwise operations (become D_And, D_Or, D_Xor).

D_SHL Rdst, Rsrc, imm / D_SHR – shift left/right with immediate.

L_LEA Rdst, label – load address of a label (supports both code and rodata).

Building an Executable
bash
tsk-asm program.tasm -o program.tvmx
If the output file is omitted, the extension is auto‑deduced from the .type directive (.tvmx for executable, .tvml for library, .tobj for object).

To see the symbol table (label → VM address), pass --emit-symbols.

Running the VM (Native)
rust
use triskele_common::tvm::TvmFile;
use triskele_vm::{Cpu, memory::Memory};

let tvm = TvmFile::load_from_file("program.tvmx")?;
let mut mem = Memory::new(0x1000, 16 * 1024 * 1024);
// ... load sections into memory ...
let mut cpu = Cpu::new(mem, entry_address, NativeHost);
let exit_code = cpu.run()?;
The VM implements full memory protection, a 32‑register file (R0–R31, plus FP, SP, LR, PC aliases), and a configurable heap.

WebAssembly Support (Roadmap)
TriskeleVM can be compiled to WebAssembly and run inside a browser. The plan includes:

Abstract host interface (HostInterface trait) to separate platform‑dependent operations.

A WasmHost implementation that calls into JavaScript (console, canvas, keyboard, timers).

A non‑blocking step‑by‑step execution model (step_frame) to keep the browser responsive.

Optional support for threaded coroutines via JavaScript’s requestAnimationFrame and setTimeout.

Once the triskele-wasm crate is complete, you will be able to instantiate the VM in a few lines of JavaScript and run existing .tvmx executables directly.

Building from Source
bash
git clone https://github.com/yourname/triskelevm
cd triskelevm
cargo build --release
The assembler binary will be placed in target/release/tsk-asm.

Testing
A comprehensive test suite is included. Run:

bash
cargo test --workspace
The tests verify opcode encoding, label resolution, and execute small programs inside the VM.

License & Authors
Author: Echopraxium, with the collaboration of Claude AI

Version: 0.3.0 (ISA 0.2.0 / assembler 0.3.0)

License: (specify your license, e.g., MIT or Apache 2.0)

Further Reading
triskele-common/src/isa.rs – full opcode list and category definitions

tsk-asm/src/assembler.rs – assembler logic and relocation

triskele-vm/src/cpu.rs – execution engine

TriskeleVM – where structure meets execution.

text

Ce README couvre l’essentiel : présentation du projet, description de l’ISA, utilisation de l’assembleur, exemples, compilation, tests et perspectives WASM. N’hésite pas à ajuster les détails de licence et les liens.