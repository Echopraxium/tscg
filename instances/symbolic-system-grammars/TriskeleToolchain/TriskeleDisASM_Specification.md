# tsk-dis — Triskele Disassembler Specification

**Author**: Echopraxium with the collaboration of Claude AI  
**Version**: 0.1.0  
**Date**: 2026-05-30  
**Status**: Draft — TriskeleToolchain  
**Input extensions**: `.tobj`, `.tvx`, `.tvl`, `.tva`  
**Output**: stdout or `.tsk.dis` listing file

---

## 1. Overview

`tsk-dis` is the disassembler for TriskeleVM. It translates binary `.tobj` /
`.tvx` / `.tvl` files back into human-readable Triskele assembly, enriched
with Base16 Triskele semantic annotations and optional TSCG M2/M3 metadata.

Design principles:
- **Semantic transparency** — every opcode displayed with its M3 category
- **Base16 Triskele** — numeric values shown as M3 primitive sequences
- **TSCG-aware** — reads `.tscg` section and annotates output
- **Multiple output modes** — from minimal to fully annotated
- **Round-trip fidelity** — output re-assemblable by `tsk-asm` (best effort)

---

## 2. Output Modes

### 2.1 `--mode minimal`

Bare mnemonics, no annotations. Closest to re-assemblable source.

```asm
main:
    D_MOV_I   R0, 0x00000020
    Im_FFI_CALL SDL_Init
    V_CMP     R0, 0
    A_JL      L_0004
    A_CALL    game_loop
    Im_FFI_CALL SDL_Quit
    D_MOV_I   R0, 0
    Im_EXIT
L_0004:
    D_MOV_I   R0, 1
    Im_EXIT
```

### 2.2 `--mode standard` (default)

Addresses, hex encoding, M3 category tag, mnemonic, operands.

```asm
; ── Section .code ─────────────────────────────────────────────
; Offset   Encoding    M3   Mnemonic      Operands
; ──────── ─────────── ──── ────────────  ───────────────────────
main:
00000000  D1 00 0020   D    D_MOV_I       R0, 0x00000020
00000004  91 08 ????   Im   Im_FFI_CALL   SDL_Init
00000008  70 00 0000   V    V_CMP         R0, 0
0000000C  08 ??????    A    A_JL          L_0004
00000010  02 ??????    A    A_CALL        game_loop
00000014  91 08 ????   Im   Im_FFI_CALL   SDL_Quit
00000018  D1 00 0000   D    D_MOV_I       R0, 0
0000001C  9F 00        Im   Im_EXIT
L_0004:
00000020  D1 00 0001   D    D_MOV_I       R0, 1
00000024  9F 00        Im   Im_EXIT
```

### 2.3 `--mode annotated`

Full annotations: Base16 Triskele encoding, M3 semantics, TSCG M2 tags,
symbol names, relocation info.

```asm
; ════════════════════════════════════════════════════════════════
; wolf3d_main.tvx — Disassembly (tsk-dis 0.1.0)
; Date: 2026-05-30
; Format: .tvx executable
; Entry: main @ 0x00000000
; TSCG: SymbolicSystemGrammar — TriskeleToolchain
; ════════════════════════════════════════════════════════════════

; ── Section .code ─────────────────────────────────────────────
; M3 tag: F (Flow) — dominant: computation
; TSCG: m2:Process "main execution"

; ┌─ TSCG block: m2:Attractor "program entry point" ──────────┐
main:                              ; [EXPORT] entry point
00000000  D1 00 20 00   D·_^·F·A   D    D_MOV_I    R0, 0x00000020
          ; Base16: D=0xD _^=0xB F=0x2 → #K_POS_F_A
          ; Value: 32 (SDL_INIT_VIDEO)
          ; Semantic: D(Dynamics) — register initialization

00000004  91 08 00 00   Im·O·A·A   Im   Im_FFI_CALL SDL_Init
          ; Base16: Im=0x9 → Interoperability category
          ; FFI: SDL2::SDL_Init(int) → int
          ; [RELOC R_TSK_FFI → SDL_Init@SDL2]

00000008  70 01 00 00   T·A·A·A    V    V_CMP       R0, 0
          ; Base16: V=0x7 → Verifiability category
          ; Compares R0 (SDL_Init result) to 0
          ; Sets flags: ZF if R0==0, SF if R0<0

0000000C  08 ?? ?? ??   A          A    A_JL        L_0004
          ; Base16: A=0x0 → Attractor category (flow control)
          ; Conditional jump: if SDL_Init < 0 → error
          ; [RELOC R_TSK_REL24 → L_0004]
; └──────────────────────────────────────────────────────────────┘

; ┌─ TSCG block: m2:Homeostasis "main game loop 35fps" ────────┐
00000010  02 ?? ?? ??   F          A    A_CALL      game_loop
          ; Base16: A=0x0 → Attractor (call = convergence point)
          ; Saves LR=0x00000014, jumps to game_loop
          ; [RELOC R_TSK_REL24 → game_loop]
; └──────────────────────────────────────────────────────────────┘

00000014  91 08 00 00   Im·O·A·A   Im   Im_FFI_CALL SDL_Quit
          ; FFI: SDL2::SDL_Quit(void) → void

00000018  D1 00 00 00   D·A·A·A    D    D_MOV_I     R0, 0
          ; Exit code 0 (success)

0000001C  9F 00         Im·L       Im   Im_EXIT
          ; Base16: Im=0x9 L=0xF → Interoperability+Localizability
          ; Terminates VM cleanly with exit code in R0

L_0004:                            ; [LOCAL] SDL init failure
00000020  D1 00 00 01   D·A·A·S    D    D_MOV_I     R0, 1
          ; Base16: value 1 = S (Structure) in last nibble
          ; Exit code 1 (error)

00000024  9F 00         Im·L       Im   Im_EXIT
```

### 2.4 `--mode tscg`

TSCG-focused output — groups code by M2 GenericConcept blocks,
shows M3 primitive distribution statistics.

```asm
; ════════════════════════════════════════════════════════════════
; TSCG Semantic Analysis — wolf3d_main.tvx
; ════════════════════════════════════════════════════════════════

; M3 Primitive Distribution (opcode categories):
;   A  (Attractor)       12 instructions  18.2%  ████████
;   S  (Structure)        8 instructions  12.1%  █████
;   F  (Flow)            15 instructions  22.7%  ██████████
;   It (Information)      6 instructions   9.1%  ████
;   D  (Dynamics)         9 instructions  13.6%  ██████
;   Im (Interop)          8 instructions  12.1%  █████
;   T  (Time)             4 instructions   6.1%  ██
;   V  (Verif)            4 instructions   6.1%  ██
;   [Gt total: 50 / Gm total: 12 / Gs total: 4]

; Active M2 GenericConcepts (from .tscg section):
;   m2:Process     → 15 instructions (raycaster, game update)
;   m2:Homeostasis → 4  instructions (35fps sync)
;   m2:Attractor   → 12 instructions (loops, entry points)
;   m2:Channel     → 8  instructions (SDL2 FFI)

; ── m2:Attractor "program entry point" ───────────────────────
[0x00000000 – 0x0000001F]
main:
    D_MOV_I    R0, SDL_INIT_VIDEO
    Im_FFI_CALL SDL_Init
    V_CMP      R0, 0
    A_JL       @error
    A_CALL     game_loop
    ...

; ── m2:Homeostasis "35fps steady state" ──────────────────────
[0x00000040 – 0x0000008F]
game_loop:
    Im_INPUT_RD
    A_CALL     update_game
    A_CALL     render_frame
    Im_FB_BLIT
    D_MOV_I    R0, 35
    T_FRAME_SYN R0
    A_JMP      game_loop

; ── m2:Process "raycaster inner loop" ────────────────────────
[0x00000200 – 0x000003FF]
render_column:
    F_FIXMUL   R0, R1, R2
    F_MULDIV   R3, R4, R5
    ...
```

---

## 3. Base16 Triskele Display

### 3.1 Inline encoding column

For each instruction, `tsk-dis` shows the Base16 Triskele encoding
of the 32-bit instruction word:

```
Encoding column format:
  XX XX XX XX   P₁·P₂·P₃·P₄

Where:
  XX XX XX XX = hex bytes (little-endian)
  P₁·P₂·P₃·P₄ = M3 primitive names for each nibble
```

Example:
```
Instruction: F_FIXMUL R0, R1, R2
Binary:      2D 00 01 02
Base16:      F·K·A·S·A·S·F

Decoded:
  High nibble of opcode: 0x2 = F (Flow category)
  Low  nibble of opcode: 0xD = K (instruction 13 = F_FIXMUL)
  dst  register:         0x0 0x0 = R0
  src1 register:         0x0 0x1 = R1
  src2 register:         0x0 0x2 = R2
```

### 3.2 Constant values in Base16 Triskele

Numeric constants shown in both hex and Base16 Triskele:

```asm
D_MOV_I   R0, 320
; → hex:    0x00000140
; → Base16: A·A·A·S·_^·A  (A=0, A=0, A=0, S=1, _^=4, A=0)
; → reads:  "zero·zero·zero·Structure·PosPole·zero"

D_MOV_I   R0, 35        ; FPS_TARGET
; → hex:    0x00000023
; → Base16: A·A·A·A·F·It  (F=2, It=3)
; → reads:  "...Flow·Information"

Im_FB_BLIT              ; opcode 0x92
; → hex:    0x92
; → Base16: Im·F  (Im=9, F=2)
; → reads:  "Interoperability·Flow" — FFI display (blit = data flow to screen)
```

### 3.3 `--base16-only` flag

Forces all numeric output exclusively in Base16 Triskele notation:

```asm
; Standard:
D_MOV_I   R0, 0x00000140   ; 320

; --base16-only:
D_MOV_I   R0, #A_A_A_S_POS_A   ; 320
```

---

## 4. Symbol Resolution

### 4.1 From `.symtab` section

All symbols from the symbol table are displayed:

```asm
; Symbols resolved from .symtab:
main:           ; [EXPORT] [ENTRY] @ 0x00000000
game_loop:      ; [EXPORT] @ 0x00000040
render_frame:   ; [EXPORT] @ 0x00000200
handle_keydown: ; [LOCAL]  [CALLBACK:SDL_KEYDOWN] @ 0x00000300
L_0004:         ; [LOCAL]  [GENERATED] @ 0x00000020
```

### 4.2 TSCG M2 tags on symbols

If the `.symtab` contains TSCG M2 tags (set by `tsk-asm` `.tscg` directive):

```asm
game_loop:      ; [EXPORT] m2:Homeostasis "35fps steady state"
render_frame:   ; [EXPORT] m2:Process     "raycaster render"
handle_keydown: ; [LOCAL]  m2:Channel     "SDL2 keyboard event"
```

### 4.3 Auto-generated labels

When no symbol exists for a jump target, `tsk-dis` generates labels:

```
Format: L_{address_hex}
Examples:
  L_0004   → address 0x00000004
  L_00A0   → address 0x000000A0
  L_1000   → address 0x00001000
```

With `--tscg-labels` flag, generated labels use M3 primitive names:

```
L_A_A_S_F   → address 0x0014  (A·A·S·F in Base16)
```

---

## 5. Section Display

### 5.1 Code section (`.code`)

```asm
; ════════════════════════════════════════════════════════════════
; Section .code
; Size:    0x00004200 (16896 bytes)
; Align:   4
; M3 tag:  F (Flow)
; Flags:   readable executable
; ════════════════════════════════════════════════════════════════
```

### 5.2 Data section (`.rodata` / `.data`)

Data sections disassembled as typed values:

```asm
; ════════════════════════════════════════════════════════════════
; Section .rodata
; Size:    0x00000200
; M3 tag:  It (Information)
; ════════════════════════════════════════════════════════════════

window_title:                      ; [STRING] "Wolfenstein 3D — TriskeleVM"
00000000  57 6F 6C 66   W·o·l·f
00000004  65 6E 73 74   e·n·s·t
00000008  65 69 6E 20   e·i·n· 
0000000C  33 44 20 E2   3·D· ·â
00000010  80 94 20 54   €·"· ·T
; [null-terminated at 0x0000001C]

cos_table:                         ; [ARRAY .dd × 256]
00000020  00 00 01 00   ; [0] 0x00010000 = 1.0 (16.16 fixed)
                        ; Base16: A·A·S·A → Structure in high byte
00000024  62 FF 00 00   ; [1] 0x0000FF62 = 0.99691 (cos 1°)
...
```

### 5.3 BSS section

```asm
; ════════════════════════════════════════════════════════════════
; Section .bss (uninitialized — zero at load)
; Size:    0x0000FA00 (64000 bytes)
; M3 tag:  S (Structure)
; ════════════════════════════════════════════════════════════════

framebuffer:    ; [RESERVE 64000 bytes] (320 × 200 × 1 byte)
game_running:   ; [RESERVE 4 bytes] (int32)
player_x:       ; [RESERVE 4 bytes] (fixed 16.16)
player_y:       ; [RESERVE 4 bytes] (fixed 16.16)
player_angle:   ; [RESERVE 4 bytes] (fixed 16.16)
```

### 5.4 Import section (`.import`)

```asm
; ════════════════════════════════════════════════════════════════
; Section .import — FFI Declarations
; M3 tag:  Im (Interoperability)
; ════════════════════════════════════════════════════════════════

; [FFI] SDL2
SDL_Init:           sig:SIG_INT_INT           lib:"SDL2"
SDL_CreateWindow:   sig:SIG_PTR_PTR_IIIII     lib:"SDL2"
SDL_PollEvent:      sig:SIG_INT_PTR           lib:"SDL2"
SDL_RenderPresent:  sig:SIG_VOID_PTR          lib:"SDL2"
SDL_Quit:           sig:SIG_VOID_VOID         lib:"SDL2"

; [CALLBACK]
handle_keydown:     event:SDL_KEYDOWN         sig:SIG_PTR_VOID
handle_quit:        event:SDL_QUIT            sig:SIG_VOID_VOID
```

### 5.5 TSCG annotation section (`.tscg`)

```asm
; ════════════════════════════════════════════════════════════════
; Section .tscg — Semantic Annotations
; M3 tag:  K (Knowledge)
; ════════════════════════════════════════════════════════════════

[0x00000000 – 0x0000001F]  m2:Attractor   "program entry point — system bootstrap"
[0x00000040 – 0x0000008F]  m2:Homeostasis "main loop — 35fps steady state"
[0x00000090 – 0x000000BF]  m2:Channel     "SDL2 framebuffer blit"
[0x000000C0 – 0x000000CF]  m2:Homeostasis "frame rate regulation — T_FRAME_SYN"
[0x00000200 – 0x000003FF]  m2:Process     "ray casting — F × It × D"
[0x00000400 – 0x000004FF]  m2:Process     "game update — D × It × F"
```

### 5.6 Raw asset section (`.raw`)

```
; ════════════════════════════════════════════════════════════════
; Section .raw — Binary Assets (not disassembled)
; ════════════════════════════════════════════════════════════════

; Asset [0]: walls.bin
;   Type:   TEXTURE
;   Size:   0x00010000 (65536 bytes)
;   Offset: 0x00008000
;   M3 tag: F (Flow) — visual data flow

; Asset [1]: sprites.bin
;   Type:   TEXTURE
;   Size:   0x00004000 (16384 bytes)
;   Offset: 0x00018000
;   M3 tag: S (Structure) — sprite structure

; Asset [2]: E1M1.map
;   Type:   MAP
;   Size:   0x00002000 (8192 bytes)
;   Offset: 0x0001C000
;   M3 tag: It (Information) — map data

; Use --extract-assets to dump raw data to files
```

---

## 6. Relocation Display

```asm
; ════════════════════════════════════════════════════════════════
; Section .reltab — Relocations
; M3 tag:  L (Localizability)
; ════════════════════════════════════════════════════════════════

Offset      Type              Symbol
0x00000004  R_TSK_FFI         SDL_Init        → resolved at load
0x0000000C  R_TSK_REL24       L_0004          → +0x14
0x00000010  R_TSK_REL24       game_loop       → +0x30
0x00000014  R_TSK_FFI         SDL_Quit        → resolved at load
0x00000050  R_TSK_POOL        cos_table       → .rodata+0x20
```

---

## 7. Statistics and Summary

With `--stats` flag:

```
; ════════════════════════════════════════════════════════════════
; wolf3d_main.tvx — Statistics
; ════════════════════════════════════════════════════════════════

File size:        0x00024000 (147456 bytes)

Sections:
  .code           0x00004200  (16896 bytes)  28.6%
  .rodata         0x00000800  (2048 bytes)    3.5%
  .data           0x00000100  (256 bytes)     0.4%
  .bss            0x0000FA00  (64000 bytes)  (virtual)
  .symtab         0x00000400  (1024 bytes)    0.7%
  .tscg           0x00000200  (512 bytes)     0.3%
  .raw            0x00016000  (90112 bytes)  61.0%

Instructions:     1024 total
  Per category:
    A  Attractor      142  13.9%  ████████████████
    S  Structure      186  18.2%  █████████████████████
    F  Flow           198  19.3%  ██████████████████████
    It Information     89   8.7%  ██████████
    D  Dynamics       112  10.9%  ████████████
    R  Represent.      23   2.2%  ██
    E  Evolvability     4   0.4%  
    V  Verifiability   67   6.5%  ███████
    O  Observability   12   1.2%  █
    Im Interop.        98   9.6%  ███████████
    T  Time            18   1.8%  ██
    _^ PosPole         41   4.0%  ████
    _$ NegPole         34   3.3%  ███

  Gt (Territory):  727  71.0%  — computation-dominant
  Gm (Map):        204  19.9%  — representation + FFI
  Gs (Stereopsis):  93   9.1%  — time + memory management

Symbols:          47 total (12 exported, 35 local)
Relocations:      89 total (23 FFI, 66 internal)
TSCG annotations:  8 blocks

Active M2 GenericConcepts:
  m2:Process     38.2% coverage
  m2:Attractor   13.9% coverage
  m2:Homeostasis  5.3% coverage
  m2:Channel      9.6% coverage
  m2:Structure   18.2% coverage
```

---

## 8. Diff Mode

`--diff` mode compares two binaries — useful for verifying compiler output:

```
tsk-dis --diff wolf3d_v1.tvx wolf3d_v2.tvx

; ════════════════════════════════════════════════════════════════
; Diff: wolf3d_v1.tvx vs wolf3d_v2.tvx
; ════════════════════════════════════════════════════════════════

; render_frame @ 0x00000200 — MODIFIED
  v1: F_FIXMUL   R0, R1, R2      ; 00000200: 2D 00 01 02
  v2: F_MULDIV   R3, R1, R2      ; 00000200: 2C 03 01 02
; 1 instruction changed

; game_loop @ 0x00000040 — UNCHANGED

; Total: 1 function modified, 46 functions unchanged
; Size delta: +0 bytes
```

---

## 9. Interactive Mode

`tsk-dis --interactive wolf3d.tvx` opens a REPL:

```
tsk-dis 0.1.0 — wolf3d.tvx loaded (147456 bytes)
Type 'help' for commands.

> list main
; main @ 0x00000000 [EXPORT] [ENTRY]
00000000  D_MOV_I    R0, 0x00000020   ; SDL_INIT_VIDEO
00000004  Im_FFI_CALL SDL_Init
...

> list 0x200 0x220
; render_frame+0x00
00000200  F_FIXMUL   R0, R1, R2
00000204  F_MULDIV   R3, R4, R5
...

> sym game_loop
; game_loop: .code @ 0x00000040 [EXPORT]
; TSCG: m2:Homeostasis "35fps steady state"

> tscg 0x200
; TSCG annotation at 0x200:
;   m2:Process "ray casting — F × It × D"
;   Range: [0x00000200 – 0x000003FF]

> b16 320
; 320 = 0x00000140
; Base16 Triskele: #A_A_A_S_POS_A
; Nibbles: A(0) A(0) A(0) S(1) _^(4) A(0)

> b16 0xFF
; 255 = 0x000000FF
; Base16 Triskele: #A_A_A_A_L_L
; Nibbles: A(0) A(0) A(0) A(0) L(F) L(F)

> stats
; [shows statistics summary]

> quit
```

---

## 10. Command-Line Interface

```
tsk-dis [options] <input> [-o <output.tsk.dis>]

Input formats:
  .tobj   object file (unlinked)
  .tvx    executable
  .tvl    shared library
  .tva    static archive (disassembles all members)

Options:

Output mode:
  --mode minimal       bare mnemonics, no annotations
  --mode standard      addresses + encoding + M3 tag (default)
  --mode annotated     full semantic annotations
  --mode tscg          TSCG-focused grouping

Content selection:
  --code               disassemble .code section (default: on)
  --data               disassemble .data / .rodata sections
  --bss                show .bss layout
  --imports            show .import section
  --exports            show exported symbols
  --tscg               show .tscg annotation section
  --relocs             show .reltab section
  --raw                show .raw asset directory (not data)
  --all                all sections

Numeric display:
  --base16             show Base16 Triskele encoding (default: on)
  --base16-only        suppress hex, show only Base16 Triskele
  --no-base16          suppress Base16 Triskele column
  --decimal            show immediates in decimal

Symbol handling:
  --symbols            show symbol table
  --no-labels          suppress auto-generated labels
  --tscg-labels        use Base16 Triskele in auto-labels

TSCG:
  --tscg-annotations   inline TSCG block annotations (default: on)
  --no-tscg            suppress all TSCG output
  --m3-stats           show M3 primitive distribution

Analysis:
  --stats              show section and instruction statistics
  --diff <file2>       compare with second binary
  --call-graph         show call graph (requires symbols)
  --xrefs              show cross-references

Output:
  -o <file>            write to file (default: stdout)
  --color              ANSI color output (auto-detected)
  --no-color           disable colors
  --width <N>          output width in columns (default: 120)

Asset handling:
  --extract-assets <dir>  extract .raw assets to directory

Interactive:
  --interactive        launch interactive REPL

Examples:
  tsk-dis wolf3d.tvx
  tsk-dis --mode annotated --all wolf3d.tvx -o wolf3d.tsk.dis
  tsk-dis --mode tscg --m3-stats wolf3d.tvx
  tsk-dis --base16-only --data wolf3d.tvx
  tsk-dis --diff wolf3d_v1.tvx wolf3d_v2.tvx
  tsk-dis --interactive wolf3d.tvx
  tsk-dis --extract-assets ./assets wolf3d.tvx
  tsk-dis --mode minimal wolf3d.tvx | tsk-asm - -o roundtrip.tobj
```

---

## 11. Color Scheme (ANSI terminal)

```
Opcode category (M3 primitive):
  A  (Attractor)     → cyan       \x1b[36m
  S  (Structure)     → blue       \x1b[34m
  F  (Flow)          → green      \x1b[32m
  It (Information)   → yellow     \x1b[33m
  D  (Dynamics)      → magenta    \x1b[35m
  R  (Represent.)    → white      \x1b[37m
  E  (Evolvability)  → bright white \x1b[97m
  V  (Verifiab.)     → bright cyan \x1b[96m
  O  (Observab.)     → bright blue \x1b[94m
  Im (Interop.)      → bright green \x1b[92m
  T  (Time)          → bright yellow \x1b[93m
  _^ (PosPole)       → bright magenta \x1b[95m
  _$ (NegPole)       → red         \x1b[31m
  K  (Knowledge)     → bright red  \x1b[91m
  Ss (Symbol)        → orange      \x1b[38;5;208m
  L  (Localiz.)      → purple      \x1b[38;5;135m

Other elements:
  Labels/symbols     → bold        \x1b[1m
  Comments           → dim         \x1b[2m
  TSCG annotations   → italic      \x1b[3m
  Addresses          → dim white   \x1b[2;37m
  Base16 Triskele    → color per primitive (see above)
  Strings            → bright yellow \x1b[93m
  Numbers            → bright white \x1b[97m
```

---

## 12. Round-trip Fidelity

The `--mode minimal` output is designed to be re-assemblable:

```bash
# Disassemble
tsk-dis --mode minimal wolf3d.tvx -o wolf3d_rt.tsk

# Re-assemble
tsk-asm wolf3d_rt.tsk -o wolf3d_rt.tobj

# Link
tsk-link wolf3d_rt.tobj sdl2.tvl libc_stub.tva -o wolf3d_rt.tvx

# Verify (should be byte-identical modulo timestamps)
tsk-dis --diff wolf3d.tvx wolf3d_rt.tvx
```

**Limitations of round-trip**:
- Generated label names (`L_0004`) differ from original source names
  if `.tdbg` debug symbols are not present
- `.tdbg` file provides original source names for full fidelity:
  `tsk-dis --debug wolf3d.tdbg wolf3d.tvx`
- Macro expansions are not recovered (they appear as inline instructions)
- `#define` constants appear as literal values

---

## 13. Implementation Notes (Rust)

```
Crate structure:
  tsk-dis/
  ├── src/
  │   ├── main.rs          CLI argument parsing (clap)
  │   ├── loader.rs        .tobj/.tvx/.tvl/.tva parser
  │   ├── disasm.rs        instruction decoder (32-bit → mnemonic)
  │   ├── base16.rs        Base16 Triskele encoder/decoder
  │   ├── symbols.rs       symbol table management
  │   ├── tscg.rs          .tscg section reader + annotation display
  │   ├── output/
  │   │   ├── minimal.rs   --mode minimal formatter
  │   │   ├── standard.rs  --mode standard formatter
  │   │   ├── annotated.rs --mode annotated formatter
  │   │   └── tscg_mode.rs --mode tscg formatter
  │   ├── stats.rs         statistics computation
  │   ├── diff.rs          binary diff engine
  │   └── interactive.rs   REPL (rustyline)
  └── Cargo.toml

Key dependencies:
  clap        → CLI argument parsing
  rustyline   → interactive REPL readline
  colored     → ANSI color output
  serde       → .tobj structure deserialization
```

---

*TriskeleToolchain — tsk-dis Specification v0.1.0*  
*Echopraxium with the collaboration of Claude AI — 2026-05-30*
