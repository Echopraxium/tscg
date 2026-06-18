# TriskeleToolchain — Handover v0.3.14b

**Author**: Echopraxium with the collaboration of Claude AI  
**Date**: 2026-06-15  
**Patch**: `TriskeleToolchain_patch_v0314b.zip`  
**Workspace (Windows)**: `E:\_00_Michel\_00_Lab\_00_GitHub\tscg\instances\symbolic-system-grammars\TriskeleToolchain\`

---

## 1. Validation Baseline

### Stable (inchangé depuis v0.3.12b)

| Projet | Exit attendu | Statut |
|--------|-------------|--------|
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

### En cours

| Projet | Exit | Linux (sandbox) | Windows (v0.3.13) |
|--------|------|-----------------|-------------------|
| doom_wad | 255 | `I_Error: Couldn't realloc lumpinfo` (exit 1) | identique |

---

## 2. Bugs Corrigés Cette Session (v0.3.13 → v0.3.14b)

### B15 — Offsets alloca incohérents (`tsk-cc/src/codegen.rs`)

**Cause** : dans `load_reg_or_imm`, l'adresse d'un slot alloca était calculée par `fp_offset = slot - self.frame_size`. Or `frame_size` commence à `alloca_top` pendant la génération, puis est **patchée vers le haut** après allocation de tous les spill slots. Le prologue stockait les params à `[FP - petit_offset]` et les accès ultérieurs lisaient depuis `[FP - grand_offset]` → collision silencieuse.

**Fix** : nouveau champ `alloca_top: i32` enregistré après le pre-pass 1. Formule corrigée : `fp_offset = slot - self.alloca_top` (invariant).

### B16 — Formule spill incohérente (`tsk-cc/src/codegen.rs`)

**Cause** : `emit_spill_store/reload` utilisaient `offset = -(self.frame_size + slot + 8)`. Même problème : `frame_size` changeait entre le store et le reload.

**Fix** : formule directe `offset = -(slot + 8)`. Les spills commencent toujours à `[FP - (alloca_top + 8)]`, sans dépendance à `frame_size`.

**Layout résultant** :
```
FP + 0              : LR (sauvé par A_ENTER)
FP - 8              : dernière alloca (slot = alloca_top - 8)
FP - alloca_top     : première alloca (slot = 0)
FP - (alloca_top+8) : spill slot 0  (slot = alloca_top)
FP - (alloca_top+16): spill slot 1
...
FP - frame_size     : SP final
```

### B17 — Named struct byte_size fallback (`tsk-cc/src/codegen.rs`)

**Cause** : dans le pre-pass alloca, `ty.byte_size()` pour `IrType::Named("struct.wadinfo_t")` retournait **8** (fallback conservatif) au lieu de **12** (taille réelle `{[4xi8], i32, i32}`). Cela décalait de 8 bytes les slots de tous les allocas suivants dans `W_AddFile`, rendant la lecture du champ `numlumps` du header WAD impossible (slot wrong → valeur 0 → `calloc(0, 40)` → NULL).

**Fix** : une ligne dans le pre-pass :
```rust
// AVANT
let size = ty.byte_size().max(8) as i32;
// APRÈS
let resolved = self.resolve_type(ty);
let size = resolved.byte_size().max(8) as i32;
```

**Résultat** : `W_AddFile` lit correctement `numlumps=2` depuis le header WAD → `calloc(2, 40)` → 80 bytes alloués. Le code progresse jusqu'à `I_Error: Couldn't realloc lumpinfo` (nouveau bug).

### write_le32 simplifiée (`test_doom_wad.c`)

Pour réduire la pression sur le RA liveness, `write_le32` utilise maintenant un pointeur local `p = buf + offset` au lieu de recalculer `buf+offset+N` quatre fois séparément. Cela réduit le nombre de valeurs live simultanées (472 → 336 bytes de code généré).

---

## 3. Diagnostic du Bug Actuel : `calloc(nmemb=0, size=40)` dans ExtendLumpInfo

### Trace prouvée (Linux sandbox v0.3.14b)

```
1. build_test_wad() crée /home/claude/test_minimal.wad (60 bytes, correct)
   magic=IWAD, numlumps=2, infotableofs=28  ← vérifié

2. W_AddFile ouvre test_minimal.wad en lecture
   fopen("test_minimal.wad", "rb") → handle 0xF0000000  ← FILE_HANDLE_BASE+0, valide

3. W_StdC_Read appelle fread:
   [FSEEK] fp=0xF0000000 offset=0 whence=0  ← seek to pos 0
   [FREAD] ptr=0x6FFFFF28 sz=1 cnt=12 fp=0xF0000000  ← lit 12 bytes (header)
   → ptr=0x6FFFFF28 = FP_WAddFile - 80 = &wadinfo alloca  ← CORRECT

4. D_LOAD32 R15 ← [FP_WAddFile-76] → R15 = wadinfo.numlumps = 2  ← CORRECT

5. R16 = [FP_WAddFile-8] = numlumps_local (= 0 initialement)
   R17 = R16 + R15 = 0 + 2 = 2
   [FP_WAddFile-8] = R17 = 2  ← stocké correctement

6. R0 = [FP_WAddFile-8] = 2
   F_CALL ExtendLumpInfo  ← R0 = 2 à l'entrée de ExtendLumpInfo

7. Dans ExtendLumpInfo (prologue):
   D_MOV_I R24, -32
   D_ADD R24 = FP_EI - 32
   D_STORE32 [FP_EI-32] = R0  ← stocke param (2?) dans alloca %2
   ...
   D_LOAD32 R2 ← [FP_EI-32]  ← recharge
   D_MOV R0, R2               ← calloc arg1

8. [CALLOC] nmemb=0 size=40   ← BUG: R0=0 pas 2!
```

### Hypothèse du bug (B20)

Le RA liveness de `ExtendLumpInfo` génère un **store spill de R0 avant le prologue-store**, ou un **caller-save qui écrase [FP-32]** entre le store initial et le reload. Traces RA observées :

```
spill-store R0 → [FP-40]   (slot 32)   ← caller-save avant calloc
spill-store R0 → [FP-136]  (slot 128)  ← deuxième éviction de R0!
```

Deux évictions de R0 avec **slots différents** (32 et 128). La valeur rechargée après la deuxième éviction peut ne pas correspondre à `numlumps_new=2`.

**Piste prioritaire** : vérifier si R0 vaut 2 ou 0 au moment de `D_STORE32 [FP_EI-32] = R0` dans le prologue d'ExtendLumpInfo. Si R0=0, le bug est dans le passage depuis W_AddFile. Si R0=2, le bug est dans le reload depuis [FP-32].

---

## 4. Informations Clés du Binaire (Linux, v0.3.14b)

```
Adresses VM (tsk-link output):
  @W_AddFile          → 0x3BFC
  @ExtendLumpInfo     → 0x4798
  @W_StdC_OpenFile    → 0x342C
  @W_StdC_Read        → 0x36D4
  @W_ReadLump         → 0x509C

F_CALL ExtendLumpInfo dans W_AddFile → vm=0x4374
  0x4354: D_MOV_I R24, -8
  0x4358: D_ADD R24=FP-8
  0x435C: D_LOAD32 R0 ← [FP-8]   ← R0 = numlumps_new (devrait = 2)
  0x4360: D_MOV R24, R0
  0x4364: D_MOV R0, R24
  0x4368: D_MOV_I R25, -392       ← caller-save slot
  0x436C: D_ADD R25=FP-392
  0x4370: D_STORE64 [FP-392]=R0   ← spill R0
  0x4374: F_CALL → 0x4798

FILE_HANDLE_BASE = 0xF0000000 (dans triskele-vm/src/libc/mod.rs)
  fopen retourne 0xF0000000 + index → valeur VALIDE
  fp=0xF0000000 dans fread = premier handle = test_minimal.wad ← CORRECT

alloca_top W_AddFile = 96 (11 allocas dont wadinfo_t=16 bytes via B17)
alloca_top ExtendLumpInfo = 32 (4 allocas: %2,%3,%4,%5)
  alloca %2 (param numlumps_new): slot=0, fp_offset=-32 → [FP-32]
  spill slot 0: slot=32, offset=-(32+8)=-40 → [FP-40]
```

---

## 5. Architecture Frame Layout (v0.3.14b)

```
FP + 0              : LR
FP - alloca_top     : alloca[0]  (slot=0, fp_off=0-alloca_top)
...
FP - 8              : alloca[N-1] (slot=alloca_top-8)
FP - (alloca_top+8) : spill[0]   (slot=alloca_top, offset=-(slot+8))
FP - (alloca_top+16): spill[1]
...
FP - frame_size     : SP
```

Formules clés dans `codegen.rs` :
```rust
// Alloca address (invariant):
fp_offset = slot - self.alloca_top

// Spill store/reload (invariant):
offset_from_fp = -(slot + 8)   // slot >= alloca_top toujours

// Patch frame_size final:
frame_size = ra.spill_top       // = alloca_top + N×8 spill slots
```

---

## 6. Invariants Critiques

| Invariant | Localisation | Conséquence si violé |
|-----------|-------------|---------------------|
| `libc_symbols.rs` IDs = `libc/mod.rs` IDs | tsk-cc + tsk-link | symbole résolu à 0 → crash |
| `fp_offset = slot - alloca_top` | `codegen.rs` `load_reg_or_imm` | reads/writes mauvais slot stack |
| `spill_offset = -(slot + 8)` | `codegen.rs` `emit_spill_store/reload` | collision alloca↔spill |
| `resolve_type(ty).byte_size()` dans pre-pass alloca | `codegen.rs` | Named structs mal dimensionnées |
| `FILE_HANDLE_BASE = 0xF0000000` | `libc/mod.rs` | handles fp semblent invalides mais sont corrects |
| Symboles privés clé `__objN::name` | `tsk-link/main.rs` | string literals fusionnées entre objets |

---

## 7. Prochaines Priorités

### 1. Diagnostiquer B20 : R0=0 au calloc dans ExtendLumpInfo

**Action** : ajouter un watchpoint VM ciblé sur `[FP_EI-32]` (alloca du param dans ExtendLumpInfo) pour voir si le store initial met bien `2` ou `0` :

```rust
// Dans cpu/mod.rs, Opcode::D_Store32:
let pc = self.regs.pc();
if pc >= 0x4798 && pc <= 0x4900 {  // ExtendLumpInfo range
    eprintln!("[EI-STORE32] PC={:#X} [{:#X}]={}", pc, addr, v as i32);
}
```

Ou ajouter un printf dans `w_wad.c` `ExtendLumpInfo` :
```c
printf("DBG ExtendLumpInfo: new_numlumps=%d\n", new_numlumps);
```

**Hypothèse** : le RA liveness émet deux caller-saves de R0 avec slots 32 et 128. Le second spill stocke R0 avec une valeur différente de `numlumps_new=2`. Le reload de slot 128 produit 0.

### 2. Appliquer le patch Windows

- Patch : `TriskeleToolchain_patch_v0314b.zip`
- Builder, relancer `run_pipeline.py Doom-Generic/vm-porting/tests/doom_wad`
- Uploader `pipeline_report.txt`

### 3. Si B20 confirmé : corriger le RA liveness pour ExtendLumpInfo

**Options** :
- **A** : Corriger le slot mismatch dans le RA. Deux évictions de la même valeur → vérifier que la deuxième réutilise le même slot (si toujours in spill_map) ou alloue un nouveau slot avec la **bonne valeur** dans le registre.
- **B** : Seuil conservatif pour les fonctions avec phi nodes (ExtendLumpInfo en a : `%22 = phi i1 [false, %13], [%20, %17]`). Le mode conservatif ne recycle pas les registres → pas de slot mismatch.

Option B est plus rapide : `func_has_phi` est déjà détecté dans le codegen → activer le mode fully-conservatif (protection de tous les SSA defs) uniquement pour les fonctions phi. Vérifier que cela ne cause pas de CODEGEN FAILED pour ExtendLumpInfo (4 allocas + ~15 spill slots = 19 valeurs live max << 24 registres).

### 4. Bump versions

`Cargo.toml` workspace → version 0.3.14 (actuellement 0.3.10).

---

## 8. Commandes de Référence (Linux Sandbox)

```bash
# Build
cd /home/claude && cargo build -p tsk-cc -p tsk-link -p triskele-vm

# Pipeline doom_wad complet
BASE=projects/Doom-Generic/vm-porting/tests/doom_wad
INC="-I$BASE/include -I$BASE/src"
for src in z_zone m_argv w_file_stdc w_file w_wad test_doom_wad; do
  clang -O0 -emit-llvm -S $INC $BASE/src/${src}.c -o /tmp/${src}.ll 2>/dev/null
  target/debug/tsk-cc /tmp/${src}.ll -o /tmp/${src}.tobj 2>/dev/null
done
target/debug/tsk-link /tmp/z_zone.tobj /tmp/m_argv.tobj /tmp/w_file_stdc.tobj \
  /tmp/w_file.tobj /tmp/w_wad.tobj /tmp/test_doom_wad.tobj \
  -o /tmp/doom_wad.tvmx 2>/dev/null
target/debug/tskvm /tmp/doom_wad.tvmx; echo "exit: $?"

# RA debug log pour une fonction cible
RUST_LOG=tsk_cc=debug target/debug/tsk-cc /tmp/w_wad.ll -o /dev/null 2>&1 | \
  awk '/ExtendLumpInfo/{p=1} p{print} /W_NumLumps/{p=0}'

# Checker les frame_size dans un tobj
python3 -c "
import struct
data = open('/tmp/w_wad.tobj', 'rb').read()
for i in range(0, len(data)-3, 4):
    w = struct.unpack_from('<I', data, i)[0]
    if w == 0x08000000:
        w1 = struct.unpack_from('<I', data, i+4)[0]
        if (w1>>24)&0xFF == 0x41:
            fsz = w1 & 0x7FFFF
            print(f'A_ENTER file[0x{i:X}]: frame_size={fsz}', '>>> B11!' if fsz>256 else '')
"
```

---

*TriskeleToolchain Handover v0.3.14b — Echopraxium with the collaboration of Claude AI*
