# TriskeleToolchain — Handover v0.3.0 Stack-Based
**Date**: 2026-06-04  
**Auteur**: Echopraxium with the collaboration of Claude AI  
**Repo**: https://github.com/Echopraxium/tscg  
**Chemin local**: `E:\_00_Michel\_00_Lab\_00_GitHub\tscg\instances\symbolic-system-grammars\TriskeleToolchain\`

---

## Statut actuel — ✅ EXIT 31 VALIDÉ

Le pipeline complet fonctionne sur `test_main.c` :
```
clang -O0 → .ll → tsk-cc → .tobj → tsk-link → .tvmx → tskvm → Exit 31
```
Tous les 5 tests passent : ScaleDiv(10,2), ScaleDiv(7,0), IsSolid(3,5), IsSolid(0,0), SumTiles(0,0,8,8).

---

## Architecture — 32 registres Stack-Based

### ISA (32 registres)
```
R0-R7   : args/retour (caller-saved)
R8-R23  : temporaires SSA (liveness-based)
R24-R25 : scratch codegen
R28=FP, R29=SP, R30=LR, R31=PC
```

### Encodage instructions (32-bit fixe)
```
Type R : opcode(8) | dst(5) | src1(5) | src2(5) | flags(9)
Type I : opcode(8) | dst(5) | imm19(19) signé
Type J : opcode(8) | offset24(24) signé
```

### Modèle mémoire stack-based
- `alloca` → slot sur la stack (SP+offset), **jamais** dans un registre
- `load/store` → adresse recalculée `D_MOV_I scratch, slot` + `D_ADD scratch, SP, scratch`
- Après chaque `F_CALL` → tous les registres SSA invalidés
- Compatible clang `-O0` : pattern `alloca/store/load` natif

---

## Fichiers clés modifiés (v0.3.0 vs v0.2.0)

| Fichier | Changement |
|---------|-----------|
| `tsk-cc/src/codegen.rs` | Alloca stack-based, `has_alloca=false`, liveness sans pinning, post-call invalidation |
| `tsk-cc/src/parser.rs` | `skip_to_keyword` s'arrête sur `GlobalRef` (fix @tilemap zappé) |
| `tsk-cc/src/main.rs` | Globals data dans symtab avec flag `0x8000_0000` |
| `tsk-link/src/main.rs` | Résolution data symbols via `data_base+offset`, GEP inline `name+offset` |

---

## Outils de développement

### Scripts Python (racine du workspace)
- `run_pipeline.py` — pipeline complet clang→VM, génère `pipeline_report.txt`
- `update_toolchain.py` — extraction zip vers workspace avec touch des .rs

### Batch Windows
- `_01_update_toolchain.bat` — mise à jour depuis zip (détecte automatiquement le zip)
- `_02_run_pipeline.bat` — lance le pipeline et attend une touche

### Commandes manuelles
```cmd
clang -O0 -S -emit-llvm -o lib/samples/test_main.ll lib/samples/test_main.c
cargo run -p tsk-cc  -- lib/samples/test_main.ll -o lib/samples/test_main.tobj
cargo run -p tsk-link -- lib/samples/test_main.tobj -o lib/samples/test_main.tvmx --entry main
cargo run -p triskele-vm -- lib/samples/test_main.tvmx
echo Exit: %ERRORLEVEL%
```

---

## Bugs identifiés et résolus

1. **Parser** : `skip_to_keyword` zappait `@tilemap` (entre `target` et `define`)
2. **Symtab** : globals data absents → flag `0x8000_0000` pour distinguer data/code
3. **Linker** : data symbols résolus via `code_base` au lieu de `data_base`
4. **Linker** : GEP inline `tilemap+323` — offset ignoré
5. **Codegen** : alloca en registres → register spill sur SumTiles (24+ valeurs vivantes)
6. **Codegen** : `has_alloca=true` mode conservative → registres épuisés
7. **Convention d'appel** : caller-saved correctement invalidés post-call

---

## Prochaines étapes

### Priorité 1 — Wolf3D sample
```cmd
clang -O0 -S -emit-llvm -o lib/samples/wolf3d_sample.ll lib/samples/wolf3d_sample.c
python run_pipeline.py  # adapter pour wolf3d_sample
```
Nouvelles instructions LLVM IR à implémenter :
- `switch` — Wolf3D a des switch() (état du jeu, touches)
- `select` — ternaire compilé par clang `-O0`
- `llvm.memset` / `llvm.memcpy` — intrinsics LLVM
- GEP multi-niveaux pour structs

### Priorité 2 — tsk-libc
Fonctions libc à porter :
- `memset`, `memcpy` → déjà dans ISA (`D_Memset`, `D_Memcpy`) ✅
- `malloc`, `free` → `A_Alloc`, `A_Free` ✅
- `strlen`, `strcpy`, `strcmp` → implémenter en bytecode TriskeleVM
- `sin`, `cos` → lookup tables (Wolf3D C89, pas de float)

### Priorité 3 — Debugger tsk-dbg
Migrer le debugger CLI de `cpu/mod.rs` → `tsk-dbg/session.rs` :
- Support `--script <file>` dans tsk-dbg (pas dans la VM)
- CLI et DAP partagent le même `session.rs`
- Breakpoints, step, registres, mémoire

### Priorité 4 — Wolf3D complet
Pipeline end-to-end : code source C89 Wolf3D → `.tvmx` → tskvm avec SDL2

---

## Structure du workspace
```
TriskeleToolchain/
  Cargo.toml              ← workspace root (version 0.3.0)
  run_pipeline.py         ← pipeline de test
  update_toolchain.py     ← mise à jour depuis zip
  _01_update_toolchain.bat
  _02_run_pipeline.bat
  crates/
    triskele-common/      ← ISA, registres, types TVM (32-reg)
    triskele-vm/          ← VM interpréteur + SDL2 + debugger CLI basique
    tsk-cc/               ← compilateur LLVM IR → .tobj (stack-based)
    tsk-link/             ← linker .tobj → .tvmx
    tsk-asm/              ← assembleur .tasm → .tobj
    tsk-dis/              ← désassembleur .tvmx
    tsk-dbg/              ← debugger DAP (VSCode) + CLI — À MIGRER
    tsk-build/            ← orchestrateur de build
    wolf3d-demo/          ← démo raycaster BabylonJS
  lib/
    SDL2.dll, SDL2.lib    ← SDL2 2.0.x Windows
    samples/
      test_main.c         ← test de validation (exit 31)
      test_main.ll        ← généré par clang -O0
      wolf3d_sample.c     ← sample Wolf3D (prochaine étape)
      wolf3d_sample.ll    ← à générer
```

---

## Notes importantes

- **LLVM IR target** : clang `-O0` uniquement — génère le pattern alloca/load/store compatible
- **SDL2** : version 0.36 (Rust crate), SDL2.dll 2.0.x requis dans `lib/`
- **Windows** : `cargo build` copie SDL2.dll dans `target/debug/` via `build.rs`
- **Auteur** : toujours `Echopraxium with the collaboration of Claude AI`
- **Licence** : BSD 3-Clause (code), CC BY 4.0 (documentation)
