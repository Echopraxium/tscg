# TriskeleToolchain — Handover v0.3.9
**Date**: 2026-06-11  
**Auteur**: Echopraxium with the collaboration of Claude AI  
**Repo**: https://github.com/Echopraxium/tscg  
**Chemin local**: `E:\_00_Michel\_00_Lab\_00_GitHub\tscg\instances\symbolic-system-grammars\TriskeleToolchain\`

---

## Statut actuel — ✅ OCTUPLE VALIDATION

| Projet | Type | Exit | Statut |
|--------|------|------|--------|
| `test_main` | C89 | 31 | ✅ |
| `wolf3d` | C89 | 15 | ✅ |
| `test_patterns` | C89 | 15 | ✅ |
| `test_select` | C89 | 9 | ✅ |
| `doom_fixed` | C89 | 127 | ✅ |
| `doom_alloc` | C89 | 255 | ✅ |
| `doom_zzone` | C89 | 255 | ✅ |
| **`test_variadic`** | C89 | **255** | ✅ **NOUVEAU** |

> ✅ Validé sur Windows (2026-06-11) avec `run_pipeline.py` v0.3.3 (`--release`).

---

## Changements en v0.3.9

### Tâche 1 — Support complet des fonctions variadiques

**Problèmes résolus (14 bugs) :**

#### tsk-cc/parser.rs
- **`call (ptr,...) @func` (fntype skip)** : syntaxe LLVM variadic mal parsée → le parser skippait `(fntype)` et lisait `@funcname` comme valeur Undef → pas de relocation → fonctions jamais appelées.
- **`linkonce_odr` globals non parsées** : attribut de linkage non reconnu → strings de format (format strings) initialisées à zéro.
- **`GlobalInit::Bytes`** : les initialiseurs `c"%d\n\0"` n'avaient pas de variante dans l'enum → toutes les format strings étaient des buffers zéros → `format_printf` lisait `\0` immédiatement → résultat vide.
- **`CRT_STUBS` étendu** : `printf`, `sprintf`, `vsprintf`, `vfprintf` et leurs variantes MSVC ajoutés → corps CRT Windows skippés, tsk-link résout directement vers stubs libc.

#### tsk-cc/codegen.rs
- **Call arg staging débordement FP** : `stage_reg = REG_SCRATCH + i` pour i≥4 → `R28 = FP` écrasé avec la valeur de l'argument → `FP + (-72) = valeur_arg - 72` → crash mémoire. Fix : staging limité à R24..R27 (4 slots), i≥4 → stage dans Ri directement.
- **VaStart frame layout** : save area chevauchait les allocas. Fix : `frame_size = 32` initialisé **avant** la boucle des allocas pour les fonctions variadiques → save area au bas du frame, allocas au-dessus.
- **VaStart SP dynamique supprimé** : `D_Sub SP, SP, 32` était émis dynamiquement mais la save area est maintenant incluse dans le prologue.

#### triskele-vm/src/cpu/decode.rs
- **`Im_Syscall` décodé Type R** (ROOT CAUSE) : `Im_Syscall` absent de `is_immediate_opcode` → décodé comme Type R → `id = dst = 0` → syscall 0x00 → crash. Fix : `Im_Syscall` ajouté à `is_immediate_opcode`. **Délégation vers `Opcode::is_immediate()` dans triskele-common.**

#### triskele-vm/src/cpu/mod.rs
- **`Im_Syscall` map_err écrasait `Halted`** : `.map_err(|e| VmError::FfiError(e.to_string()))` convertissait `VmError::Halted(42)` en `FfiError` → process::exit(1). Fix : propagation sélective — `Halted` passe tel quel, les autres deviennent `FfiError`.
- **`Im_CbInvoke` = CALL** : écrasait LR → retour dans trampoline. Fix : `Im_CbInvoke` = JMP indirect pur (`set_pc` sans `set_lr`).

#### triskele-vm/src/libc/mod.rs
- **`Exit` retournait `VmError::Trap`** au lieu de `VmError::Halted` → non géré dans run loop → `process::exit(1)`.
- **Doublon `Vsprintf`** dans `ALL_SYSCALLS` → `test_stub_addresses_are_unique` FAIL → supprimé.
- **`Vsprintf` (0x45)** ajouté comme syscall distinct.

#### tsk-link/src/main.rs
- **Phase 0** : pré-peuplement des symboles libc dans `global_syms` avant layout.
- **Phase 0b** : pré-scan far F_CALLs → calcul de `trampoline_reservation` → `data_base` correct **avant** Phase 2 (évite chevauchement trampolines/data).
- **Phase 3** : trampolines `Im_CbInvoke` pour far calls (code → libc à 0xE000_0000, distance 3.7GB > portée F_CALL 24 bits).

#### triskele-common (nouveaux modules)
- **`encoding.rs`** : `Opcode::encoding() → InstrEncoding { R, I, J }` — source de vérité unique. Élimine la classe de bugs Im_Syscall-like.
- **`memmap.rs`** : constantes VM canoniques (`LOAD_BASE`, `STACK_TOP`, `HEAP_BASE`, `LIBC_BASE`, `LIBC_STUB_SIZE`).
- **`libc_symbols.rs`** : table partagée symboles libc entre `tsk-link` et `triskele-vm`.

### Tâche 2 — Tests unitaires

**`triskele-vm` : 65 tests (dont 22 nouveaux)**
- `test_sprintf_percent_d/s/multi_args` — vérifie les bytes écrits
- `test_sprintf_writes_to_correct_address` — guard bytes poisonnés à 0xFF
- `test_sprintf_does_not_clobber_adjacent_memory`
- `test_vsprintf_from_va_ptr` / `test_vsprintf_va_ptr_zero_fallback`
- `test_vfprintf_returns_char_count`
- `test_malloc_returns_nonzero` / `test_malloc_zero_fills` / `test_malloc_two_calls_give_different_ptrs`
- `test_puts_returns_length_plus_newline`
- `test_format_printf_empty_string` / `test_format_printf_percent_p`

**`tsk-link` : 7 tests**
- `test_trampolines_do_not_overlap_data_{1,3,7}_calls`
- `test_libc_symbols_pre_populated`

### Tâche 3 — wolf3d-demo

Ajout de `#![allow(unused_assignments, dead_code)]` en tête de `wolf3d-demo/src/main.rs` pour supprimer les warnings bénins.

---

## Architecture VaStart (v0.3.9)

```
Frame layout pour fonctions variadiques (frame_size = 32 + allocas) :

  FP + 0                ← caller frame
  FP - (frame_size-32)  ← alloca[0]  (premier alloca)
  FP - (frame_size-24)  ← alloca[1]
  FP - (frame_size-16)  ← alloca[2]
  ...
  FP - frame_size       ← va_save[0] = R(n_fixed+0)
  FP - frame_size + 8   ← va_save[1] = R(n_fixed+1)
  FP - frame_size + 16  ← va_save[2] = R(n_fixed+2)
  FP - frame_size + 24  ← va_save[3] = R(n_fixed+3)
  SP                    ← bas du frame
```

---

## Architecture trampolines (v0.3.9)

```
Code compilé (0x1000..0x1000+N)
Trampolines    (0x1000+N..0x1000+N+T)    ← dans portée F_CALL ±33MB
Data section   (0x1000+N+T..0x1000+N+T+D)
```

Trampoline format (6 instructions, 24 bytes) :
```
D_MovI  R24, hi16(target)
D_MovI  R25, 16
D_Shl   R24, R24, R25
D_MovI  R25, lo16(target)
D_Or    R24, R24, R25
Im_CbInvoke R24          ← JMP indirect (LR inchangé)
```

---

## Fichiers modifiés en v0.3.9

```
crates/tsk-cc/src/ir.rs          ← GlobalInit::Bytes(Vec<u8>)
crates/tsk-cc/src/parser.rs      ← linkonce_odr, c"...", CRT_STUBS, (fntype) skip
crates/tsk-cc/src/codegen.rs     ← VaStart frame, call staging, GlobalInit::Bytes emit
crates/triskele-common/src/lib.rs         ← exports encoding, memmap, libc_symbols
crates/triskele-common/src/encoding.rs    ← NOUVEAU : InstrEncoding
crates/triskele-common/src/memmap.rs      ← NOUVEAU : constantes mémoire canoniques
crates/triskele-common/src/libc_symbols.rs ← (déjà en v0.3.8, amélioré)
crates/triskele-vm/src/cpu/decode.rs      ← Im_Syscall dans is_immediate, délégation
crates/triskele-vm/src/cpu/mod.rs         ← map_err sélectif, Im_CbInvoke=JMP
crates/triskele-vm/src/libc/mod.rs        ← Exit→Halted, Vsprintf, doublon supprimé
crates/tsk-link/src/main.rs               ← Phase 0/0b/3 trampolines, data_base fix
crates/tsk-link/Cargo.toml               ← [[bin]] explicite, tempfile dev-dep
crates/wolf3d-demo/src/main.rs            ← #![allow(unused_assignments, dead_code)]
projects/test_variadic/                   ← NOUVEAU projet (8 tests variadics)
```

---

## ISA — rappel

```
R0-R7   args/retour (caller-saved)
R8-R23  SSA temporaires
R24-R27 scratch codegen (staging args call)  ← R24..R27 UNIQUEMENT (R28=FP protégé)
R28=FP  frame pointer
R29=SP  stack pointer
R30=LR  link register
R31=PC
```

Mémoire VM :
```
0x00001000  .code/.data     0x70000000  Stack (1MB)
0x80000000  Heap (4MB)      0xE0000000  tsk-libc stubs
```

---

## Progression DoomGeneric : 60.9% (+6.9% cette session)

| Phase | Poids | Avancement |
|-------|-------|-----------|
| IR compiler (tsk-cc) | 35% | **84%** |
| tsk-libc | 20% | **52%** |
| VM & runtime | 20% | **48%** |
| Toolchain | 15% | **60%** |
| DoomGeneric intégration | 10% | **25%** |

---

## Prochaines étapes

### Priorité 1 — tsk-libc : `strcat`, `strtol`, `atoi`
Requis pour le parsing des arguments CLI de Doom et la construction des chemins WAD.

### Priorité 2 — File I/O : `fopen`/`fread`/`fclose`
Indispensable pour charger le fichier WAD. Implémentation via syscalls Im_FILE_* dans la VM.

### Priorité 3 — `snprintf`/`vsnprintf` complets
Doom utilise ces fonctions pour les messages d'erreur.

### Priorité 4 — Linking libdoom (95 fichiers .c)
Une fois file I/O disponible, compiler DoomGeneric complet.

---

## Backlog architectural

### Im_Syscall — protection structurelle (v0.3.9)
`Opcode::encoding()` dans `triskele-common` rend impossible le re-bug Im_Syscall. Toute future instruction Im_* doit être listée dans `encoding.rs`.

### wolf3d-demo migration
`crates/wolf3d-demo/` devrait migrer vers `projects/wolf3d-demo/` (démo applicative, pas composant toolchain). Non urgent.

### Register spill cross-block
Valeurs spillées dans bloc A, rechargées dans bloc B : fonctionne via `load_reg_or_imm` mais non testé sur cas DoomGeneric. À surveiller lors du linking libdoom.
