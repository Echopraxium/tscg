# TriskeleToolchain — Handover v0.3.8
**Date**: 2026-06-09  
**Auteur**: Echopraxium with the collaboration of Claude AI  
**Repo**: https://github.com/Echopraxium/tscg  
**Chemin local**: `E:\_00_Michel\_00_Lab\_00_GitHub\tscg\instances\symbolic-system-grammars\TriskeleToolchain\`

---

## Statut actuel — ✅ SEXTUPLE VALIDATION (inchangée depuis v0.3.7)

| Projet | Type | Exit | Tests |
|--------|------|------|-------|
| `test_main` | C89 | 31 ✅ | ScaleDiv(10,2), ScaleDiv(7,0), IsSolid(3,5), IsSolid(0,0), SumTiles |
| `wolf3d` | C89 | 15 ✅ | ScaleDiv, IsSolid, MoveActor (fixed-point 16.16), SumTiles |
| `test_patterns` | C89 | 15 ✅ | switch, function pointers, 2D array, pointer arithmetic |
| `test_select` | C89 | 9 ✅ | select (ternaire C), memset, memcpy, clamp, abs, max, min |
| `doom_fixed` | C89 | 127 ✅ | FixedMul×3, FixedDiv×4 |
| `doom_alloc` | C89 | 255 ✅ | Zone allocator Z_Malloc/Z_Free |

> ✅ Validé sur Windows (2026-06-09) avec `run_pipeline.py` v0.3.3 (`--release`).  
> Pipeline report `test_main` confirmé exit 31 avec tsk-cc v0.3.8.

---

## Changements en v0.3.8

### Tâche 1 — Nouveau projet `doom_zzone`

Compile le **vrai `z_zone.c` de DoomGeneric** (non modifié) avec des stubs pour les dépendances externes.

**Différence clé vs `doom_alloc`** : `doom_alloc` utilisait une version standalone modifiée de l'allocateur. `doom_zzone` utilise l'original verbatim avec des stubs légers.

Structure :
```
projects/doom_zzone/
  include/
    z_zone_stubs.h   ← I_ZoneBase (buffer 2MB statique) + I_Error (halt) + byte/boolean
    z_zone.h         ← copie de DoomGeneric (stdio.h → z_zone_stubs.h)
  src/
    z_zone.c         ← original DoomGeneric (i_system.h / doomtype.h strippés)
    doom_zzone_test.c ← 8 tests, exit bitmask 255
  pipeline.toml      ← expected_exit = 255
```

Tests (exit bitmask) :
| Bit | Test |
|-----|------|
| 0 | Z_Malloc non-NULL |
| 1 | Z_Free + Z_CheckHeap — heap integrity |
| 2 | *user == p3 — double indirection Z_Malloc |
| 3 | p4 != p3 — deux allocations adresses différentes |
| 4 | Z_FreeTags PU_LEVEL — augmente Z_FreeMemory |
| 5 | Z_FreeMemory after Z_Free — coalesce |
| 6 | Z_CheckHeap après 8 alloc/4 free — pas de corruption |
| 7 | alloc-after-free réutilise la région rover |

Stubs dans `z_zone_stubs.h` :
- `I_ZoneBase(int* size)` → retourne `doom_zone_heap[2MB]`, `*size = 2MB`
- `I_Error(const char* fmt, ...)` → `fprintf(stderr, ...)` + boucle infinie (VM halt sur F_Halt)
- `byte` / `boolean` / `TRUE` / `FALSE` typedefs C89

---

### Tâche 2 — `tsk-libc` enrichi (`libc/mod.rs`)

Ajout de 6 nouveaux syscalls + refactorisation de `printf` :

| ID hex | Symbole | Comportement |
|--------|---------|--------------|
| 0x33 | `malloc` | Bump allocator sur `HEAP_BASE`, align 8, zero-fill. OOM → R0=0 |
| 0x34 | `free` | No-op (bump allocator sans libération) |
| 0x35 | `exit` | `VmError::Trap(code)` → halt propre avec exit code |
| 0x41 | `fprintf` | FILE* ignoré, redirige stderr. Args R1=fmt, R2..R5=args |
| 0x42 | `vfprintf` | Lit va_list depuis pointeur stack (R2=va_ptr, 4 args max) |
| 0x43 | `sprintf` | Écrit dans buffer VM (R0=buf, R1=fmt, R2..R5=args) |
| 0x44 | `puts` | String + `\n` → stderr. R0=str_ptr |

**Refactorisation `printf`** : extraction vers `fn format_printf(fmt_ptr, args, mem)` partagé par `Printf`, `Fprintf`, `Vfprintf`, `Sprintf`. Élimine ~60 lignes dupliquées.

**`LibcState`** : ajout champs `heap_bump: u64` et `heap_ceil: u64` initialisés depuis `HEAP_BASE`/`HEAP_SIZE`.

Segment LIBC étendu dans les tests : `0x45 * STUB_SIZE` (couvre jusqu'à `Puts = 0x44`).

---

### Tâche 3 — Register spill sur stack (`tsk-cc/codegen.rs`)

Résout le `bail!("register spill...")` en implémentant un vrai mécanisme d'éviction sur stack.

**Architecture :**

```
RegAlloc nouveaux champs:
  spill_map:     HashMap<String, i32>   // SSA → offset depuis frame base
  spill_top:     i32                    // prochain slot disponible
  spill_pending: Option<SpillAction>    // éviction à émettre
  
SpillAction { victim: String, reg: usize, slot: i32 }
```

**Algorithme d'éviction** (dans `get_or_alloc`) :
1. Pool `free` vide → cherche victime parmi valeurs live non-protégées non-params
2. Critère : coût = `live_block_count + 1000 * live_in_cur_block`
3. Éviction : retire de `ra.map`, enregistre dans `spill_map`, set `spill_pending`
4. Attribue le registre libéré au nouveau nom

**Émission store/reload** :
```
emit_spill_store(reg, slot)  → D_Store64 [FP - (frame_size + slot + 8)], reg
emit_spill_reload(reg, slot) → D_Load64  reg, [FP - (frame_size + slot + 8)]
flush_spill_pending()        → consomme spill_pending et émet le store
```

**Intégration `gen_instr`** : 12 appels `flush_spill_pending()` insérés automatiquement après chaque `get_or_alloc(dst)`.

**`load_reg_or_imm`** : path supplémentaire — si `is_spilled(name)`, appelle `reload()` + `emit_spill_reload()`.

**Frame size patching** : après génération du code, `frame_size` est étendu (`= spill_top`) et le `D_MovI` du prologue est patché in-place avec la taille totale.

**Fixes warnings v0.3.8** :
- `#[allow(dead_code)]` sur `SpillAction` et `ensure_loaded`
- Renommage `prologue_movI_offset` → `prologue_mov_i_offset`

---

## Fichiers modifiés en v0.3.8

```
crates/tsk-cc/src/codegen.rs           ← register spill + fixes warnings
crates/triskele-vm/src/libc/mod.rs     ← malloc/free/exit/fprintf/sprintf/puts
projects/doom_zzone/                   ← NOUVEAU projet (vrai z_zone.c)
  include/z_zone_stubs.h
  include/z_zone.h
  src/z_zone.c
  src/doom_zzone_test.c
  pipeline.toml
```

---

## Structure workspace

```
TriskeleToolchain/
  run_pipeline.py         ← v0.3.3 générique (--release, --clean opt-in)
  update_toolchain.py     ← v0.3.2 (merge intelligent projects/)
  lib/  SDL2.dll  SDL2.lib  tsk-libc.tvml
  projects/
    test_main/            ← ✅ exit 31 (5 tests)
    wolf3d/               ← ✅ exit 15 (4 tests)
    test_patterns/        ← ✅ exit 15 (switch, fn ptrs, 2D array, ptr arith)
    test_select/          ← ✅ exit 9  (select, memset, memcpy)
    doom_fixed/           ← ✅ exit 127 (FixedMul, FixedDiv)
    doom_alloc/           ← ✅ exit 255 (Zone allocator standalone)
    doom_zzone/           ← 🆕 à valider (vrai z_zone.c DoomGeneric)
    Doom-Generic/         ← code source DoomGeneric (à compiler)
    wolfenstein3d-opensource/ ← code Wolf3D DOS (en attente)
```

---

## ISA — rappel

```
R0-R7   args/retour (caller-saved)
R8-R23  SSA temporaires
R24-R25 scratch codegen (R24=SCRATCH, R25=SCRATCH+1)
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

## Prochaines étapes

### Priorité 1 — Valider `doom_zzone`
```
python run_pipeline.py doom_zzone
```
Exit attendu : 255 (tous les 8 bits). Premiers problèmes probables :
- `fprintf` dans `Z_DumpHeap` / `Z_CheckHeap` → résolu via libc `fprintf` v0.3.8
- `Z_CheckHeap` appelle `I_Error` → résolu via stub `z_zone_stubs.h`

### Priorité 2 — `z_zone.c` complet avec `I_Error`/`printf` fonctionnels
Compiler le vrai `z_zone.c` DoomGeneric avec `tsk-libc` printf (déjà disponible) et valider les chemins d'erreur (`Z_CheckHeap` corruption detection).

### Priorité 3 — `tsk-libc` : `malloc`/`free` vrais (avec coalesce)
Le bump allocator actuel est suffisant pour Doom (qui utilise principalement `Z_Malloc`). Un vrai `malloc` avec free-list sera nécessaire pour du code C général.

### Priorité 4 — Valider le register spill sur une vraie fonction dense
`Z_ClearZone` de `doom_alloc` avait ~52 instructions dans un seul bloc — c'est un bon candidat pour déclencher le spill et valider le reload.

---

## Backlog architectural

### Register spill — points à surveiller
- **Cross-block reload** : si une valeur est spillée dans le bloc A et utilisée dans le bloc B, `load_reg_or_imm` la rechargera implicitement. Correct pour les cas simples (alloca-like), mais peut introduire une double-load si le même spill_slot est rechargé sur plusieurs chemins.
- **Phi + spill** : les phi-destinations sont `protected` (jamais évictées), donc aucun risque de conflit entre spill et phi-copies.
- **Frame size limite** : `offset_from_fp = -(frame_size + slot + 8)` est encodé en `i16` dans `_flags`. Limite : ±32767 bytes de slots de spill (≈4095 valeurs de 8 bytes). Suffisant pour tout code C89 réaliste.

### Registres "smart pointer" avec flags
Backlog long terme : formaliser `FREE` / `OWNED` / `BORROWED` / `PINNED` pour un futur allocateur par graphe de coloration.
