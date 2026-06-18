# TriskeleToolchain — Handover v0.3.6
**Date**: 2026-06-09  
**Auteur**: Echopraxium with the collaboration of Claude AI  
**Repo**: https://github.com/Echopraxium/tscg  
**Chemin local**: `E:\_00_Michel\_00_Lab\_00_GitHub\tscg\instances\symbolic-system-grammars\TriskeleToolchain\`

---

## Statut actuel — ✅ SEXTUPLE VALIDATION

| Projet | Type | Exit | Tests |
|--------|------|------|-------|
| `test_main` | C89 | 31 ✅ | ScaleDiv(10,2), ScaleDiv(7,0), IsSolid(3,5), IsSolid(0,0), SumTiles |
| `wolf3d` | C89 | 15 ✅ | ScaleDiv, IsSolid, MoveActor (fixed-point 16.16), SumTiles |
| `test_patterns` | C89 | 15 ✅ | switch, function pointers, 2D array, pointer arithmetic |
| `test_select` | C89 | 9 ✅ | select (ternaire C), memset, memcpy, clamp, abs, max, min |
| `doom_fixed` | C89 | 127 ✅ | FixedMul×3, FixedDiv×4 |
| `doom_alloc` | C89 | 255 ✅ | Zone allocator Z_Malloc/Z_Free — **NOUVEAU v0.3.6** |

> ⚠️ `doom_alloc` validé exit 255 sur la VM Linux de développement.
> Validation Windows en attente (patch_v036.zip à appliquer).

---

## Tous les changements en v0.3.6

### Nouveau projet `doom_alloc`

Zone Memory Allocator inspiré de `z_zone.c` de DoomGeneric, standalone (sans `I_Error`/`printf`).

Structure :
```
projects/doom_alloc/
  include/doom_alloc.h      ← memblock_t, memzone_t, PU_*, ZONEID — standalone
  src/doom_alloc.c          ← Z_Init, Z_ClearZone, Z_Malloc, Z_Free, Z_FreeMemory
  src/doom_alloc_test.c     ← 8 tests, exit bitmask 255
  pipeline.toml             ← expected_exit = 255
```

Nouveaux patterns LLVM IR validés :

| Bit | Test | Pattern IR validé |
|-----|------|-------------------|
| 0 | Z_Malloc non-NULL | `icmp eq ptr` — comparaison de pointeurs (boucle do/while) |
| 1 | Z_Free *user=0 | `GEP i8, ptr, i64 -40` — offset négatif (byte cast) |
| 2 | *block->user==p3 | `store ptr` via double indirection |
| 3 | p2 > p1 | `icmp ugt ptr` — split de bloc, MINFRAGMENT |
| 4 | prev coalesce | do/while + phi + break sur ptr |
| 5 | next coalesce | coalesce bidirectionnelle |
| 6 | Z_FreeMemory | boucle while avec sentinelle ptr |
| 7 | alloc-after-free | rover logic, réutilisation de bloc libéré |

---

### Fix 1 — `tsk-cc/codegen.rs` : `Store` double-usage et register pressure

**Bug A** : `free_name(val)` appelé après le premier `store` alors que `val` était réutilisé dans un second `store` immédiat :
```llvm
%58 = load ptr, ptr %57
store ptr %58, ptr %10   ← free_name("%58") ← registre libéré !
store ptr %58, ptr %12   ← %58 plus dans ra.map → undefined SSA
```

**Bug B** : Le pointeur de destination d'un `store` (ex: `%9 = GEP...`) n'était jamais libéré → accumulation dans les blocs denses → register spill dans `Z_ClearZone` (52 instructions, bloc unique).

**Fix** : Pré-calcul dans `gen_block` d'un `multi_use: HashSet<String>` = SSA utilisées > 1 fois dans le bloc. `free_name` conditionné sur l'absence dans `multi_use`, pour `val` ET `ptr`.

```rust
// gen_block: pré-calcule les SSA multi-use du bloc courant
let mut use_count: HashMap<String, usize> = HashMap::new();
for instr in &block.instrs {
    for name in instr_uses(instr) {
        *use_count.entry(name).or_insert(0) += 1;
    }
}
let multi_use: HashSet<String> = use_count.into_iter()
    .filter(|(_, c)| *c > 1).map(|(n, _)| n).collect();
```

`gen_instr` reçoit `multi_use: &HashSet<String>` comme paramètre supplémentaire.

---

### Fix 2 — `tsk-cc/parser.rs` : constante `inttoptr` inline dans `Store`

**Bug** : `store ptr inttoptr (i64 1 to ptr), ptr %6` (de `owner1 = (void*)1` en C89) générait `undefined SSA '%inttoptr'` car le parser traitait `inttoptr` comme un nom de registre SSA.

**Fix** : Reconnaissance dans `parse_value` :
```rust
"inttoptr" => {
    self.eat(&Tok::LParen);
    let _ = self.parse_type();   // i64
    let val = self.parse_value()?; // N
    // skip "to ptr"
    while !matches!(self.peek(), Tok::RParen | Tok::Eof) { self.advance(); }
    self.eat(&Tok::RParen);
    Ok(val)  // inttoptr(i64 N) → Value::Const(N)
}
```
Idem pour `ptrtoint`.

---

### Fix 3 — `tsk-cc/ir.rs` + `codegen.rs` : `IrType::Named` pour les types imbriqués

**Bug (cause racine)** : `%struct.memzone_t = { i32, %struct.memblock_s, ptr }`. Lors du premier pass du parser, `%struct.memblock_s` n'est pas encore défini → résolu comme `IrType::I64` (8 bytes) au lieu de `Struct([I32, Ptr, I32, I32, Ptr, Ptr])` (36 bytes). Conséquence : tous les offsets de champs de `memzone_t` étaient calculés faux (champ `rover` à offset 12 au lieu de 28) → `mainzone->rover` pointait vers une zone arbitraire → `Z_Malloc` retournait NULL → `Z_Free(NULL)` → memory fault.

**Fix** : Ajout de `IrType::Named(String)` dans `ir.rs` :
```rust
pub enum IrType {
    // ... existants ...
    Named(String),  // forward reference, résolu par resolve_type
}
```

Parser : émettre `Named(name)` au lieu de `I64` pour les types non encore définis.

`resolve_type` étendu pour résoudre `Named` via `type_defs` et résoudre récursivement les champs de structs :
```rust
IrType::Named(name) => {
    if let Some(resolved) = self.type_defs.get(name.as_str()) {
        self.resolve_type(resolved)
    } else {
        IrType::I64  // fallback conservatif
    }
}
IrType::Struct(fields) => {
    let resolved = fields.iter().map(|f| self.resolve_type(f)).collect();
    IrType::Struct(resolved)
}
```

---

### Fix 4 — `tsk-link/src/main.rs` : entry point et grandes adresses

**Bug A — Entry point** : `tsk-link` sans `--entry` choisissait la première fonction du premier `.tobj` (= `Z_ClearZone`) au lieu de `main`. Le stub VM `F_CALL → Im_EXIT` sautait donc sur `Z_ClearZone`, résultant en une boucle infinie ou un stack overflow.

**Fix** : Auto-détection de `@main` si `--entry` non spécifié :
```rust
} else if let Some(&addr) = self.global_syms.get("main") {
    // Auto-detect: use @main if present
    addr
} else {
    // Fallback: première fonction du premier objet
    ...
}
```

**Bug B — Grandes adresses globales** : `D_MovI` patchée avec troncature à 19 bits pour les adresses > 262143 (fréquent sur Windows où le binaire est plus grand). `heap_buf` à adresse > `0x3FFFF` recevait 0 → `Z_Init(NULL, 4096)` → memory fault.

**Fix** : Séquence 5-instructions pour les adresses > `0x3FFFF` :
```
D_MovI dst, hi16
D_MovI R24, 16
D_Shl  dst, dst, R24
D_MovI R24, lo16
D_Or   dst, dst, R24
```
Utilise le slot de 20 bytes pré-réservé par `split_const32` dans `tsk-cc`.

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
| phi nodes multi-blocs | ✅ | doom_fixed |
| sext i32→i64 / trunc i64→i32 | ✅ | doom_fixed |
| sdiv i64 | ✅ | doom_fixed |
| zext i1→i64 | ✅ | doom_fixed |
| **icmp eq/ugt ptr** | ✅ | doom_alloc |
| **GEP i8 offset négatif** | ✅ | doom_alloc |
| **store ptr (double indirection)** | ✅ | doom_alloc |
| **do/while + boucle sur pointeur sentinelle** | ✅ | doom_alloc |
| **inttoptr constant expression** | ✅ | doom_alloc |
| **structs imbriquées (Named forward ref)** | ✅ | doom_alloc |

---

## Fichiers modifiés en v0.3.6

```
crates/tsk-cc/src/ir.rs          ← IrType::Named(String) ajouté
crates/tsk-cc/src/parser.rs      ← Named au lieu de I64 (forward ref) + inttoptr/ptrtoint const expr
crates/tsk-cc/src/codegen.rs     ← multi_use intra-bloc + Store free_name conditionnel + resolve_type étendu
crates/tsk-link/src/main.rs      ← auto-detect @main + D_MovI large addr (5-instr sequence)
projects/doom_alloc/              ← NOUVEAU projet
  include/doom_alloc.h
  src/doom_alloc.c
  src/doom_alloc_test.c
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
    doom_fixed/           ← ✅ exit 127 (FixedMul, FixedDiv)
    doom_alloc/           ← ✅ exit 255 (Zone allocator Z_Malloc/Z_Free — NOUVEAU v0.3.6)
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

### Priorité 1 — Sentinelle `0xDEADBEEF` dans triskele-vm
Initialiser toute la mémoire non-allouée avec `0xDEADBEEF` au démarrage. Permet de détecter immédiatement les déréférencements de pointeurs invalides (au lieu de tomber silencieusement dans des zones de zéros → `A_PUSH` infinis ou stack overflow non diagnosticable). Inspiré des pratiques IBM/debug classiques.
- Fichier : `triskele-vm/src/memory/mod.rs` ou `main.rs`
- Impact : rendre les crashes de la VM auto-documentés

### Priorité 2 — `z_zone.c` complet (DoomGeneric)
Compiler le vrai `z_zone.c` avec stubs `I_Error`/`I_ZoneBase` une fois les patterns de `doom_alloc` validés sur Windows. Nécessite `printf` → tsk-libc.

### Priorité 3 — tsk-libc
`malloc`, `free`, `printf`, `memset`, `memcpy` (stubs VM déjà présents pour memset/memcpy).

### Priorité 4 — Fix `D_Shl` avec constante immédiate (`tsk-cc/codegen.rs`)
`split_const32` émet `D_MovI hi + D_Shl 16` mais encode le shift comme s2=0 → le fallback `_flags` est utilisé, qui est aussi 0 → shift nul → résultat faux. Fix : émettre `D_MovI R_scratch2, 16 + D_Shl dst, src, R_scratch2` en passant explicitement le registre scratch en s2.

### Priorité 5 — Fix `tsk-asm` symtab format
Format attendu par `tsk-link` : `name\0` puis `u32 offset`. Actuellement inversé dans `tsk-asm`.

---

## Backlog architectural

### Registres "smart pointer" avec flags
Formaliser l'allocation/libération avec états : `FREE`, `OWNED`, `BORROWED`, `PINNED`.
- `PINNED` = équivalent de `protected` actuel, mais formalisé avec instrumentation
- Prérequis pour un futur allocateur par graphe de coloration

### Register spill sur stack
Quand les 32 registres physiques sont saturés, spiller vers la stack.
- Pas urgent (max ~9 registres actifs avec le liveness unifié)
- Nécessaire pour les fonctions C très complexes

---

## Notes techniques importantes

### multi_use intra-bloc (v0.3.6)
- `multi_use` calculé **une fois par bloc** dans `gen_block`, passé en paramètre à `gen_instr`
- Cas couverts : `store val` utilisé plusieurs fois, `store ptr` (GEP intermédiaire) single-use
- `alloca_slots` sont explicitement exclus du `free_name` sur `ptr` (ils ne sont jamais dans `ra.map`)
- Coût : O(n) sur les instructions du bloc — négligeable

### IrType::Named (v0.3.6)
- Utilisé exclusivement pour les références forward dans les définitions de structs
- `byte_size()` retourne 8 comme fallback conservatif (ne doit jamais être appelé avant `resolve_type`)
- `resolve_type` est récursif sur les champs de `Struct` → résout les chaînes d'imbrication arbitraires
- Aucun changement de format binaire `.tobj`/`.tvmx`

### tsk-link entry point (v0.3.6)
- Priorité : `--entry <name>` > auto-detect `@main` > première fonction du premier objet
- `run_pipeline.py` n'a pas besoin de passer `--entry` pour les projets C standard

### D_MovI large address (v0.3.6)
- Seuil : `addr > 0x3FFFF` (262143) → séquence 5 instructions
- Requiert que `tsk-cc` ait réservé 20 bytes via `split_const32` à l'emplacement de la relocation
- Sur Linux (binaire < 262KB) : chemin simple, pas de séquence étendue nécessaire
- Sur Windows (binaire > 262KB) : séquence étendue activée automatiquement

### Allocateur unifié (v0.3.5 — inchangé)
- `ra.protected` : phi-destinations uniquement — jamais recyclées
- `ra.params` : exclus du recyclage dans `get_or_alloc` ET `free_name`
- `ra.used` : high-water mark — doit rester ≤ 12 pour les fonctions normales

### D_Shl/D_Shr (v0.3.5 — inchangé)
- `s2 != 0` → shift depuis registre (chemin normal `tsk-cc`)
- `s2 == 0` → shift depuis `_flags` (legacy `tsk-asm`)
- **Cas à corriger (Priorité 4)** : `split_const32` laisse s2=0 → shift nul

### imm19 constraint
- Plage : `[-262144, 262143]`
- Valeurs hors plage → `split_const32` → `D_MovI hi + D_Shl 16 + D_Or lo`
- `D_Shl` avec s2=0 est cassé → éviter les grandes constantes dans les harness en attendant le fix
