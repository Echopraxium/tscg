# tsk-asm — Triskele Assembler Specification

**Author**: Echopraxium with the collaboration of Claude AI  
**Version**: 0.1.0  
**Date**: 2026-05-30  
**Status**: Draft — TriskeleToolchain  
**Source extension**: `.tsk`  
**Output extension**: `.tobj` (object file, linkable)

---

## 1. Overview

`tsk-asm` is the assembler for TriskeleVM. It translates `.tsk` source files
into `.tobj` object files consumed by `tsk-link`.

Design principles:
- **One pass + fixup** — labels resolved in a second pass
- **Base16 Triskele** — all numeric constants expressed in M3 primitives
- **TSCG-aware** — directives for semantic annotation (M2 GenericConcepts)
- **C-preprocessor subset** — `#define`, `#include`, `#ifdef` familiar to C developers
- **Readable** — mnemonic names derived from M3 primitive semantics

---

## 2. File Structure

A `.tsk` file is divided into ordered sections:

```
; ── File header comment (optional) ─────────────────────────
; my_module.tsk
; Description: ...
; Author: ...

; ── Preprocessor directives ─────────────────────────────────
#include  "path/to/file.tsk"
#define   SYMBOL  value

; ── Module declaration ───────────────────────────────────────
.module   my_module
.type     executable          ; executable | library | archive

; ── Imports (FFI / external symbols) ─────────────────────────
.import   SDL_Init      ffi:"SDL2"   sig:SIG_INT_INT
.import   malloc        ffi:"libc"   sig:SIG_PTR_INT
.extern   other_func               ; symbol defined in another .tobj

; ── Exports ──────────────────────────────────────────────────
.export   main
.export   my_public_func

; ── Data sections ────────────────────────────────────────────
.section  .rodata
.section  .data
.section  .bss

; ── Code section ─────────────────────────────────────────────
.section  .code
.entry    main             ; entry point (executables only)

; ── TSCG annotation (optional) ───────────────────────────────
.tscg     m2:Process  "main execution loop"
```

---

## 3. Syntax Rules

### 3.1 General

```
- Case-sensitive mnemonics (uppercase opcodes, lowercase directives)
- One statement per line
- Whitespace: spaces or tabs as separators
- Comments: semicolon (;) to end of line
- Labels: identifier followed by colon (:)
- Strings: double-quoted ("hello\n")
- Characters: single-quoted ('A')
- Line continuation: backslash (\) at end of line (not in strings)
```

### 3.2 Identifiers

```
[A-Za-z_][A-Za-z0-9_]*

Valid:   main  my_func  WOLF3D_WIDTH  _internal
Invalid: 3d_func  my-func  $ptr
```

### 3.3 Numeric Literals

Three formats — all ultimately encoded as Base16 Triskele in the binary:

```
; Decimal (human-friendly)
320
-1
3_200_000          ; underscores allowed for readability

; Hexadecimal (standard — maps directly to Base16 Triskele)
0x140              ; = 320
0xFF
0x1_A3_F0          ; underscores allowed

; Base16 Triskele (native — explicit M3 primitive sequence)
#S_A_A             ; S=0x1, A=0x0, A=0x0 → 0x100 = 256
#F_A               ; F=0x2, A=0x0         → 0x20  = 32
#L_Im_A_A          ; L=0xF, Im=0x9, A=0x0, A=0x0 → 0xF900
```

**Base16 Triskele literal syntax**: `#` followed by primitive names separated by `_`

```
Primitives:  A  S  F  It  D  R  E  V  O  Im  T  POS  NEG  K  Ss  L
Hex values:  0  1  2   3  4  5  6  7  8   9  A    B    C  D   E  F
```

### 3.4 Registers

```
R0  .. R31          ; general registers (case-insensitive: r0 = R0)
FP                  ; alias for R28 (Frame Pointer)
SP                  ; alias for R29 (Stack Pointer)
LR                  ; alias for R30 (Link Register)
PC                  ; alias for R31 (Program Counter)
```

### 3.5 Labels

```
; Local label (visible in current file only)
my_label:
    A_JMP  my_label

; Global label (visible after .export)
.export  public_func
public_func:
    ...

; Anonymous labels (forward/backward reference)
@@:                 ; define anonymous label
    A_JMP  @f       ; jump to next @@ (forward)
    A_JMP  @b       ; jump to previous @@ (backward)
```

### 3.6 Expressions

```
; Arithmetic in operands (evaluated at assembly time)
D_MOV_I  R0, (320 * 200)         ; = 64000
D_MOV_I  R1, (SCREEN_W - 1)      ; uses #define
D_MOV_I  R2, (0x1000 + offset)

; Operators: + - * / % << >> & | ~ ( )
; All evaluated as 64-bit integers at assembly time
```

---

## 4. Preprocessor Directives

### 4.1 `#include`

```asm
#include "path/to/file.tsk"      ; relative to current file
#include <stdlib.tsk>            ; from include path (tsk-asm -I)
```

Textual inclusion before assembly. Circular includes detected and rejected.

### 4.2 `#define`

```asm
; Simple constant
#define  SCREEN_W      320
#define  SCREEN_H      200
#define  FPS_TARGET    35
#define  FIXED_SHIFT   16
#define  FIXED_ONE     0x10000

; Expression
#define  SCREEN_PIXELS  (SCREEN_W * SCREEN_H)

; String constant
#define  VERSION_STR   "0.1.0"

; Base16 Triskele constant
#define  FLOW_TAG      #F_A       ; 0x20 — Flow category marker

; Macro with arguments
#define  ALIGN(x, n)   (((x) + (n) - 1) & ~((n) - 1))
#define  MIN(a, b)     ((a) < (b) ? (a) : (b))
#define  MAX(a, b)     ((a) > (b) ? (a) : (b))
#define  ABS(x)        ((x) < 0 ? -(x) : (x))

; Undefine
#undef   SCREEN_W
```

### 4.3 Conditional Compilation

```asm
#ifdef   WOLFENSTEIN
  #define  MAP_W  64
  #define  MAP_H  64
#endif

#ifndef  DEBUG
  #define  NDEBUG
#endif

#if  FPS_TARGET == 35
  ; Wolf3D timing
#elif  FPS_TARGET == 60
  ; modern timing
#else
  #error "Unsupported FPS_TARGET"
#endif

; Nesting supported up to 16 levels
```

### 4.4 `#error` / `#warning`

```asm
#if SCREEN_W > 1920
  #error "Screen width exceeds maximum supported resolution"
#endif

#ifndef SDL2_BINDINGS
  #warning "SDL2 bindings not included — display will not work"
#endif
```

### 4.5 Predefined Macros

```asm
__FILE__        ; current filename (string)
__LINE__        ; current line number (integer)
__DATE__        ; assembly date "2026-05-30" (string)
__VERSION__     ; tsk-asm version "0.1.0" (string)
__TRISKELE__    ; always defined — identifies TriskeleVM target
__BASE16__      ; always defined — Base16 Triskele encoding active
__TSCG__        ; always defined — TSCG annotations available
```

---

## 5. Module Directives

### 5.1 `.module`

```asm
.module  wolf3d_render
; Declares the module name (used in .symtab, linker messages)
; Must be the first non-comment, non-preprocessor line
```

### 5.2 `.type`

```asm
.type  executable    ; produces .tvx when linked as main module
.type  library       ; produces .tvl (shared library)
.type  archive       ; produces .tva (static archive)
.type  object        ; produces .tobj only (default)
```

### 5.3 `.entry`

```asm
.entry  main         ; declares entry point for executable
                     ; tsk-link uses this for .tvx header
```

---

## 6. Import / Export Directives

### 6.1 `.import` — FFI declarations

```asm
; Native C function via Im_FFI_CALL
.import  SDL_Init          ffi:"SDL2"    sig:SIG_INT_INT
.import  SDL_CreateWindow  ffi:"SDL2"    sig:SIG_PTR_PTR_INT_INT_INT_INT_INT
.import  SDL_PollEvent     ffi:"SDL2"    sig:SIG_INT_PTR
.import  SDL_RenderPresent ffi:"SDL2"    sig:SIG_VOID_PTR
.import  SDL_Quit          ffi:"SDL2"    sig:SIG_VOID_VOID

; Triskele function from another .tobj (resolved by linker)
.extern  game_update
.extern  game_render
.extern  math_fixmul
```

**Signature identifiers** (sig:):

```asm
SIG_VOID_VOID          void f(void)
SIG_INT_VOID           void f(int)
SIG_PTR_VOID           void f(ptr)
SIG_INT_INT            int  f(int)
SIG_PTR_INT            int  f(ptr)
SIG_PTR_PTR            ptr  f(ptr)
SIG_INT_INT_VOID       void f(int, int)
SIG_PTR_INT_INT_VOID   void f(ptr, int, int)
SIG_PTR_PTR_INT_INT_INT_INT_INT  ; SDL_CreateWindow
SIG_VARIADIC           variadic (resolved at runtime)
```

### 6.2 `.export`

```asm
.export  main              ; visible to linker as global symbol
.export  render_frame
.export  update_game
```

### 6.3 `.callback` — SDL2 event callbacks

```asm
; Declares a function as callable from C via Im_REGISTER_CB
.callback  handle_keydown  event:SDL_KEYDOWN  sig:SIG_PTR_VOID
.callback  handle_quit     event:SDL_QUIT     sig:SIG_VOID_VOID
```

---

## 7. Section Directives

### 7.1 `.section`

```asm
.section  .code          ; executable instructions
.section  .rodata        ; read-only constants (lookup tables, strings)
.section  .data          ; initialized read-write globals
.section  .bss           ; uninitialized globals (zero-initialized)
```

Default section if none declared: `.code`

### 7.2 `.align`

```asm
.align  4                ; align to 4-byte boundary
.align  16               ; align to 16-byte boundary (SIMD future)
; Inserts NOP padding in .code, zero bytes elsewhere
```

### 7.3 `.org`

```asm
.org  0x1000             ; set current address (rare — linker usually handles)
```

---

## 8. Data Definition Directives

All data emitted into the current section (`.rodata`, `.data`, or `.bss`).

### 8.1 Scalar types

```asm
.db   0x41               ; 1 byte  (define byte)
.dw   0x1234             ; 2 bytes (define word, little-endian)
.dd   0x12345678         ; 4 bytes (define dword)
.dq   0x123456789ABCDEF0 ; 8 bytes (define qword)

; Base16 Triskele encoding
.db   #F_A               ; 1 byte = 0x20
.dd   #S_A_A_A           ; 4 bytes = 0x01000000 (big-endian notation)

; Expressions
.dd   (SCREEN_W * SCREEN_H * 3)   ; framebuffer size RGB
```

### 8.2 Strings

```asm
.str   "Hello, Triskele!\n"    ; null-terminated string
.strn  "Wolf3D"                ; NOT null-terminated (raw bytes)
.stru  "élément"               ; UTF-8 string

; Multi-line string
.str   "Line 1\n"  \
        "Line 2\n"  \
        "Line 3\n"
```

### 8.3 Arrays

```asm
; Typed array
.arr  .dd  64  0x00            ; 64 dwords initialized to 0
.arr  .db  320 * 200  0x00     ; framebuffer 320×200, zeroed

; Initialized array (inline values)
.arr  .db  { 0x01, 0x02, 0x03, 0x04 }

; Lookup table (Wolf3D cosine table example)
cos_table:
.arr  .dd  { 0x10000, 0xFF62, 0xFD88, 0xFA80 }  ; 16.16 fixed-point
```

### 8.4 Structs

```asm
; Struct layout declaration (no memory allocated)
.struct  SDL_Rect
  .field  x   .dd
  .field  y   .dd
  .field  w   .dd
  .field  h   .dd
.endstruct
; SDL_Rect.size = 16, SDL_Rect.x = 0, SDL_Rect.y = 4...

; Allocate struct instance
my_rect:
.dd  0        ; x
.dd  0        ; y
.dd  320      ; w
.dd  200      ; h

; Access via field offset
D_MOV_I  R0, my_rect
F_ADD_I  R0, SDL_Rect.w    ; R0 = &my_rect.w
S_LOAD32 R1, R0, 0         ; R1 = my_rect.w
```

### 8.5 BSS (uninitialized)

```asm
.section  .bss

framebuffer:
.res  .db  (320 * 200 * 4)    ; reserve 256000 bytes (RGBA)

map_data:
.res  .dd  (64 * 64)          ; Wolf3D map 64×64

player_state:
.res  .db  64                 ; player struct, 64 bytes
```

---

## 9. Type System Directives

### 9.1 `.typedef`

```asm
; Primitive type aliases
.typedef  int8    .db
.typedef  int16   .dw
.typedef  int32   .dd
.typedef  int64   .dq
.typedef  ptr     .dq          ; 64-bit pointer
.typedef  fixed   .dd          ; 16.16 fixed-point

; Usage
player_x:   fixed  0x00280000  ; 40.0 in 16.16
player_y:   fixed  0x00280000
```

### 9.2 `.enum`

```asm
.enum  GameState
  GS_MENU      = 0
  GS_PLAYING   = 1
  GS_PAUSED    = 2
  GS_GAMEOVER  = 3
.endenum

; Usage
D_MOV_I  R0, GS_PLAYING
V_CMP    R0, R1
A_JZ     @handle_playing
```

### 9.3 `.const`

```asm
; Typed named constant (stronger than #define — has type info)
.const  int32   SCREEN_W       320
.const  int32   SCREEN_H       200
.const  fixed   PLAYER_SPEED   0x00028000   ; 2.5 in 16.16
.const  ptr     NULL           0x00000000
```

---

## 10. Code Directives

### 10.1 `.proc` / `.endproc`

```asm
; Procedure declaration with metadata
.proc  render_frame
  .tscg   m2:Process  "main render loop — F × It × D"
  .locals  4           ; 4 local variable slots (× 8 bytes = 32 bytes)
  .args    0           ; 0 arguments

  ; prologue generated automatically by tsk-asm:
  ;   S_PUSH  LR
  ;   S_PUSH  FP
  ;   D_MOV   FP, SP
  ;   F_SUB_I SP, 32      ; locals space

  ; ... procedure body ...

  ; epilogue generated automatically:
  ;   D_MOV   SP, FP
  ;   S_POP   FP
  ;   S_POP   LR
  ;   A_RET
.endproc
```

### 10.2 `.macro` / `.endmacro`

```asm
; Parameterized code macro
.macro  LOAD_FIXED_ADDR  reg, label
  L_GLOB  \reg, @\label
.endmacro

; Multi-instruction macro
.macro  CALL_SDL  func_name
  D_MOV_I   R8, \func_name   ; load FFI symbol
  Im_FFI_CALL R8
.endmacro

; Usage
  LOAD_FIXED_ADDR  R0, cos_table
  CALL_SDL  SDL_RenderPresent

; Inline macro (no label pollution)
.macro  FIXMUL  dst, a, b
  D_MOV    R24, \a
  D_MOV    R25, \b
  F_FIXMUL \dst, R24, R25
.endmacro
```

### 10.3 `.inline`

```asm
; Mark procedure as inline candidate for tsk-cc optimizer (future)
.proc  fast_abs
  .inline
  ; ...
.endproc
```

---

## 11. TSCG Semantic Directives

Unique to TriskeleToolchain — no equivalent in standard assemblers.
These directives populate the `.tscg` annotation section in the `.tobj`.

### 11.1 `.tscg`

```asm
; Annotate next instruction or label with M2 GenericConcept
.tscg  m2:Process       "raycaster inner loop"
.tscg  m2:Homeostasis   "frame rate control — T_FRAME_SYN"
.tscg  m2:Channel       "SDL2 FFI bridge — Im_FFI_CALL"
.tscg  m2:Attractor     "game loop convergence point"
.tscg  m2:Structure     "framebuffer layout"
```

### 11.2 `.tscg_block` / `.endtscg_block`

```asm
; Annotate a range of instructions
.tscg_block  m2:Process  "ray casting — F × It × D"
  ; ... raycasting instructions ...
.endtscg_block
```

### 11.3 `.m3tag`

```asm
; Explicit M3 primitive tag (overrides auto-detection from opcode)
.m3tag  F                ; Flow — computation section
.m3tag  Im               ; Interoperability — FFI section
.m3tag  T                ; Time — timing section
```

---

## 12. Instruction Syntax

### 12.1 General form

```asm
[label:]  OPCODE  [operand1 [, operand2 [, operand3]]]  [; comment]
```

### 12.2 Type R — Register operations

```asm
; dst = src1 op src2
F_ADD    R0, R1, R2        ; R0 = R1 + R2
F_MUL    R3, R4, R5        ; R3 = R4 * R5
F_FIXMUL R0, R1, R2        ; R0 = (R1 * R2) >> 16
It_AND   R0, R1, R2        ; R0 = R1 & R2
It_SHL   R0, R1, R2        ; R0 = R1 << R2
D_MOV    R0, R1             ; R0 = R1
```

### 12.3 Type I — Immediate operand

```asm
; dst = src op immediate
D_MOV_I   R0, 320              ; R0 = 320
D_MOV_I   R0, SCREEN_W        ; R0 = #define value
D_MOV_I   R0, 0xFF            ; R0 = 255
D_MOV_I   R0, #F_A            ; R0 = 0x20 (Base16 Triskele)
F_ADD_I   R0, 1               ; R0 = R0 + 1
It_AND_I  R0, 0x0F            ; R0 = R0 & 0x0F
```

### 12.4 Type J — Jumps and calls

```asm
; Labels
A_JMP    game_loop             ; unconditional jump
A_JMP    @f                   ; jump forward to next @@
A_JMP    @b                   ; jump backward to previous @@
A_CALL   render_frame          ; call procedure
A_RET                          ; return

; Conditional jumps (use flags set by V_CMP)
V_CMP    R0, R1                ; compare R0 and R1 → flags
A_JZ     equal_branch          ; jump if zero (R0 == R1)
A_JNZ    not_equal_branch      ; jump if not zero
A_JL     less_branch           ; jump if less (signed)
A_JGE    ge_branch             ; jump if >= (signed)

; Register indirect jump
A_JMP_R  R0                   ; jump to address in R0 (SWITCH table)
```

### 12.5 Memory access

```asm
; Load
S_LOAD8   R0, R1, 0           ; R0 = mem8[R1 + 0]
S_LOAD16  R0, R1, 4           ; R0 = mem16[R1 + 4]
S_LOAD32  R0, R1, 8           ; R0 = mem32[R1 + 8]
S_LOAD64  R0, R1, 0           ; R0 = mem64[R1 + 0]

; Store
S_STORE8  R0, R1, 0           ; mem8[R1 + 0] = R0
S_STORE32 R0, R1, 8           ; mem32[R1 + 8] = R0

; Global variable
L_GLOB   R0, player_x         ; R0 = address of player_x
S_LOAD32 R1, R0, 0            ; R1 = player_x value

; Stack operations
S_PUSH   R0                   ; push R0 onto stack
S_POP    R1                   ; pop from stack into R1
S_PUSH_I 320                  ; push immediate

; Memory operations (Wolf3D critical)
S_MEMCPY R0, R1, R2           ; memcpy(R0, R1, R2)
S_MEMSET R0, R2, R3           ; memset(R0, R2, R3) — R2=value
```

### 12.6 FFI and syscalls

```asm
; Call imported C function
; (symbol must be declared with .import)
D_MOV_I   R0, SDL_INIT_VIDEO
Im_FFI_CALL SDL_Init           ; SDL_Init(SDL_INIT_VIDEO)
V_CMP     R0, 0
A_JL      sdl_init_failed

; Register SDL2 event callback
D_MOV_I   R0, SDL_KEYDOWN      ; event id
L_GLOB    R1, handle_keydown   ; VM function address
D_MOV_I   R2, SIG_PTR_VOID    ; signature
Im_REGISTER_CB

; Blit framebuffer (Wolf3D critical)
L_GLOB    R0, framebuffer      ; framebuffer ptr
D_MOV_I   R1, SCREEN_W
D_MOV_I   R2, SCREEN_H
Im_FB_BLIT                     ; display frame
```

### 12.7 Timing (Wolf3D 35fps)

```asm
; Frame synchronization
D_MOV_I   R0, FPS_TARGET       ; 35
T_FRAME_SYN R0                  ; wait until next frame slot

; Timer
T_TICK    R0                   ; R0 = current tick count
T_DELTA   R1, R0               ; R1 = ticks since last call
```

---

## 13. Complete Example — Wolf3D Main Loop

```asm
; wolf3d_main.tsk
; Wolf3D main module — TriskeleVM PoC
; Author: Echopraxium with the collaboration of Claude AI

;; ─── Preprocessor ────────────────────────────────────────────
#include  <sdl2.tsk>
#include  <libc.tsk>
#include  "wolf3d_defs.tsk"

#define  SCREEN_W     320
#define  SCREEN_H     200
#define  FPS_TARGET   35
#define  MAP_W        64
#define  MAP_H        64

;; ─── Module ───────────────────────────────────────────────────
.module  wolf3d_main
.type    executable
.entry   main

;; ─── Imports ──────────────────────────────────────────────────
.import  SDL_Init          ffi:"SDL2"  sig:SIG_INT_INT
.import  SDL_CreateWindow  ffi:"SDL2"  sig:SIG_PTR_PTR_INT_INT_INT_INT_INT
.import  SDL_PollEvent     ffi:"SDL2"  sig:SIG_INT_PTR
.import  SDL_Quit          ffi:"SDL2"  sig:SIG_VOID_VOID

;; ─── Exports ──────────────────────────────────────────────────
.export  main

;; ─── Callbacks ────────────────────────────────────────────────
.callback  handle_keydown  event:SDL_KEYDOWN  sig:SIG_PTR_VOID
.callback  handle_quit     event:SDL_QUIT     sig:SIG_VOID_VOID

;; ─── Constants ────────────────────────────────────────────────
.section  .rodata
.align    4

window_title:
.str      "Wolfenstein 3D — TriskeleVM"

;; ─── BSS (uninitialized) ──────────────────────────────────────
.section  .bss

framebuffer:
.res  .db  (SCREEN_W * SCREEN_H * 4)  ; RGBA

game_running:
.res  .dd  1

;; ─── Data (initialized) ───────────────────────────────────────
.section  .data

player_x:   .dd  0x00200000   ; 32.0 in 16.16
player_y:   .dd  0x00200000
player_angle: .dd  0x00000000

;; ─── Code ─────────────────────────────────────────────────────
.section  .code

;; ── main ──────────────────────────────────────────────────────
.proc  main
  .tscg   m2:Attractor  "program entry point — system bootstrap"
  .locals  2

  ; Init SDL2
  D_MOV_I   R0, 0x00000020     ; SDL_INIT_VIDEO
  Im_FFI_CALL SDL_Init
  V_CMP     R0, 0
  A_JL      @init_failed

  ; Register event callbacks
  D_MOV_I   R0, SDL_KEYDOWN
  L_GLOB    R1, handle_keydown
  D_MOV_I   R2, SIG_PTR_VOID
  Im_REGISTER_CB

  D_MOV_I   R0, SDL_QUIT
  L_GLOB    R1, handle_quit
  D_MOV_I   R2, SIG_VOID_VOID
  Im_REGISTER_CB

  ; Enter game loop
  A_CALL    game_loop

  ; Cleanup
  Im_FFI_CALL SDL_Quit
  D_MOV_I   R0, 0
  Im_EXIT

@@init_failed:
  D_MOV_I   R0, 1
  Im_EXIT
.endproc

;; ── game_loop ────────────────────────────────────────────────
.proc  game_loop
  .tscg   m2:Homeostasis  "main loop — 35fps steady state"
  .tscg   m2:Attractor    "convergence: running=0 exits loop"

@@:
  ; Poll SDL2 events (dispatches registered callbacks)
  Im_INPUT_RD

  ; Check exit condition
  L_GLOB    R0, game_running
  S_LOAD32  R1, R0, 0
  V_CMP     R1, 0
  A_JZ      @loop_exit

  ; Update game state
  .tscg_block  m2:Process  "game update — D × It × F"
    A_CALL    update_game
  .endtscg_block

  ; Render frame
  .tscg_block  m2:Process  "render — F × It × D"
    A_CALL    render_frame
  .endtscg_block

  ; Blit to screen
  .tscg  m2:Channel  "SDL2 framebuffer blit — Im_FB_BLIT"
  L_GLOB    R0, framebuffer
  D_MOV_I   R1, SCREEN_W
  D_MOV_I   R2, SCREEN_H
  Im_FB_BLIT

  ; Sync to 35fps
  .tscg  m2:Homeostasis  "frame rate regulation"
  D_MOV_I   R0, FPS_TARGET
  T_FRAME_SYN R0

  A_JMP  @b         ; jump to previous @@

@@loop_exit:
.endproc

;; ── handle_keydown ──────────────────────────────────────────
handle_keydown:
  .tscg  m2:Channel  "keyboard event — Im_REGISTER_CB callback"
  ; R0 = SDL_Event* (from SDL2 callback)
  S_LOAD32  R1, R0, 16     ; SDL_Event.key.keysym.sym offset
  D_MOV_I   R2, 0x0000001B ; SDLK_ESCAPE
  V_CMP     R1, R2
  A_JNZ     @keydown_done

  ; ESC pressed — set game_running = 0
  L_GLOB    R3, game_running
  D_CLR     R4
  S_STORE32 R4, R3, 0

@@keydown_done:
  A_RET

;; ── handle_quit ─────────────────────────────────────────────
handle_quit:
  .tscg  m2:Channel  "SDL_QUIT event — Im_REGISTER_CB callback"
  L_GLOB    R0, game_running
  D_CLR     R1
  S_STORE32 R1, R0, 0
  A_RET
```

---

## 14. Assembly Process

```
Input:  wolf3d_main.tsk
        wolf3d_render.tsk
        wolf3d_map.tsk

Step 1: Preprocessor
  → resolve #include, #define, #ifdef
  → expand macros
  → emit expanded .tsk (optional --save-pp flag)

Step 2: Pass 1 — Symbol scan
  → collect all labels → symbol table
  → collect .export, .extern, .import
  → compute section sizes and alignments
  → collect .struct layouts

Step 3: Pass 2 — Code generation
  → emit instructions (32-bit fixed format)
  → encode operands (Base16 Triskele constants)
  → emit relocation entries for forward refs
  → emit .tscg annotation entries
  → emit .import FFI declarations

Step 4: Object file emission
  → write .tobj (format: subset of .tvm)
  → sections: .code, .rodata, .data, .bss,
              .symtab, .strtab, .reltab,
              .tscg, .import

Output: wolf3d_main.tobj
        wolf3d_render.tobj
        wolf3d_map.tobj
  → passed to tsk-link
```

---

## 15. Command-Line Interface

```
tsk-asm [options] <input.tsk> -o <output.tobj>

Options:
  -o <file>           output object file (default: input.tobj)
  -I <dir>            add include search directory
  -D <SYM>[=<val>]    define preprocessor symbol
  -U <SYM>            undefine preprocessor symbol
  --save-pp           save preprocessed output (.tsk.pp)
  --list              generate listing file (.tsk.lst)
  --no-tscg           omit .tscg annotation section
  --base16-strict     reject non-Base16-Triskele numeric literals
  --warn-all          enable all warnings
  --error             treat warnings as errors
  --verbose           verbose output
  --version           print tsk-asm version

Examples:
  tsk-asm wolf3d_main.tsk -o wolf3d_main.tobj
  tsk-asm -I include/ -D WOLFENSTEIN -D DEBUG wolf3d_main.tsk -o out.tobj
  tsk-asm --list --save-pp wolf3d_render.tsk -o wolf3d_render.tobj
```

---

## 16. Listing File Format (`.tsk.lst`)

```
; wolf3d_main.tsk — Assembly Listing
; tsk-asm 0.1.0 — 2026-05-30
; ──────────────────────────────────────────────────────────────

Section: .code
Addr     Encoding    M3   Source
──────── ──────────  ───  ──────────────────────────────────────
00000000 40 00 0020  A    main:
00000000 D1 00 0020  D    D_MOV_I   R0, 0x00000020
00000004 91 00 ????  Im   Im_FFI_CALL SDL_Init     [reloc→SDL_Init]
00000008 70 01 0000  V    V_CMP     R0, 0
0000000C 08 ????     A    A_JL      @init_failed   [reloc]
...

Section: .rodata
Addr     Bytes       Content
──────── ──────────  ──────────────────────────────────────────
00000000 57 6F 6C 66  "Wolf"
00000004 65 6E 73 74  "enst"
...

Symbols:
  main          .code  0x00000000  GLOBAL
  game_loop     .code  0x00000040  GLOBAL
  framebuffer   .bss   0x00000000  LOCAL
  ...

Relocations:
  0x00000004  R_TSK_FFI    SDL_Init
  0x0000000C  R_TSK_REL24  @init_failed
  ...

TSCG Annotations:
  [0x00000000 – 0x00000050]  m2:Attractor   "program entry point"
  [0x00000040 – 0x000000C0]  m2:Homeostasis "main loop — 35fps"
  ...
```

---

*TriskeleToolchain — tsk-asm Specification v0.1.0*  
*Echopraxium with the collaboration of Claude AI — 2026-05-30*
