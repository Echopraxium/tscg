# TriskeleToolchain — Handover v0.3.5
**Date**: 2026-06-09  
**Auteur**: Echopraxium with the collaboration of Claude AI  
**Repo**: https://github.com/Echopraxium/tscg  
**Chemin local**: `E:\_00_Michel\_00_Lab\_00_GitHub\tscg\instances\symbolic-system-grammars\TriskeleToolchain\`

---

## Statut actuel — ✅ QUINTUPLE VALIDATION

| Projet | Type | Exit | Tests |
|--------|------|------|-------|
| `test_main` | C89 | 31 ✅ | ScaleDiv(10,2), ScaleDiv(7,0), IsSolid(3,5), IsSolid(0,0), SumTiles |
| `wolf3d` | C89 | 15 ✅ | ScaleDiv, IsSolid, MoveActor (fixed-point 16.16), SumTiles |
| `test_patterns` | C89 | 15 ✅ | switch, function pointers, 2D array, pointer arithmetic |
| `test_select` | C89 | 9 ✅ | select (ternaire C), memset, memcpy, clamp, abs, max, min |
| `doom_fixed` | C89 | 127 ✅ | FixedMul×3, FixedDiv×4 — **NOUVEAU v0.3.5** |

---

## Tous les changements en v0.3.5

### Nouveau projet `doom_fixed`

Premier fichier de DoomGeneric compilé et validé : `m_fixed.c` (arithmetic fixed-point 16.16).

Structure :
```
projects/doom_fixed/
  include/doom_fixed.h      ← fixed_t, FRACBITS, FIXED_ABS — standalone (pas de dépendances Doom)
  src/m_fixed.c             ← FixedMul + FixedDiv (fidèles à DoomGeneric)
  src/doom_fixed_test.c     ← 7 tests, exit bitmask 127
  pipeline.toml             ← expected_exit = 127
```

**Contrainte imm19 dans le harness** : toutes les constantes littérales sont dans `[-262144, 262143]`
pour éviter `D_SHL` (bug connu). Les tests overflow utilisent des comparaisons de signe (`r > 0`,
`r < 0`) au lieu de comparer à `INT_MAX`/`INT_MIN` (hors imm19).

### Allocateur de registres unifié (`tsk-cc/codegen.rs`)

**Problème** : L'ancien mode conservatif (`has_alloca=true`) ne recyclait jamais aucun registre →
24 valeurs SSA vivantes simultanément dans `FixedDiv` → register spill → codegen échouait
silencieusement → `F_Trap` à la place de la fonction.

**Solution** : Un seul mode avec deux règles :
- **Phi destinations** → `ra.protected: HashSet<String>` — jamais recyclées (registre stable
  nécessaire pour `emit_phi_copies` depuis n'importe quel prédécesseur)
- **Paramètres** → jamais recyclés ni par liveness ni par `free_name` (R0..Rn doivent rester
  valides pendant toute la durée de la fonction appelée)
- **Tout le reste** → liveness inter-blocs : recyclé dès que mort dans le bloc courant

Suppression de `has_alloca: bool`, remplacé par `protected: HashSet<String>`.

**Résultat** : `FixedDiv` (10 blocs, 2 phi nodes) compile en 472 bytes, 118 instructions. Maximum
de registres simultanément actifs : ~9 au lieu de 24.

### `free_name` après Store et Select (`tsk-cc/codegen.rs`)

Libération explicite des registres après leur dernier usage certain :
- **`Store`** : la valeur SSA stockée en mémoire ne sera jamais relue depuis son registre (modèle `-O0`)
- **`Select`** : `cond`, `true_val`, `false_val` sont morts après le select

Ces libérations complètent le liveness pour les cas où la liveness inter-blocs n'est pas suffisamment
précise à l'intérieur d'un bloc.

### Fix D_Shl / D_Shr (`triskele-vm/cpu/mod.rs`)

**Bug** : `D_Shl` et `D_Shr` lisaient le shift depuis `_flags` (toujours 0 quand `tsk-cc` encode via
Type R) au lieu de `s2`.

**Fix** : Lire `s2` en priorité, fallback sur `_flags` pour compatibilité legacy :
```rust
let shift = if s2 != 0 {
    (self.regs.get(s2)? & 0x3F) as u32
} else {
    (_flags & 0x1F) as u32
};
```

Ce bug causait `FixedMul` de retourner `a * b` sans le décalage de 16 bits.

### Fix parallel move dans Call (`tsk-cc/codegen.rs`)

**Bug** : Les arguments d'appel étaient copiés séquentiellement en R0..Rn, causant une collision
quand arg0 était dans R1 et arg1 dans R0 :
```
D_Mov R0, R1   ← R0 = b (correct)
D_Mov R1, R0   ← R1 = b (FAUX — R0 vient d'être écrasé)
```

**Fix** : Two-phase staging via R24, R25... :
- Phase 1 : charger tous les args dans REG_SCRATCH+i (R24, R25, ...)
- Phase 2 : copier R24→R0, R25→R1, ...

### Nouveaux tests unitaires (`tsk-cc/codegen.rs`)

4 tests dans `codegen::tests` validant le nouvel allocateur :

| Test | Ce qu'il vérifie |
|------|-----------------|
| `test_phi_dst_is_protected` | Les phi-destinations sont dans `ra.protected` |
| `test_phi_dst_register_is_stable` | Une fonction avec phi compile sans spill |
| `test_no_spill_with_many_ssa_and_phi` | 6 blocs, 2 phi nodes, 20+ SSA → pas de spill |
| `test_liveness_recycles_non_phi_values` | `ra.used ≤ 12` (liveness recycle bien) |

**Total tests unitaires** : 11 (7 existants + 4 nouveaux), tous ✅.

---

## Patterns LLVM IR validés (cumulatif)

| Pattern | Status | Projet validant |
|---------|--------|-----------------|
| alloca / store / load | ✅ | test_main |
| if/else (BrCond) | ✅ | test_main |
| boucles (BrUncond) | ✅ | test_main |
| appels de fonctions | ✅ | test_main |
| GEP tableaux 1D | ✅ | test_main |
| GEP struct | ✅ | wolf3d |
| fixed-point 16.16 | ✅ | wolf3d |
| switch | ✅ | test_patterns |
| pointeurs de fonctions | ✅ | test_patterns |
| tableaux 2D | ✅ | test_patterns |
| arithmétique de pointeurs | ✅ | test_patterns |
| select (ternaire C) | ✅ | test_select |
| llvm.memset | ✅ | test_select |
| llvm.memcpy | ✅ | test_select |
| **phi nodes multi-blocs** | ✅ | doom_fixed |
| **sext i32→i64 / trunc i64→i32** | ✅ | doom_fixed |
| **sdiv i64** | ✅ | doom_fixed |
| **zext i1→i64** | ✅ | doom_fixed |

---

## Fichiers modifiés en v0.3.5

```
crates/tsk-cc/src/codegen.rs              ← allocateur unifié + free_name + Call two-phase
crates/triskele-vm/src/cpu/mod.rs         ← fix D_Shl/D_Shr (s2 en priorité sur flags)
projects/doom_fixed/                      ← NOUVEAU projet
  include/doom_fixed.h
  src/m_fixed.c
  src/doom_fixed_test.c
  pipeline.toml
```

---

## Structure workspace

```
TriskeleToolchain/
  run_pipeline.py         ← v0.3.2 générique (lit pipeline.toml)
  update_toolchain.py     ← v0.3.2 (merge intelligent projects/)
  lib/  SDL2.dll  SDL2.lib  tsk-libc.tvml
  projects/
    test_main/            ← ✅ exit 31 (5 tests)
    wolf3d/               ← ✅ exit 15 (4 tests, C89 sample avec struct fixed-point)
    test_patterns/        ← ✅ exit 15 (switch, fn ptrs, 2D array, ptr arith)
    test_select/          ← ✅ exit 9  (select, memset, memcpy)
    doom_fixed/           ← ✅ exit 127 (FixedMul, FixedDiv — NOUVEAU v0.3.5)
    Doom-Generic/         ← code source DoomGeneric (à compiler)
    wolfenstein3d-opensource/ ← code Wolf3D DOS (trop dépendant DOS, en attente)
    wolf3d_raycaster/     ← tasm, bug chargement VM (data avant code)
    wolf3d_v2/            ← tasm, même bug
  crates/
    triskele-common/  triskele-vm/  tsk-cc/  tsk-link/
    tsk-asm/  tsk-dis/  tsk-dbg/  tsk-build/
    tsk-libc-gen/  wolf3d-demo/
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

### Priorité 1 — doom_alloc (m_alloc.c de DoomGeneric)
Prochain fichier DoomGeneric à compiler. Introduira probablement `malloc`/`free` → tsk-libc.

### Priorité 2 — tsk-libc
`malloc`, `free`, `printf`, `memset`, `memcpy` (stubs VM déjà présents pour memset/memcpy).

### Priorité 3 — Fix bug tasm raycaster
`wolf3d_v2` : section `.rodata` chargée à `LOAD_BASE`, labels calculés depuis `0x0000`.

### Priorité 4 — tsk-asm symtab format
Format attendu par `tsk-link` : `name\0` puis `u32 offset`. Actuellement inversé.

### Priorité 5 — Fix D_Shl avec constante immédiate
`D_Shl` émet `D_MovI hi + D_Shl 16` pour les grandes constantes — `s2=0` dans ce cas, donc
le fallback `_flags` est utilisé. **Ce cas est cassé.** Les contournements actuels évitent
`D_Shl` dans les harness de test. À corriger proprement : émettre `D_MovI s2, 16 + D_Shl dst, src, s2`.

---

## Backlog architectural

### Registres "smart pointer" avec flags
Formaliser l'allocation/libération avec états explicites : `FREE`, `OWNED`, `BORROWED`, `PINNED`.
- `PINNED` = équivalent de `protected` actuel, mais formalisé
- Permettrait l'instrumentation (compter les utilisations, détecter les fuites)
- Prérequis pour un futur allocateur par graphe de coloration

### Register spill sur stack ("register file étendu")
Quand les 32 registres physiques sont saturés, spiller vers la stack et recharger à la demande.
- Mécanisme standard sur x86/ARM pour callee-saved registers
- Pas urgent avec le liveness unifié (max ~9 registres actifs simultanément)
- Nécessaire pour des fonctions C très complexes avec nombreux temporaires actifs

---

## Notes techniques importantes

### Allocateur unifié (v0.3.5)
- `ra.protected` contient **uniquement** les phi-destinations — pré-allouées en pre-pass 3
- Les paramètres (`ra.params`) sont exclus du recyclage dans `get_or_alloc` ET dans `free_name`
- `free_name` est safe car les adresses alloca ne sont jamais dans `ra.map`
- `ra.used` = high-water mark des registres physiques — doit rester ≤ 12 pour les fonctions normales

### D_Shl/D_Shr (v0.3.5)
- `s2 != 0` → shift depuis registre (chemin normal pour `tsk-cc`)
- `s2 == 0` → shift depuis `_flags` (legacy, utilisé par tsk-asm manuel)
- **Cas à corriger** : `split_const32` émet `D_MovI hi + D_Shl 16 (s2=scratch)` — le scratch
  doit être passé en s2, pas laissé à 0

### Call two-phase staging (v0.3.5)
- Staging via R24+i (max 8 args → R24..R31, pas de collision avec les slots d'args R0..R7)
- Coût : 2 `D_Mov` par arg au lieu de 1 — négligeable pour `-O0`

### MemSet/MemCpy inline
- Boucle byte-à-byte (pas de D_Store32 par blocs) — correct mais lent
- Pour DoomGeneric, envisager une optimisation word-aligned si les benchmarks le justifient

### imm19 constraint
- Plage : `[-262144, 262143]`
- Valeurs hors plage → `split_const32` → `D_MovI hi + D_Shl 16 + D_Or lo`
- `D_Shl` avec s2=0 est cassé (voir ci-dessus) → éviter les grandes constantes dans les harness
