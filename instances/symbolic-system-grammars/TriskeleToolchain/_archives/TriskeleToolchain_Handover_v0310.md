# TriskeleToolchain — Handover v0.3.10
**Date**: 2026-06-12  
**Auteur**: Echopraxium with the collaboration of Claude AI  
**Repo**: https://github.com/Echopraxium/tscg  
**Chemin local**: `E:\_00_Michel\_00_Lab\_00_GitHub\tscg\instances\symbolic-system-grammars\TriskeleToolchain\`

---

## Statut actuel — ✅ DÉCUPLE VALIDATION (10/10)

```
python run_all_tests.py
```

| Projet | Chemin | Exit | Statut |
|--------|--------|------|--------|
| `test_main` | `toolchain-tests/c89/test_main` | 31 | ✅ |
| `test_patterns` | `toolchain-tests/c89/test_patterns` | 15 | ✅ |
| `test_select` | `toolchain-tests/c89/test_select` | 9 | ✅ |
| `test_variadic` | `toolchain-tests/c89/test_variadic` | 255 | ✅ |
| `test_doom_libc` | `toolchain-tests/c89/test_doom_libc` | 511 | ✅ |
| `wolf3d` | `wolfenstein3D/wolf3d` | 15 | ✅ |
| `doom_fixed` | `doom-generic/vm-porting/tests/doom_fixed` | 127 | ✅ |
| `doom_alloc` | `doom-generic/vm-porting/tests/doom_alloc` | 255 | ✅ |
| `doom_zzone` | `doom-generic/vm-porting/tests/doom_zzone` | 255 | ✅ |
| **`doom_math`** | `doom-generic/vm-porting/tests/doom_math` | **127** | ✅ **NOUVEAU** |

> ✅ Validé sur Windows (2026-06-12) avec `run_all_tests.py` v0.3.10.

---

## Changements en v0.3.10

### Tâche 1 — tsk-libc : 26 nouveaux syscalls

**`crates/triskele-vm/src/libc/mod.rs`** (1244 → 1809 lignes)  
**`crates/triskele-common/src/libc_symbols.rs`** — table linker mise à jour (était désynchronisée)

| Groupe | Fonctions | IDs |
|--------|-----------|-----|
| String ext | `strrchr strstr strdup strcasecmp strncasecmp strlcat strlcpy` | 0x16–0x1C |
| Stdlib+ | `atoi strtol` | 0x36–0x37 |
| I/O fmt | `snprintf vsnprintf` | 0x46–0x47 |
| Ctype | `toupper tolower isspace isdigit isalpha isprint` | 0x50–0x55 |
| File I/O | `fopen fclose fread fwrite fseek ftell feof fflush` | 0x60–0x67 |

`LibcState` enrichi : table de file handles (`FILE_HANDLE_BASE = 0xF000_0000`), méthodes `alloc_handle` / `get_handle_mut` / `free_handle`.

**Leçon importante** : `libc_symbols.rs` dans `triskele-common` est la **source de vérité du linker**. Tout ajout dans `mod.rs` doit impérativement être reflété dans ce fichier, sinon les nouveaux symboles sont résolus à adresse nulle → crash.

### Tâche 2 — tsk-cc : `llvm.abs.*` intrinsic

**`crates/tsk-cc/src/ir.rs`** : nouvel `Instr::Abs { dst, ty, val }`  
**`crates/tsk-cc/src/parser.rs`** : intercepte `llvm.abs.i32` / `llvm.abs.i64`  
**`crates/tsk-cc/src/codegen.rs`** : codegen inline (V_CmpI + F_Jnz + D_Sub + D_Mov)

Nécessaire pour `FixedDiv` dans `m_fixed.c` — clang -O0 génère `@llvm.abs.i32` pour `abs()` sur entiers.

### Tâche 3 — Premier vrai code DoomGeneric compilé

Nouveau projet `doom-generic/vm-porting/tests/doom_math` :
- Compile **`m_fixed.c`** et **`m_random.c`** directement depuis `Doom-Generic/doomgeneric/` sans modification
- 7 tests : `FixedMul`, `FixedDiv`, `M_Random`, `P_Random`, `M_ClearRandom`
- Exit attendu : 127 (0x7F)

### Tâche 4 — Infrastructure

**Hiérarchie `projects/`** réorganisée :
```
projects/
├── toolchain-tests/
│   ├── c89/          (test_main, test_patterns, test_select, test_variadic, test_doom_libc, test-lib-dos)
│   └── asm/          (hello, test_div, test_shr, sdl_test)
├── wolfenstein3D/
│   ├── wolf3d/       (projet principal pipeline)
│   └── tests/        (wolf3d_drawtest, wolf3d_raycaster, wolf3d_raycaster_debug, wolf3d_v2, wolf3d_v2_clean)
├── doom-generic/
│   ├── src/          (Doom-Generic sources originaux)
│   └── vm-porting/
│       └── tests/    (doom_fixed, doom_alloc, doom_zzone, doom_math)
└── references/       (wolf3D_4DSL, wolfenstein3d-opensource, .url)
```

**`run_pipeline.py` v0.3.4** : accepte les chemins relatifs (`doom-generic/vm-porting/tests/doom_math`) et reste rétrocompatible avec les noms plats (résolution récursive).

**`run_all_tests.py` v0.3.10** : lance les 10 projets de validation en une commande, avec `--keep-going` et `--clean`.

---

## À faire en priorité dans la prochaine session

### ⚠️ Avant tout : bumper les versions Cargo

Les crates modifiées en v0.3.10 sont encore à `0.3.5`. Bumper dans les `Cargo.toml` :
- `crates/triskele-vm/Cargo.toml` → `0.3.10`
- `crates/triskele-common/Cargo.toml` → `0.3.10`
- `crates/tsk-cc/Cargo.toml` → `0.3.10`

### Priorité 1 — `m_argv.c` (parsing CLI Doom)

Fichier : `Doom-Generic/doomgeneric/m_argv.c`  
Dépendances : `doomtype.h`, `i_system.h`, `m_argv.h`, `m_misc.h`  
Fonctions libc utilisées : `strcasecmp`, `strrchr` (déjà dans tsk-libc ✅)  
Blocker potentiel : `I_Error` (fonction variadique Doom — stub nécessaire)

Créer `doom-generic/vm-porting/tests/doom_argv/` avec un `main` de test qui appelle `M_CheckParm`, `M_FindResponseFile`, `M_GetExecutableName`.

### Priorité 2 — `w_wad.c` (loader WAD — critique pour Doom)

Fichier : `Doom-Generic/doomgeneric/w_wad.c`  
Fonctions libc utilisées : `fopen`, `fread`, `fclose`, `fseek`, `ftell`, `malloc`, `strdup`, `strcasecmp`, `toupper` — **tout est déjà dans tsk-libc** ✅  
Blocker potentiel : `I_Error` + `W_CheckNumForName` utilise `strncasecmp`

Créer un fichier WAD minimal de test (header + 1 lump) pour valider le chargement.

### Priorité 3 — Stub `I_Error`

`I_Error` est une fonction variadique Doom appelée partout. Elle doit être stubée pour que les modules compilent. Signature :
```c
void I_Error(const char *error, ...)
```
Le stub minimal : afficher le message via `vsnprintf` + `puts`, puis `exit(1)`.

### Priorité 4 — `strerror` + `sscanf`

Encore absents de tsk-libc, utilisés dans `m_config.c` et quelques autres fichiers Doom.

---

## Progression DoomGeneric

| Phase | Poids | v0.3.9 | v0.3.10 |
|-------|-------|--------|---------|
| IR compiler (tsk-cc) | 35% | 84% | **87%** |
| tsk-libc | 20% | 52% | **78%** |
| VM & runtime | 20% | 48% | **55%** |
| Toolchain | 15% | 60% | **65%** |
| DoomGeneric intégration | 10% | 25% | **30%** |

**Total : ~68%** (+7% cette session)

---

## Rappels architecture

### Patchs — convention obligatoire
Les patchs sont **toujours livrés sous forme de zip** contenant les fichiers modifiés dans leur arborescence exacte (`crates/…`, `projects/…`). À décompresser à la racine du workspace. **Jamais de scripts Python pour modifier les fichiers source.**

### Validation
```cmd
python run_all_tests.py          # suite complète (10 projets)
python run_all_tests.py --clean  # avec cargo clean
python run_pipeline.py doom-generic/vm-porting/tests/doom_math --clean  # projet seul
```

### libc_symbols.rs — règle de synchronisation
Chaque ajout dans `triskele-vm/src/libc/mod.rs` (enum `LibcSyscall` + dispatch) **doit** avoir une entrée correspondante dans `triskele-common/src/libc_symbols.rs` avec le **même ID**. Sans ça, le linker résout le symbole à l'adresse 0 → crash immédiat.

### llvm intrinsics connus
| Intrinsic | Statut | Fichier |
|-----------|--------|---------|
| `llvm.memset.*` | ✅ supporté | parser.rs |
| `llvm.memcpy.*` | ✅ supporté | parser.rs |
| `llvm.va_start.*` | ✅ supporté | parser.rs |
| `llvm.va_end.*` | ✅ no-op | parser.rs |
| `llvm.abs.*` | ✅ supporté | parser.rs + ir.rs + codegen.rs |
| `llvm.lifetime.*` | ✅ no-op | parser.rs |
| `llvm.dbg.*` | ✅ no-op | parser.rs |

### ISA rappel
```
R0-R7   args/retour (caller-saved)
R8-R23  SSA temporaires
R24-R27 scratch codegen (staging args call)
R28=FP  frame pointer
R29=SP  stack pointer
R30=LR  link register
R31=PC
```

Mémoire VM :
```
0x00001000  .code/.data
0x70000000  Stack (1MB)
0x80000000  Heap (4MB)
0xE0000000  tsk-libc stubs  (IDs 0x01..0x67)
0xF0000000  FILE* handles   (LibcState.file_handles)
```
