# tsk-link — Triskele Linker Specification

**Author**: Echopraxium with the collaboration of Claude AI  
**Version**: 0.1.0  
**Date**: 2026-05-30  
**Status**: Draft — TriskeleToolchain  
**Input extensions**: `.tobj`, `.tvl`, `.tva`  
**Output extensions**: `.tvx`, `.tvl`, `.tva`

---

## 1. Overview

`tsk-link` is the linker for TriskeleVM. It combines multiple `.tobj` object
files and `.tva` static archives into a final executable (`.tvx`), shared
library (`.tvl`), or static archive (`.tva`).

Design principles:
- **Two-pass linking** — symbol collection then resolution
- **Base16 Triskele** — all addresses and metadata in M3 encoding
- **TSCG-aware** — merges `.tscg` annotation sections, preserves M2 semantics
- **C ABI compatible** — FFI declarations resolved via `.import` sections
- **Minimal** — inspired by LLD/mold simplicity, not GNU ld complexity

---

## 2. Linking Pipeline

```
Input:
  wolf3d_main.tobj
  wolf3d_render.tobj
  wolf3d_map.tobj
  wolf3d_audio.tobj
  sdl2.tvl              (shared library — FFI bindings)
  libc_stub.tva         (static archive — stdlib stub)

Step 1: Load
  → parse all .tobj headers and section tables
  → load .tva archives, enumerate members
  → record .tvl shared libraries (not linked in, resolved at runtime)

Step 2: Symbol collection (Pass 1)
  → build global symbol table from all .symtab sections
  → detect duplicate definitions → error
  → detect weak symbols → lower priority
  → collect undefined (.extern) symbols

Step 3: Archive member selection
  → for each undefined symbol, check .tva archives
  → pull in archive members that define needed symbols
  → repeat until no new members added (closure)

Step 4: Symbol resolution (Pass 2)
  → resolve all .extern references to their definitions
  → detect remaining undefined symbols → error (unless .tvl)
  → assign final virtual addresses to all sections

Step 5: Section merging
  → concatenate same-type sections from all inputs
  → apply alignment padding between sections
  → merge .tscg annotation sections (adjust offsets)
  → merge .symtab, .strtab, .reltab sections

Step 6: Relocation application
  → for each relocation entry:
      R_TSK_ABS32/64  → patch absolute address
      R_TSK_REL24     → patch PC-relative offset (Type J)
      R_TSK_REL19     → patch PC-relative offset (Type I)
      R_TSK_POOL      → patch constant pool reference
      R_TSK_FFI       → emit .import entry (resolved at VM load)

Step 7: Output generation
  → write .tvx / .tvl / .tva header
  → write merged sections in canonical order
  → write .tmap link map (optional)
  → write .tdbg debug symbols (optional)

Output:
  wolf3d.tvx            (executable)
  wolf3d.tmap           (link map — optional)
  wolf3d.tdbg           (debug symbols — optional)
```

---

## 3. Symbol Table

### 3.1 Symbol types

```
FUNCTION    executable code symbol (.proc / label in .code)
OBJECT      data symbol (.data / .rodata / .bss)
SECTION     section itself
FILE        source filename (from .module directive)
EXTERN      undefined — must be resolved
FFI         native C symbol — resolved at VM load time
CALLBACK    VM function registered as C callback
WEAK        lower priority — overridable by GLOBAL
```

### 3.2 Symbol visibility

```
GLOBAL      visible to all modules — declared with .export
LOCAL       visible within module only — no .export
HIDDEN      global but not re-exported from .tvl
WEAK        global but overridable — .weak directive
```

### 3.3 Global symbol table structure

```
Entry (64 bytes, Base16 Triskele):
  Offset  Size  Field
  0x00    8     Symbol value (virtual address after linking)
  0x08    4     Symbol size (bytes)
  0x0C    4     Name offset in merged .strtab
  0x10    1     Symbol type (FUNCTION/OBJECT/FFI/CALLBACK...)
  0x11    1     Symbol binding (GLOBAL/LOCAL/WEAK/HIDDEN)
  0x12    1     Symbol visibility
  0x13    1     Section index in merged section table
  0x14    4     Source module index (for diagnostics)
  0x18    4     Source line number (from .tdbg — optional)
  0x1C    4     TSCG M2 tag hash (GenericConcept IRI)
  0x20    4     TSCG M3 tag (dominant primitive nibble)
  0x24    28    Reserved
```

### 3.4 Duplicate symbol resolution

```
Priority rules (highest to lowest):
  1. GLOBAL  (strong definition) — wins unconditionally
  2. WEAK    (weak definition)   — loses to any GLOBAL
  3. EXTERN  (undefined)         — must be satisfied

Conflicts:
  GLOBAL vs GLOBAL  → ERROR: duplicate symbol
  GLOBAL vs WEAK    → GLOBAL wins, warning suppressed
  WEAK   vs WEAK    → first-seen wins, warning emitted
  EXTERN vs GLOBAL  → resolved (normal case)
  EXTERN vs EXTERN  → unresolved → ERROR at end of pass 2
  FFI    vs GLOBAL  → ERROR: cannot shadow FFI symbol
```

---

## 4. Section Merging

### 4.1 Canonical section order in output

```
.tvx output section order:
  1.  .code          (executable — F/Flow tag)
  2.  .rodata        (read-only data — It/Information tag)
  3.  .data          (initialized r/w — S/Structure tag)
  4.  .bss           (uninitialized — S/Structure tag)
  5.  .symtab        (symbols — Ss/Symbol tag)
  6.  .strtab        (strings — Ss/Symbol tag)
  7.  .reltab        (relocations — L/Localizability tag)
  8.  .tscg          (TSCG annotations — K/Knowledge tag)
  9.  .import        (FFI declarations — Im/Interop tag)
  10. .export        (exported symbols — Im/Interop tag)
  11. .debug         (debug info — O/Observability tag) [optional]
  12. .raw           (binary assets — always last) [optional]
```

### 4.2 Section merging algorithm

```
For each section type T:
  merged_T.data = []
  merged_T.offset_map = {}    ; input_section → offset in merged

  For each input module M (in link order):
    if M has section T:
      pad to alignment requirement
      offset_map[M.T] = len(merged_T.data)
      merged_T.data += M.T.data

  Update all cross-references using offset_map
```

### 4.3 Alignment padding

```
Between sections from different modules:
  .code   → align to 4 bytes  (instruction alignment)
  .rodata → align to 8 bytes  (max data alignment)
  .data   → align to 8 bytes
  .bss    → align to 8 bytes

Within a section, respect per-symbol .align directives
  (preserved from assembler output in .symtab)
```

### 4.4 .tscg section merging

The TSCG annotation section requires special handling:
all address ranges must be rebased to final virtual addresses.

```
For each .tscg entry from input module M:
  entry.start_offset += section_base[M.code_section]
  entry.end_offset   += section_base[M.code_section]
  append to merged .tscg
```

---

## 5. Relocation Application

### 5.1 Relocation types

```
R_TSK_ABS32   — absolute 32-bit address patch
  value = symbol.virtual_address + addend
  patch: write 32-bit LE at reloc.offset

R_TSK_ABS64   — absolute 64-bit address patch
  value = symbol.virtual_address + addend
  patch: write 64-bit LE at reloc.offset

R_TSK_REL24   — PC-relative 24-bit (Type J instructions)
  offset = (symbol.virtual_address - (reloc.offset + 4)) >> 2
  check: offset fits in 24-bit signed range (±8MB)
  patch: write offset into bits [23:0] of instruction word

R_TSK_REL19   — PC-relative 19-bit (Type I branches)
  offset = (symbol.virtual_address - (reloc.offset + 4)) >> 2
  check: offset fits in 19-bit signed range (±256K)
  patch: write offset into bits [18:0] of instruction word

R_TSK_POOL    — constant pool reference
  pool_entry.value = symbol.virtual_address
  patch: pool index already in instruction (no change needed)

R_TSK_FFI     — native FFI symbol
  → NOT patched in binary
  → emitted as .import entry in output
  → resolved at VM load time via dlsym(SDL2, "SDL_Init")
  → placeholder value 0xDEADFFI kept in binary (trap on misuse)
```

### 5.2 Relocation error handling

```
Overflow (offset too large):
  R_TSK_REL24: distance > ±8MB
  → ERROR: "relocation overflow: game_loop → render_frame (+12MB)"
  → fix: use L_FAR_CALL (0xFE) for long jumps
  → or: linker-inserted trampolines (--trampolines flag)

Undefined symbol:
  → ERROR: "undefined symbol: SDL_CreateRenderer"
  → hint: "did you link sdl2.tvl?"

Duplicate definition:
  → ERROR: "duplicate symbol: render_frame"
  → hint: "defined in wolf3d_render.tobj and wolf3d_ui.tobj"
```

---

## 6. Virtual Address Layout

### 6.1 Default memory map

```
Address range       Content
0x00000000          NULL (unmapped — catches null ptr dereference)
0x00001000          .code  (entry point here)
0x00001000 + code_size + pad
                    .rodata
... + rodata_size + pad
                    .data
... + data_size + pad
                    .bss   (zero-initialized at VM load)
... + bss_size + pad
0x70000000          Stack (grows downward)
0x80000000          Heap  (grows upward, managed by P_ALLOC)
0xF0000000          VM internal (FFI dispatch tables, etc.)
0xFFFFFFFF          Sentinel
```

### 6.2 Custom layout via linker script `.tldf`

```yaml
# wolf3d.tldf — Triskele Linker Definition File
# Extension: .tldf (Triskele Linker Definition File)

layout:
  null_page:    { base: 0x00000000, size: 0x1000 }
  code:         { base: 0x00001000, align: 4 }
  rodata:       { follows: code,    align: 8 }
  data:         { follows: rodata,  align: 8 }
  bss:          { follows: data,    align: 8 }
  stack:        { base: 0x70000000, size: 0x100000,  direction: down }
  heap:         { base: 0x80000000, size: 0x00400000, direction: up }
```

---

## 7. Archive Handling (`.tva`)

### 7.1 Archive format

```
.tva file layout:
  [0x00]  Magic: "TSKA"          (Triskele Static Archive)
  [0x04]  Version (Base16)
  [0x08]  Member count N (Base16)
  [0x0C]  Symbol index offset
  [0x10]  N × member directory entries (48 bytes each)
  [...]   Member data (.tobj files, concatenated)
  [...]   Archive symbol index
```

**Member directory entry (48 bytes)**:
```
Offset  Size  Field
0x00    4     Member offset in archive
0x04    4     Member size
0x08    4     Name offset in archive string table
0x0C    4     Timestamp
0x10    4     Export symbol count
0x14    28    Reserved
```

**Archive symbol index**:
```
; Fast lookup: symbol name → member index
; Sorted for binary search
Entry (16 bytes):
  0x00  8   Symbol name hash (FNV-64)
  0x08  4   Member index
  0x0C  4   Symbol offset within member .symtab
```

### 7.2 Archive member selection

```
Algorithm (iterative — handles mutual dependencies):

  needed = {all undefined symbols from .tobj inputs}
  added  = {}

  repeat:
    for each symbol S in needed:
      if S defined in archive member M and M not in added:
        add M to link set
        added += {M}
        needed += {M.undefined_symbols} - {already_defined}
  until no change

  if needed not empty:
    ERROR: undefined symbols after archive extraction
```

---

## 8. Shared Library Handling (`.tvl`)

### 8.1 Linking against a `.tvl`

```
.tvl is NOT linked into the output binary.
It provides:
  → symbol declarations (for type checking)
  → .import entries (resolved at VM load time)

At VM load time:
  TriskeleVM reads .import section
  → Im_FFI_CALL SDL_Init:
      dlopen("SDL2") → handle
      dlsym(handle, "SDL_Init") → fn_ptr
      patch dispatch table entry
```

### 8.2 `.tvl` export table

```
.tvl contains a .export section:
  → all GLOBAL/HIDDEN symbols with their signatures
  → used by tsk-link for type checking during linking
  → used by tsk-dis for symbol display
  → NOT loaded into memory (VM loads native .dll/.so instead)
```

### 8.3 FFI signature verification

```
When linking wolf3d_main.tobj against sdl2.tvl:
  tsk-link checks:
    wolf3d_main.tobj:  .import SDL_Init sig:SIG_INT_INT
    sdl2.tvl:         .export SDL_Init sig:SIG_INT_INT  ✓

  Mismatch:
    wolf3d_main.tobj:  .import SDL_Init sig:SIG_INT_INT
    sdl2.tvl:         .export SDL_Init sig:SIG_VOID_INT ✗
    → ERROR: "FFI signature mismatch: SDL_Init"
             "expected SIG_INT_INT, got SIG_VOID_INT"
```

---

## 9. Link Map (`.tmap`)

Generated with `--map wolf3d.tmap`:

```
; ════════════════════════════════════════════════════════════════
; wolf3d.tvx — Link Map
; tsk-link 0.1.0 — 2026-05-30
; ════════════════════════════════════════════════════════════════

; ── Memory Layout ────────────────────────────────────────────────
Virtual Address     Size        Section     Source
0x00001000          0x00004200  .code
  0x00001000        0x00000200  .code       wolf3d_main.tobj
  0x00001200        0x00001800  .code       wolf3d_render.tobj
  0x00002A00        0x00001200  .code       wolf3d_map.tobj
  0x00003C00        0x00000600  .code       libc_stub.tva(malloc.tobj)
  0x00004200        0x00000000  .code       [pad to align 8]

0x00005200          0x00000800  .rodata
  0x00005200        0x00000200  .rodata     wolf3d_main.tobj
  0x00005400        0x00000400  .rodata     wolf3d_render.tobj  ; cos_table
  0x00005800        0x00000200  .rodata     wolf3d_map.tobj

0x00006000          0x00000100  .data
  0x00006000        0x00000080  .data       wolf3d_main.tobj
  0x00006080        0x00000080  .data       wolf3d_map.tobj

0x00006100          0x0000FA00  .bss
  0x00006100        0x0000FA00  .bss        wolf3d_main.tobj    ; framebuffer

; ── Symbol Table ─────────────────────────────────────────────────
Virtual Address     Size        Binding     Symbol              Source
0x00001000          0x00000200  GLOBAL      main                wolf3d_main.tobj
0x00001200          0x00001800  GLOBAL      render_frame        wolf3d_render.tobj
0x00001240          0x000000A0  GLOBAL      render_column       wolf3d_render.tobj
0x00002A00          0x00000400  GLOBAL      load_map            wolf3d_map.tobj
0x00006000          0x00000004  GLOBAL      game_running        wolf3d_main.tobj
0x00006004          0x00000004  GLOBAL      player_x            wolf3d_main.tobj
0x00005400          0x00000400  LOCAL       cos_table           wolf3d_render.tobj

; ── FFI Symbols (resolved at VM load) ────────────────────────────
Symbol              Library     Signature
SDL_Init            SDL2        SIG_INT_INT
SDL_CreateWindow    SDL2        SIG_PTR_PTR_IIIII
SDL_PollEvent       SDL2        SIG_INT_PTR
SDL_RenderPresent   SDL2        SIG_VOID_PTR
SDL_Quit            SDL2        SIG_VOID_VOID

; ── Archive Members Used ─────────────────────────────────────────
Archive             Member              Symbols pulled
libc_stub.tva       malloc.tobj         malloc, free, realloc
libc_stub.tva       string.tobj         memcpy, memset, strlen
libc_stub.tva       stdlib.tobj         exit, abs

; ── Discarded Archive Members ────────────────────────────────────
libc_stub.tva       stdio.tobj          (no references to printf, etc.)
libc_stub.tva       math.tobj           (no references to sin, cos, etc.)

; ── TSCG Annotation Summary ──────────────────────────────────────
M2 GenericConcept   Coverage    Blocks
m2:Process          38.2%       12 blocks
m2:Attractor        13.9%        5 blocks
m2:Homeostasis       5.3%        2 blocks
m2:Channel           9.6%        4 blocks
m2:Structure        18.2%        6 blocks

; ── Sizes ────────────────────────────────────────────────────────
Section             Size        Percentage
.code               16896       11.5%
.rodata              2048        1.4%
.data                 256        0.2%
.bss                64000       43.5%  (virtual — not in file)
.symtab              2048        1.4%
.tscg                 512        0.3%
.raw                90112       61.2%
Total (file)       147456      100.0%
Total (memory)     211456      (including .bss)

; ── Base16 Triskele Address Summary ──────────────────────────────
Entry point:  main @ 0x00001000
Base16:       A·A·A·S·A·A·A
Primitives:   A(0)·A(0)·A(0)·S(1)·A(0)·A(0)·A(0)
              "...Structure..." — code begins at Structure boundary
```

---

## 10. Debug Symbols (`.tdbg`)

Generated with `--debug`:

```
.tdbg file layout:
  [0x00]  Magic: "TSKD"
  [0x04]  Version (Base16)
  [0x08]  Source file table
  [...]   Line number table
  [...]   Symbol name table (original names, before mangling)
  [...]   Macro expansion records
  [...]   TSCG annotation extensions (full IRI strings)
```

**Line number table entry (24 bytes)**:
```
Offset  Size  Field
0x00    8     Virtual address
0x08    4     Source file index
0x0C    4     Line number
0x10    4     Column number
0x14    4     Flags (is_stmt, prologue_end, epilogue_begin)
```

Used by `tsk-dbg` (DAP server) to map VM instruction addresses
back to source `.tsk` file lines for VS Code breakpoints.

---

## 11. Linker Scripts (`.tldf`)

Extension `.tldf` — Triskele Linker Definition File (YAML format).

### 11.1 Full syntax

```yaml
# my_project.tldf

# Override memory layout
layout:
  null_page:
    base:  0x00000000
    size:  0x00001000
    flags: none

  code:
    base:  0x00001000
    align: 4
    flags: readable executable

  rodata:
    follows: code
    align:   8
    flags:   readable

  data:
    follows: rodata
    align:   8
    flags:   readable writable

  bss:
    follows: data
    align:   8
    flags:   readable writable

  stack:
    base:      0x70000000
    size:      0x00100000   ; 1MB
    direction: down
    flags:     readable writable

  heap:
    base:      0x80000000
    size:      0x00400000   ; 4MB
    direction: up
    flags:     readable writable

# Force section placement
sections:
  .code:
    region: code
    modules:
      - wolf3d_main        ; entry point first
      - wolf3d_render      ; then render (hot path)
      - wolf3d_map
      - "*"                ; everything else

  .rodata:
    region:  rodata
    align:   16
    modules: ["*"]

# Symbol definitions
symbols:
  __stack_top:   0x70100000
  __heap_start:  0x80000000
  __heap_end:    0x80400000

# Keep symbols (prevent dead code elimination)
keep:
  - main
  - handle_keydown
  - handle_quit

# Dead code elimination
eliminate:
  unreferenced: true       ; remove unreferenced functions
  keep_debug:   false      ; remove .debug in release builds
```

### 11.2 Default linker script (built-in)

If no `.tldf` provided, `tsk-link` uses internal defaults:

```yaml
layout:
  null_page: { base: 0x00000000, size: 0x1000 }
  code:      { base: 0x00001000, align: 4 }
  rodata:    { follows: code,    align: 8 }
  data:      { follows: rodata,  align: 8 }
  bss:       { follows: data,    align: 8 }
  stack:     { base: 0x70000000, size: 0x100000,  direction: down }
  heap:      { base: 0x80000000, size: 0x400000,  direction: up }

eliminate:
  unreferenced: false      ; conservative — keep everything
```

---

## 12. Dead Code Elimination

With `--dce` flag or `eliminate: unreferenced: true` in `.tldf`:

```
Algorithm:
  1. Mark entry point as reachable
  2. Mark all .callback symbols as reachable (called from C)
  3. Mark all .export symbols as reachable (library)
  4. Traverse call graph:
     → for each reachable function F:
         mark all functions called by F as reachable
         mark all data referenced by F as reachable
  5. Remove unreachable functions and data

Wolf3D result (estimated):
  Input:  libc_stub.tva — 12 archive members
  Output: 3 members used (malloc, string, stdlib)
          9 members eliminated (stdio, math, etc.)
  Saving: ~40% of archive code
```

---

## 13. Command-Line Interface

```
tsk-link [options] <inputs...> -o <output>

Input types:
  .tobj   object file (assembled by tsk-asm or tsk-cc)
  .tvl    shared library (symbols only — not linked in)
  .tva    static archive (members selected as needed)

Output types (determined by -o extension or --type):
  .tvx    executable (default if .tobj inputs, no --type)
  .tvl    shared library (--type library)
  .tva    static archive (--type archive)

Options:

Output:
  -o <file>              output file (required)
  --type executable      force .tvx output
  --type library         force .tvl output
  --type archive         force .tva output
  --entry <symbol>       entry point (default: main)

Symbol handling:
  --export <sym>         add symbol to exports (supplements .export)
  --undefined <sym>      allow undefined symbol (satisfied at runtime)
  --no-undefined         error on any undefined symbol (default)
  --weak <sym>           force symbol to WEAK binding

Linker script:
  --script <file.tldf>   use custom linker script
  --section-start <s>=<addr>  override section base address

Optimization:
  --dce                  dead code elimination
  --no-dce               disable DCE (default)
  --trampolines          auto-insert trampolines for long jumps
  --strip-debug          remove .debug section from output

Debug / diagnostics:
  --map <file.tmap>      generate link map
  --debug                generate .tdbg debug symbols
  --verbose              verbose linking progress
  --print-map            print map to stdout
  --print-gc-sections    print eliminated sections (with --dce)
  --warn-common          warn on COMMON symbols
  --warn-multiple-defs   warn on multiple weak definitions
  --error-limit <N>      stop after N errors (default: 20)

TSCG:
  --tscg-merge           merge .tscg sections (default: on)
  --no-tscg              discard all .tscg sections
  --tscg-stats           print TSCG coverage statistics

Asset bundling:
  --raw-asset <file>:<type>  add raw asset to .raw section
  --raw-dir <dir>        add all files from directory as assets

Examples:

  # Link Wolf3D executable
  tsk-link wolf3d_main.tobj wolf3d_render.tobj wolf3d_map.tobj \
            sdl2.tvl libc_stub.tva \
            -o wolf3d.tvx --entry main \
            --map wolf3d.tmap --debug

  # Add assets to bundle
  tsk-link wolf3d_main.tobj wolf3d_render.tobj wolf3d_map.tobj \
            sdl2.tvl libc_stub.tva \
            --raw-asset assets/walls.bin:TEXTURE \
            --raw-asset assets/sprites.bin:TEXTURE \
            --raw-asset assets/E1M1.map:MAP \
            -o wolf3d.tvx

  # Build shared library
  tsk-link sdl2_bindings.tobj \
            --type library \
            --export SDL_Init --export SDL_Quit \
            -o sdl2.tvl

  # Build static archive
  tsk-link malloc.tobj string.tobj stdio.tobj stdlib.tobj math.tobj \
            --type archive \
            -o libc_stub.tva

  # With DCE and custom script
  tsk-link wolf3d_main.tobj wolf3d_render.tobj \
            sdl2.tvl libc_stub.tva \
            --script wolf3d.tldf \
            --dce --strip-debug \
            -o wolf3d_release.tvx \
            --map wolf3d_release.tmap
```

---

## 14. Error Messages

All error messages include:
- Source module and symbol name
- Offset in Base16 Triskele
- Hint for resolution

```
ERROR [tsk-link] duplicate symbol: render_frame
  → defined in: wolf3d_render.tobj @ 0x00000000  (S·A·A·A·A·A·A·A)
  → also in:    wolf3d_ui.tobj    @ 0x00000040  (S·A·A·A·A·_^·A·A)
  → hint: rename one definition or make it LOCAL (remove .export)

ERROR [tsk-link] undefined symbol: SDL_CreateRenderer
  → referenced in: wolf3d_render.tobj @ 0x000001A0  (S·_^·A·A·A·A)
  → hint: add sdl2.tvl to link command, or declare .import SDL_CreateRenderer

ERROR [tsk-link] relocation overflow: R_TSK_REL24
  → from: wolf3d_render.tobj:render_column @ 0x00002000
  → to:   wolf3d_audio.tobj:audio_update   @ 0x00F00000
  → distance: +0xEE0000 (15.3MB) exceeds ±8MB limit
  → hint: use L_FAR_CALL (0xFE) or link with --trampolines

ERROR [tsk-link] FFI signature mismatch: SDL_Init
  → wolf3d_main.tobj declares: sig:SIG_INT_INT
  → sdl2.tvl exports:          sig:SIG_VOID_INT
  → hint: check SDL2 binding declarations in sdl2.tvl

WARNING [tsk-link] multiple weak definitions: debug_handler
  → wolf3d_main.tobj (used)
  → wolf3d_debug.tobj (discarded)
```

---

## 15. Implementation Notes (Rust)

```
Crate structure:
  tsk-link/
  ├── src/
  │   ├── main.rs           CLI argument parsing (clap)
  │   ├── loader.rs         .tobj / .tvl / .tva parser
  │   ├── archive.rs        .tva archive member extraction
  │   ├── symbols.rs        global symbol table (Pass 1)
  │   ├── resolver.rs       symbol resolution (Pass 2)
  │   ├── layout.rs         virtual address assignment
  │   ├── merger.rs         section merging
  │   ├── relocator.rs      relocation application
  │   ├── dce.rs            dead code elimination
  │   ├── script.rs         .tldf linker script parser (serde_yaml)
  │   ├── output/
  │   │   ├── tvx.rs        .tvx writer
  │   │   ├── tvl.rs        .tvl writer
  │   │   ├── tva.rs        .tva writer
  │   │   ├── tmap.rs       .tmap link map writer
  │   │   └── tdbg.rs       .tdbg debug symbols writer
  │   └── tscg.rs           .tscg section merger + stats
  └── Cargo.toml

Key dependencies:
  clap        → CLI
  serde_yaml  → .tldf parser
  serde       → deserialization
  fnv         → FNV-64 hash for archive symbol index
  memmap2     → memory-mapped file I/O for large archives
```

---

## 16. Wolf3D Build Sequence

Complete build sequence for Wolf3D PoC:

```bash
# Step 1: Assemble all modules
tsk-asm -I include/ -D WOLFENSTEIN src/wolf3d_main.tsk    -o obj/wolf3d_main.tobj
tsk-asm -I include/ -D WOLFENSTEIN src/wolf3d_render.tsk  -o obj/wolf3d_render.tobj
tsk-asm -I include/ -D WOLFENSTEIN src/wolf3d_map.tsk     -o obj/wolf3d_map.tobj
tsk-asm -I include/ -D WOLFENSTEIN src/wolf3d_act.tsk     -o obj/wolf3d_act.tobj

# Step 2: Build static archive (libc stub)
tsk-asm lib/malloc.tsk  -o obj/malloc.tobj
tsk-asm lib/string.tsk  -o obj/string.tobj
tsk-asm lib/stdlib.tsk  -o obj/stdlib.tobj
tsk-link obj/malloc.tobj obj/string.tobj obj/stdlib.tobj \
         --type archive -o lib/libc_stub.tva

# Step 3: Build SDL2 bindings library
tsk-asm -I include/ bindings/sdl2.tsk -o obj/sdl2.tobj
tsk-link obj/sdl2.tobj --type library -o lib/sdl2.tvl

# Step 4: Link final executable
tsk-link \
  obj/wolf3d_main.tobj   \
  obj/wolf3d_render.tobj \
  obj/wolf3d_map.tobj    \
  obj/wolf3d_act.tobj    \
  lib/sdl2.tvl           \
  lib/libc_stub.tva      \
  --raw-asset assets/walls.bin:TEXTURE   \
  --raw-asset assets/sprites.bin:TEXTURE \
  --raw-asset assets/E1M1.map:MAP        \
  --entry main                           \
  --map wolf3d.tmap                      \
  --debug                                \
  -o wolf3d.tvx

# Step 5: Verify
tsk-dis --stats wolf3d.tvx
tsk-dis --mode tscg --m3-stats wolf3d.tvx

# Step 6: Run
triskele-vm wolf3d.tvx
```

Or equivalently with `tsk-build`:

```bash
tsk-build wolf3d.tyml         # steps 1-4 automated
tsk-build wolf3d.tyml run     # + step 6
tsk-build wolf3d.tyml debug   # + DAP server for VS Code
```

---

*TriskeleToolchain — tsk-link Specification v0.1.0*  
*Echopraxium with the collaboration of Claude AI — 2026-05-30*
