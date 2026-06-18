# TriskeleToolchain — Handover v0.3.13

**Author**: Echopraxium with the collaboration of Claude AI  
**Date**: 2026-06-15  
**Patch**: `TriskeleToolchain_patch_v0313.zip`  
**Workspace (Windows)**: `E:\_00_Michel\_00_Lab\_00_GitHub\tscg\instances\symbolic-system-grammars\TriskeleToolchain\`

---

## 1. Validation Baseline

### Stable (unchanged from v0.3.12b)

| Project | Expected Exit | Status |
|---------|--------------|--------|
| test_main | 31 | ✅ |
| test_patterns | 15 | ✅ |
| test_select | 9 | ✅ |
| test_variadic | ? | ✅ |
| test_doom_libc | ? | ✅ |
| wolf3d | 15 | ✅ |
| doom_fixed | 127 | ✅ |
| doom_alloc | 255 | ✅ |
| doom_zzone | 255 | ✅ |
| doom_math | ? | ✅ |
| doom_argv | 63 | ✅ |

### In progress

| Project | Expected Exit | Linux (sandbox) | Windows (last known) |
|---------|--------------|-----------------|----------------------|
| doom_wad | 255 | `I_Error: Couldn't realloc lumpinfo` (exit 1) | `Memory fault addr=0x4` (exit 1) |

---

## 2. Bugs Fixed This Session (v0.3.12b → v0.3.13)

### B15 — Alloca offsets inconsistants (`tsk-cc/src/codegen.rs`)

**Cause** : dans `load_reg_or_imm`, l'adresse d'une variable alloca était calculée par `fp_offset = slot - self.frame_size`. Or `frame_size` vaut `alloca_top` pendant la génération du code, puis est **patchée à la hausse** une fois tous les spill slots alloués. Résultat : le **prologue** stockait à `[FP - petit_offset]` (avec frame_size=alloca_top), et les accès **ultérieurs** lisaient depuis `[FP - grand_offset]` (avec frame_size patchée). Collision silencieuse → valeurs lues nulles ou erronées.

**Fix** : nouveau champ `alloca_top: i32` dans `FuncGen`, enregistré immédiatement après le pre-pass 1 d'allocation des allocas, avant toute croissance de `spill_top`. Dans `load_reg_or_imm` : `fp_offset = slot - self.alloca_top` (invariant).

**Layout résultant** :
```
FP + 0           : LR sauvé par A_ENTER
FP - 8           : dernière alloca (slot = alloca_top - 8)
FP - alloca_top  : première alloca (slot = 0)
FP - alloca_top - 8 : premier spill slot (slot = alloca_top)
...
FP - frame_size  : SP final
```

### B16 — Formule de spill inconsistante (`tsk-cc/src/codegen.rs`)

**Cause** : `emit_spill_store` et `emit_spill_reload` utilisaient `offset_from_fp = -(self.frame_size + slot + 8)`. Pendant la génération (avant le patch), `frame_size = alloca_top`. Les stores spill allaient à `[FP - (alloca_top + slot + 8)]`, mais `slot` commence à `alloca_top` → offset = `-(2 × alloca_top + 8)`. Ces adresses empiétaient sur la région alloca (collision) et changeaient de sens après le patch frame.

**Fix** : formule directe `offset_from_fp = -(slot + 8)`. Comme `slot >= alloca_top`, les spills commencent à `[FP - (alloca_top + 8)]` et descendent — toujours **sous** la région alloca, sans dépendance à `frame_size`.

**Invariant** : les trampolines 3-instructions (`D_MOV_I R25 + D_ADD + D_STORE64/LOAD64`) restent déclenchés si `|offset| >= 256`, inchangé.

### B12 — Symboles privés par objet (`tsk-link/src/main.rs`) *(déjà présent en v0.3.12b)*

Intégré dans ce patch pour consolidation. `@.str`, `@.str.1`, etc. sont désormais enregistrés sous clé `__objN::name` dans `global_syms`, et la résolution des relocs essaie d'abord la clé locale avant le scope global. Empêche `fopen(filename, "I_Error: %s\n")` au lieu de `fopen(filename, "rb")`.

### B11 — `emit_spill_store/reload` chemin 3-instructions *(amélioré)*

Le chemin 3-instructions (introduit en v0.3.12b) est maintenant cohérent avec la nouvelle formule B16. Les offsets négatifs hors `[-256, 0)` utilisent `D_MOV_I R25, offset + D_ADD R25=FP+R25 + D_STORE64 [R25+0]`.

---

## 3. Bugs Identifiés mais Non Résolus

### BUG-A — `W_AddFile` frame_size=520 (BUG B11 résiduel, Windows uniquement)

**Symptôme** : `W_AddFile` a 11 allocas (alloca_top ≈ 88) et génère ~37 spill slots en mode conservatif (phi présent via ExtendLumpInfo). `frame_size` final ≈ 520 > 256. Le chemin 3-instructions est utilisé pour les spills lointains, ce qui est correct en théorie, mais le comportement sur Windows reste à valider.

**Impact actuel** : inconnu sur Windows (précédent crash était à `addr=0x4` dans W_ReadLump, causé par `lumpinfo=4` — adresse probablement liée à une corruption en cascade depuis W_AddFile).

**Priorité** : tester le patch v0.3.13 sur Windows et observer si le crash a évolué.

### BUG-B — `ExtendLumpInfo` reçoit numlumps=0 (Linux sandbox)

**Symptôme** : après application du patch v0.3.13, la VM Linux atteint `ExtendLumpInfo` mais `calloc(0, 40)` retourne NULL → `I_Error: Couldn't realloc lumpinfo`.

**Analyse** :
- La séquence correcte dans W_AddFile : lire `wadinfo_t.numlumps` (= 2 depuis le WAD de test), puis appeler `ExtendLumpInfo(numlumps_local)`.
- Le watchpoint VM confirme que `@lumpinfo` reçoit bien `0x80100000` (calloc de ExtendLumpInfo), et que `@numlumps` est correctement écrit avec valeur non-nulle → le bug est **en amont**.
- Le paramètre R0 passé à ExtendLumpInfo vient d'un alloca de W_AddFile via la nouvelle formule. Si W_AddFile a un alloca mal placé (son alloca_top = 88, et ses spill slots commencent à `-(88+8)=-96`), une collision résiduelle pourrait corrompre la valeur locale de `numlumps_from_wad`.

**Hypothèse principale** : W_AddFile lit correctement `numlumps=2` depuis le WAD header (via `D_LOAD32 R? ← [wadinfo_ptr + 4]`), mais une collision de slot entre alloca et spill dans W_AddFile écrase cette valeur avant qu'elle arrive comme paramètre à `ExtendLumpInfo`.

**Différence Linux/Windows** : les allocas de W_AddFile changent d'offsets avec le patch B15/B16. Sur Linux le crash est à `I_Error`, sur Windows il était à `addr=0x4` → deux manifestations différentes du même bug de corruption.

**Piste d'investigation** :
```python
# Ajouter watchpoint STORE32 dans la plage @numlumps
# ET tracer la valeur de R0 juste avant le F_CALL → ExtendLumpInfo
# Dans run_pipeline.py Windows: vérifier que le rapport montre calloc syscall
```

---

## 4. Architecture — Frame Layout (v0.3.13)

```
FP + 0           : LR (sauvé par A_ENTER)
FP - 8           : alloca N-1  (slot = alloca_top - 8)
...
FP - alloca_top  : alloca 0    (slot = 0, premier alloca du pre-pass)
FP - alloca_top - 8  : spill slot 0   (slot = alloca_top)
FP - alloca_top - 16 : spill slot 1   (slot = alloca_top + 8)
...
FP - frame_size  : SP final (= FP - ra.spill_top)
```

Formules :
```
alloca fp_offset = slot - alloca_top               (invariant, ne change pas)
spill  fp_offset = -(slot + 8)                     (invariant, slot >= alloca_top)
frame_size final = ra.spill_top = alloca_top + N*8 (N spill slots)
```

---

## 5. Invariants Critiques (rappel)

| Invariant | Où | Conséquence si violé |
|-----------|----|-----------------------|
| `libc_symbols.rs` IDs = `libc/mod.rs` IDs | tsk-cc + tsk-link | symbole résolu à adresse 0 → crash immédiat |
| Alloca : `fp_offset = slot - alloca_top` | codegen.rs `load_reg_or_imm` | reads/writes à mauvaises adresses stack |
| Spill : `offset = -(slot + 8)` | codegen.rs `emit_spill_store/reload` | collision alloca↔spill → corruption silencieuse |
| Symboles privés : clé `__objN::name` | tsk-link `global_syms` | string literals partagées entre objets |
| Pas de réutilisation de `frame_size` avant patch | tous | frame_size vaut `alloca_top` pendant la génération |

---

## 6. Prochaines Priorités

1. **Windows** : appliquer `TriskeleToolchain_patch_v0313.zip`, lancer `run_pipeline.py Doom-Generic/vm-porting/tests/doom_wad`, uploader `pipeline_report.txt`. Observer si le crash est passé de `addr=0x4` à quelque chose de nouveau (progrès) ou à `I_Error` (même état que Linux).

2. **BUG-B** : investiguer pourquoi `ExtendLumpInfo` reçoit `numlumps=0`. Ajouter un `printf` minimal dans `doom_wad_stubs.h` (I_Error override) pour afficher la valeur numlumps avant l'appel, **sans** augmenter la taille de `main` (utiliser une fonction C séparée pour éviter les side-effects sur les alloca).

3. **W_AddFile alloca_top** : vérifier avec `-v` de `tsk-cc` que le pre-pass 1 compte bien 11 allocas × 8 = 88 bytes pour alloca_top, et que les spill offsets ne chevauchent pas les allocas.

4. **Bump version** : `Cargo.toml` workspace → `0.3.13` (actuellement `0.3.10`).

---

## 7. Commandes de Référence (Linux sandbox)

```bash
# Build
cd /home/claude && cargo build -p tsk-cc -p tsk-link -p triskele-vm

# Pipeline doom_wad
BASE=projects/Doom-Generic/vm-porting/tests/doom_wad
INC="-I$BASE/include -I$BASE/src"
for src in z_zone m_argv w_file_stdc w_file w_wad test_doom_wad; do
  clang -O0 -emit-llvm -S $INC $BASE/src/${src}.c -o /tmp/${src}.ll 2>/dev/null
  target/debug/tsk-cc /tmp/${src}.ll -o /tmp/${src}.tobj 2>/dev/null
done
target/debug/tsk-link /tmp/z_zone.tobj /tmp/m_argv.tobj /tmp/w_file_stdc.tobj \
  /tmp/w_file.tobj /tmp/w_wad.tobj /tmp/test_doom_wad.tobj -o /tmp/doom_wad.tvmx 2>/dev/null
target/debug/tskvm /tmp/doom_wad.tvmx; echo "exit: $?"

# Vérifier frame sizes dans un tobj
python3 -c "
import struct
data = open('/tmp/w_wad.tobj', 'rb').read()
for i in range(0, len(data)-3, 4):
    w = struct.unpack_from('<I', data, i)[0]
    if w == 0x08000000:
        w1 = struct.unpack_from('<I', data, i+4)[0]
        if (w1>>24)&0xFF == 0x41:
            print(f'A_ENTER file[0x{i:X}]: frame={w1&0x7FFFF}')
"
```

---

*TriskeleToolchain Handover v0.3.13 — Echopraxium with the collaboration of Claude AI*
