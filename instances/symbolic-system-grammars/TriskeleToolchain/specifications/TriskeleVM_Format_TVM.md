# TriskeleVM — Format `.tvm` Specification

**Author**: Echopraxium with the collaboration of Claude AI  
**Version**: 0.1.0  
**Date**: 2026-05-30  
**Status**: Draft — TriskeleToolchain

---

## 1. Overview

A `.tvm` file is the binary format produced by `tsk-asm` and `tsk-cc`,
consumed by `tsk-link` and the TriskeleVM runtime.

All structural metadata is encoded in **Base16 Triskele** (the 16 M3
monoidal primitives). Raw binary assets (textures, sounds, DLLs) are
stored as-is in a dedicated raw section.

```
.tvm file = Base16 Triskele header
          + Base16 Triskele sections (code, data, symbols, metadata)
          + Raw binary section (assets — optional)
```

---

## 2. Base16 Triskele Encoding

Each nibble (4 bits) maps to one M3 primitive:

```
Hex   Symbol  Monoid   Semantic role
0x0   A        Gt      Attractor
0x1   S        Gt      Structure
0x2   F        Gt      Flow
0x3   It       Gt      Information
0x4   D        Gt      Dynamics
0x5   R        Gm      Representability
0x6   E        Gm      Evolvability
0x7   V        Gm      Verifiability
0x8   O        Gm      Observability
0x9   Im       Gm      Interoperability
0xA   T        Gs      Time
0xB   _^       Gs      Positive Pole
0xC   _$       Gs      Negative Pole
0xD   K        Gs      Knowledge
0xE   Ss       Gs      Symbol
0xF   L        Gs      Localizability
```

A 32-bit value `0x1A3F` reads as `S · T · It · L` —
Structure · Time · Information · Localizability.

---

## 3. File Layout

```
Offset    Size     Encoding        Field
------    ----     --------        -----
0x00      4        ASCII           Magic: "TSKV"
0x04      4        Base16 Triskele Version (major.minor.patch.build)
0x08      4        Base16 Triskele Flags
0x0C      4        Base16 Triskele Section count (N)
0x10      4        Base16 Triskele Entry point (section index)
0x14      4        Base16 Triskele Entry offset within code section
0x18      8        Base16 Triskele Timestamp (Unix epoch)
0x20      32       Base16 Triskele Reserved (future use)
0x40      N×32     Base16 Triskele Section table (N entries)
0x40+N×32 ...      Mixed           Section data
...       ...      Raw binary      Raw asset section (optional, last)
```

**Total header size**: 0x40 + N×32 bytes

---

## 4. Magic & Version

```
Magic: 54 53 4B 56  →  "TSKV"
  T = Triskele
  S = System
  K = Knowledge  (Gs primitive K)
  V = VM

Version field (4 bytes, Base16 Triskele):
  Byte 0 : major  (e.g. 0x00 = version 0)
  Byte 1 : minor  (e.g. 0x01 = minor 1)
  Byte 2 : patch  (e.g. 0x00 = patch 0)
  Byte 3 : build  (e.g. 0x00 = build 0)
```

---

## 5. Flags (4 bytes, Base16 Triskele)

```
Bit 0   : has_debug_info     (O_ sections present)
Bit 1   : has_symbol_table   (Ss_ section present)
Bit 2   : has_raw_assets     (raw binary section present)
Bit 3   : is_library         (linkable module, no entry point)
Bit 4   : is_position_indep  (PIC — position independent code)
Bit 5   : has_gc_metadata    (GC roots table present)
Bit 6   : has_tscg_annot     (TSCG semantic annotations present)
Bit 7   : has_exceptions     (unwind tables present)
Bits 8-31 : reserved
```

---

## 6. Section Table Entry (32 bytes, Base16 Triskele)

```
Offset  Size  Field
0x00    4     Section type  (see §7)
0x04    4     Section flags (readable/writable/executable)
0x08    8     Section offset in file (from file start)
0x10    8     Section size in bytes
0x18    4     Section alignment (power of 2)
0x1C    4     TSCG M3 tag (dominant primitive — semantic annotation)
```

**Section flags**:
```
Bit 0 : readable
Bit 1 : writable
Bit 2 : executable
Bit 3 : Base16 Triskele encoded (vs raw binary)
Bit 4 : compressed (future)
```

**TSCG M3 tag** — encodes the dominant M3 primitive of the section:
```
0x02  (F)   → code section      (Flow — computation)
0x01  (S)   → data section      (Structure — data)
0x0E  (Ss)  → symbol table      (Symbol — names)
0x08  (O)   → debug section     (Observability)
0x0D  (K)   → metadata section  (Knowledge)
0x0F  (L)   → relocation table  (Localizability)
0xFF        → raw binary assets  (no M3 tag)
```

---

## 7. Section Types

```
Type    Name          Encoding        Description
0x01    .code         Base16 Triskele Executable bytecode
0x02    .data         Base16 Triskele Initialized global data
0x03    .rodata       Base16 Triskele Read-only constants
                                      (lookup tables, strings)
0x04    .bss          Base16 Triskele Uninitialized data
                                      (size only, no content)
0x05    .symtab       Base16 Triskele Symbol table
0x06    .strtab       Base16 Triskele String table (names)
0x07    .reltab       Base16 Triskele Relocation table
0x08    .debug        Base16 Triskele Debug information
0x09    .tscg         Base16 Triskele TSCG semantic annotations
                                      (M2 GenericConcept tags)
0x0A    .gc_roots     Base16 Triskele GC roots table
0x0B    .unwind       Base16 Triskele Exception unwind tables
0x0C    .import       Base16 Triskele FFI import declarations
0x0D    .export       Base16 Triskele Exported symbols
0xFF    .raw          Raw binary      Binary assets
                                      (textures, sounds, DLLs)
```

---

## 8. Instruction Format (32 bits fixed)

Register-based, inspired by LuaVM + ARM64.

### Type R — Register to Register

```
Bits 31-24 : opcode    (8 bits — 256 opcodes)
Bits 23-19 : reg_dst   (5 bits — 32 registers)
Bits 18-14 : reg_src1  (5 bits)
Bits 13-09 : reg_src2  (5 bits)
Bits 08-00 : flags/ext (9 bits)
```

### Type I — Immediate (19-bit signed)

```
Bits 31-24 : opcode    (8 bits)
Bits 23-19 : reg_dst   (5 bits)
Bits 18-00 : imm19     (19 bits signed — ±256K)
```

### Type J — Jump (24-bit signed offset)

```
Bits 31-24 : opcode    (8 bits)
Bits 23-00 : offset24  (24 bits signed — ±8MB relative)
```

### Type X — Extended (64-bit constant via constant pool)

```
Instruction 1:  Type I  — L_GLOB reg, pool_index
Instruction 2:  (pool entry at index — 8 bytes in .rodata)
```

---

## 9. Register File

```
Name    Index   Role                    Save convention
R0      0       Return value / arg 0    caller-saved
R1      1       Arg 1                   caller-saved
R2      2       Arg 2                   caller-saved
R3      3       Arg 3                   caller-saved
R4      4       Arg 4                   caller-saved
R5      5       Arg 5                   caller-saved
R6      6       Arg 6                   caller-saved
R7      7       Arg 7                   caller-saved
R8-R15  8-15    Temporaries             caller-saved
R16-R23 16-23   Local variables         callee-saved
R24     24      VM internal 0           reserved
R25     25      VM internal 1           reserved
R26     26      VM internal 2           reserved
R27     27      VM internal 3           reserved
R28     28      Frame Pointer (FP)      callee-saved
R29     29      Stack Pointer (SP)      callee-saved
R30     30      Link Register (LR)      caller-saved
R31     31      Program Counter (PC)    special
```

All registers are **64-bit** wide.
32-bit operations zero-extend the upper 32 bits.

---

## 10. Calling Convention (C-compatible ABI)

```
Arguments       R0–R7 (first 8 args)
                Stack beyond 8 args (right-to-left push)
Return value    R0 (scalar), R0+R1 (128-bit)
Caller saves    R0–R15, R30 (LR)
Callee saves    R16–R28 (FP)
Stack           Full descending, 16-byte aligned at call
Frame layout:
  [SP+0]        saved LR
  [SP+8]        saved FP
  [SP+16..]     local variables
```

**FFI (C native call via Im_FFI_CALL)**:
```
Maps directly to C cdecl / System V AMD64 ABI
  Integer args : R0–R7 → RDI, RSI, RDX, RCX, R8, R9 (x86_64)
  Float args   : passed via float registers (VM marshals)
  Return       : R0 ← RAX
```

---

## 11. Symbol Table Entry (32 bytes, Base16 Triskele)

```
Offset  Size  Field
0x00    8     Symbol value (address or constant)
0x08    4     Symbol size (bytes)
0x0C    4     Name offset in .strtab
0x10    1     Symbol type (function/object/section/file)
0x11    1     Symbol binding (local/global/weak)
0x12    1     Symbol visibility (default/hidden/protected)
0x13    1     Section index
0x14    4     TSCG M2 tag (GenericConcept IRI hash — optional)
0x18    8     Reserved
```

**TSCG M2 tag** — identifies the dominant M2 GenericConcept
of the symbol (e.g. `m2:Process`, `m2:Attractor`, `m2:Channel`).
Used by `tsk-dbg` and the VS Code plugin for semantic hover.

---

## 12. Relocation Table Entry (16 bytes, Base16 Triskele)

```
Offset  Size  Field
0x00    8     Relocation offset (in section)
0x08    4     Symbol index (in .symtab)
0x0C    2     Relocation type
0x0E    2     Addend
```

**Relocation types**:
```
0x01  R_TSK_ABS32    absolute 32-bit address
0x02  R_TSK_ABS64    absolute 64-bit address
0x03  R_TSK_REL24    PC-relative 24-bit (Type J instructions)
0x04  R_TSK_REL19    PC-relative 19-bit (Type I branches)
0x05  R_TSK_POOL     constant pool reference (Type X)
0x06  R_TSK_FFI      FFI symbol (resolved at load time via dlsym)
```

---

## 13. TSCG Annotation Section (.tscg)

Unique to TriskeleVM — no equivalent in JVM/CLR/LuaVM.

Each entry annotates a code range with TSCG semantic metadata:

```
Offset  Size  Field
0x00    8     Start offset in .code section
0x08    8     End offset in .code section
0x10    4     M3 dominant primitive (opcode category)
0x14    4     M2 GenericConcept IRI hash
0x18    8     Human-readable label offset in .strtab
0x20    8     Reserved
```

**Example** (Wolf3D raycaster inner loop):
```
Start   : 0x00401000
End     : 0x00401080
M3 tag  : 0x02 (F — Flow)
M2 tag  : hash("m2:Process")
Label   : "raycast_column_render"
```

The VS Code plugin uses this section to display:
```
Hover on instruction 0x00401040:
  ┌─────────────────────────────────────┐
  │ raycast_column_render               │
  │ M3 : F (Flow) — computation loop   │
  │ M2 : Process = D × It × F          │
  │ Opcode : F_FIXMUL (0x2D)           │
  └─────────────────────────────────────┘
```

---

## 14. Raw Asset Section (.raw)

Always the **last section** in the file.

```
Offset  Size  Field
0x00    4     Magic: "RRAW"
0x04    4     Asset count (N)
0x08    N×48  Asset directory (48 bytes per entry)
...     ...   Asset data (raw binary, concatenated)
```

**Asset directory entry (48 bytes)**:
```
Offset  Size  Field
0x00    4     Asset type (texture/sound/dll/font/map)
0x04    4     Asset flags
0x08    8     Data offset (from .raw section start)
0x10    8     Data size (bytes)
0x18    4     Name offset in .strtab
0x1C    4     TSCG M3 tag (dominant primitive)
0x20    16    Reserved
```

**Asset types**:
```
0x01  TEXTURE   raw RGB/RGBA pixels
0x02  SOUND     PCM audio (future)
0x03  MAP       game map data (Wolf3D/Doom format)
0x04  FONT      bitmap font
0x05  DLL       native shared library (SDL2, libc...)
0x06  JSON_LD   TSCG ontology fragment
```

---

## 15. File Format Summary

```
[0x00]  Magic "TSKV"
[0x04]  Version (Base16 Triskele)
[0x08]  Flags   (Base16 Triskele)
[0x0C]  Section count
[0x10]  Entry point section index
[0x14]  Entry point offset
[0x18]  Timestamp
[0x20]  Reserved (32 bytes)
[0x40]  Section table (N × 32 bytes)
        ├── .code    (Base16 Triskele bytecode)
        ├── .rodata  (Base16 Triskele constants)
        ├── .data    (Base16 Triskele globals)
        ├── .bss     (size descriptor only)
        ├── .symtab  (Base16 Triskele symbol table)
        ├── .strtab  (Base16 Triskele string table)
        ├── .reltab  (Base16 Triskele relocations)
        ├── .tscg    (Base16 Triskele TSCG annotations)
        ├── .import  (Base16 Triskele FFI declarations)
        ├── .debug   (Base16 Triskele debug info — optional)
        └── .raw     (raw binary assets — optional, last)
```

---

## 16. Toolchain Responsibilities

```
tsk-asm   → produces .tvm with .code, .symtab, .strtab, .reltab
tsk-cc    → produces .tvm with all sections except .raw
tsk-link  → merges multiple .tvm → final .tvm
             resolves relocations
             generates .import for FFI (SDL2, libc)
tsk-dis   → reads .tvm → human-readable assembly
             displays Base16 Triskele with M3 semantics
tsk-dbg   → reads .tvm .debug + .tscg sections
             DAP server for VS Code plugin
TriskeleVM→ loads and executes final .tvm
             resolves .raw assets at startup
             calls dlopen for .DLL assets (SDL2)
```

---

*TriskeleToolchain — Format Specification v0.1.0*  
*Echopraxium with the collaboration of Claude AI — 2026-05-30*
