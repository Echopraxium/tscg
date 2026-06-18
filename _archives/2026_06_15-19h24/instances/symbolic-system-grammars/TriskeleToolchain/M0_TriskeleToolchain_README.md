# TriskeleToolchain — Design Process & Specification README

**Author**: Echopraxium with the collaboration of Claude AI  
**Version**: 0.2.0  
**Date**: 2026-05-31  
**Status**: Specification complete — Implementation pending  
**Path**: `instances/symbolic-system-grammars/TriskeleToolchain/`

---

## 1. Genèse du projet

### 1.1 L'idée initiale

Le projet TriskeleToolchain est né de l'intuition que les **16 types monoïdaux
de la Grammaire Structurelle TSCG** (couche M3) pourraient servir de fondement
naturel à un jeu d'instructions de machine virtuelle — une forme de "Base16
sémantique" où chaque chiffre hexadécimal correspond à un primitif M3.

```
Gt (Territory/ASFID) × 5  →  A  St  F  It  D      hex 0x0–0x4
Gm (Map/REVOI)       × 5  →  R  E   V  O   Im     hex 0x5–0x9
Gs (Stereopsis/TKSL) × 6  →  T  _^  _$ K   Ss  L  hex 0xA–0xF
────────────────────────────────────────────────────────────────
Total: 16 primitifs = 1 nibble = Base16
```

L'asymétrie 5-5-6 de Gs n'est pas arbitraire : les 3 primitifs K, Ss, L
ont été identifiés indépendamment pour résoudre **17 collisions de formules**
dans M2 GenericConcepts. Le fait que 5+5+6 = 16 est une **validation
structurelle a posteriori** — la complétude Base16 est une conséquence de
l'expressivité M2, pas un choix de design.

### 1.2 Objectif PoC

```
Phase 1 : Wolfenstein 3D (1992, id Software — open source)
  → compilateur C → TriskeleVM bytecode
  → SDL2 via Im_FFI_CALL + Im_REGISTER_CB
  → 35fps via T_FRAME_SYN
  → raycaster via D_FIXMUL (virgule fixe 16.16)

Phase 2 : Doom (1993, id Software — open source)
  → même ISA, même tsk-cc
  → format WAD via Im_FILE_RD
  → BSP via F_CALL récursif + F_LOOP
  → Z_Malloc via _^_ARENA_B / _$_ARENA_E
```

---

## 2. Architecture TriskeleToolchain

```
TriskeleToolchain  (m3:SymbolicSystemGrammar)
├── TriskeleVM        VM register-based (Rust)    ← M3 layer
│   └── ISA Base16: 16 catégories × 16 opcodes = 256 opcodes
├── tsk-asm           Assembleur (.tsk → .tobj)
├── tsk-dis           Désassembleur (.tvx → listing annoté)
├── tsk-link          Linker (.tobj + .tva + .tvl → .tvx)
├── tsk-cc            Compilateur C (.c → .tobj)   [Phase 2]
├── tsk-dbg           Debugger DAP (VS Code)        [Phase 2]
├── tsk-build         Orchestrateur (.tyml)
├── VS Code plugin    Syntaxe + DAP + LSP + M3 hex  [Phase 2]
└── TriskeleL         Langage haut niveau (M2)      [Phase 4]
```

---

## 3. Le Stress Test ISA — Processus de révision sémantique

### 3.1 Principe

Chaque catégorie d'opcodes doit être **déductible** de la sémantique M3
de son primitif monoïdal. La motivation ne vient **pas** des GenericConcepts
M2 (qui sont des types dérivés), mais de la sémantique intrinsèque du
primitif dans son monoïde.

### 3.2 La question transdisciplinaire comme outil

```
Gt (Territory ×)
  A  → "Où convergent les données ?"
  St → "Comment sont-elles organisées ?"
  F  → "Comment s'écoule l'exécution ?"
  It → "Quel est l'état informationnel ?"
  D  → "Qu'est-ce qui les modifie ?"

Gm (Map +)
  R  → "Peut-on encoder autrement ?"
  E  → "Génère-t-il de la nouveauté structurelle ?"
  V  → "Peut-on vérifier/falsifier ?"
  O  → "Peut-on mesurer internement ?"
  Im → "Peut-on interfacer ?"

Gs (Stereopsis |)
  T  → "Quand ?"
  _^ → onset/activation (modificateur de polarité)
  _$ → terminus/dissolution (modificateur de polarité)
  K  → "Que sait-on ?"
  Ss → "Quel est le signe ?"
  L  → "Vers quel attracteur converge-t-on ?"
```

### 3.3 Révisions majeures issues du stress test

**F_ — flux d'exécution (pas arithmétique)**
```
F = "ce qui s'écoule" — transdisciplinaire.
En biologie = flux sanguin. En informatique = fil d'exécution.
"Flow Control" (JMP, CALL, RET, IF) est bien du F_.
Les coroutines (YIELD) sont aussi F_ : flux alternatif.
```

**A_ — Pile + Tas (deux attracteurs mémoire)**
```
A = point de convergence/attraction (pas forcément stable).
La Pile et le Tas sont deux puits gravitationnels mémoire :
  Stack → attracteur LIFO déterministe
  Heap  → attracteur dynamique non déterministe
```

**St_ — types et structs (pas LOAD/STORE)**
```
St = organisation spatiale statique.
Un type struct EST une organisation spatiale.
NOP = préservation pure de la structure.
LOAD/STORE → D_ (modification). PUSH/POP → A_ (attracteur).
```

**It_ — état informationnel + events + IRQ**
```
It = contenu encodé / état informationnel.
Un flag est de l'information encodée.
Un événement est un changement d'information d'état.
Bitwise (AND, OR, XOR) → D_ (modification brute).
```

**D_ — toute modification**
```
D = "ce qui modifie l'état du système".
MOV, LOAD, STORE, ADD, MUL, AND, OR, XOR → tous D_.
Distinction : modification BRUTE (D_) vs changement d'état
NOMMÉ et signifiant (It_SET_FLAG).
```

**E_ — auto-transformation + GC adaptatif**
```
E = "génère-t-il de la nouveauté structurelle ?"
LOAD_MOD, HOOK, PATCH → nouvelles capacités/comportements.
E_MEM_ARENA → nouvelle stratégie mémoire (Z_Malloc de Doom).
Note : E_ est le primitif Gm le plus délicat — Gm décrit des
qualités épistémiques du Modèle, pas des opérations territoire.
```

**L_FAR_CALL → L_ (pas F_)**
```
F_CALL cible proche (±8MB) → flux dominant.
L_FAR_CALL cible 64b → localisation dominante.
La localisation précède et conditionne le flux.
```

---

## 4. Notation définitive — Convention obligatoire

```
St_   Structure       (Territory/Gt)   — JAMAIS S_
It_   Information     (Territory/Gt)   — JAMAIS I_
Ss_   Symbol          (Stereopsis/Gs)  — JAMAIS S_
Im_   Interoperability (Map/Gm)        — JAMAIS I_
```

---

## 5. Tableau définitif des 16 catégories

```
Monoïde  Hex   Cat.   Question M3                   Exemples opcodes
──────────────────────────────────────────────────────────────────────
Gt  ×    0x0_  A_     Où convergent les données ?   PUSH,POP,ALLOC,FREE
         0x1_  St_    Comment organisées ?           DEF_STRUCT,SIZEOF,NOP
         0x2_  F_     Comment s'écoule l'exec ?      JMP,CALL,RET,JZ,YIELD
         0x3_  It_    Quel état informationnel ?      SET_FLAG,EMIT,IRQ_ON
         0x4_  D_     Qu'est-ce qui modifie ?        MOV,LOAD,STORE,ADD,AND

Gm  +    0x5_  R_     Encodable autrement ?          I2F,F2FIX,SIGN,PACK
         0x6_  E_     Génère de la nouveauté ?        LOAD_MOD,HOOK,MEM_ARENA
         0x7_  V_     Vérifiable/falsifiable ?        CMP,ASSERT,RANGE,NULL
         0x8_  O_     Mesurable internement ?         DUMP,TRACE,BREAK,WATCH
         0x9_  Im_    Interfaçable ?                  FFI_CALL,FB_BLIT,REG_CB

Gs  |    0xA_  T_     Quand ?                        TICK,FRAME_SYN,TIMER
         0xB_  _^_    Onset/activation ?             NEW_OBJ,SPAWN,ARENA_B
         0xC_  _$_    Terminus/dissolution ?          DEL_OBJ,KILL,ARENA_E
         0xD_  K_     Que sait-on ?                  TYPEOF,IS_A,SCHEMA
         0xE_  Ss_    Quel signe ?                   INTERN,LOOKUP,PI,NULL_T
         0xF_  L_     Vers quel attracteur ?          LEA,DEREF,FAR_CALL
```

---

## 6. Distinctions sémantiques clés

```
Ss_ vs It_    signe (identifiant "main") vs valeur (0x1000)
              Ss_LOOKUP résout Ss → It

St_ vs K_     structure statique (compile-time) vs
              connaissance réflexive (runtime)

D_ vs It_     modification brute vs changement d'état nommé
              D_STORE32 vs It_SET_FLAG

F_ vs L_      flux proche (±8MB) vs localisation lointaine (64b)
              F_CALL vs L_FAR_CALL

A_ vs _^_     attracteur mémoire (gravité) vs activation (onset)
              A_ALLOC vs _^_NEW_OBJ
```

---

## 7. Symétrie _^_ / _$_ — 14 paires sans orphelin

```
_^_NEW_OBJ ↔ _$_DEL_OBJ     _^_SPAWN   ↔ _$_KILL
_^_NEW_STR ↔ _$_DEL_STR     _^_OPEN_CH ↔ _$_CLOSE_CH
_^_NEW_ARR ↔ _$_FREE_ARR    _^_PUSH_FR ↔ _$_POP_FR
_^_PIN     ↔ _$_UNPIN       _^_NEW_CTX ↔ _$_DEL_CTX
_^_REF_INC ↔ _$_REF_DEC     _^_LOCK    ↔ _$_UNLOCK
_^_OPEN_SC ↔ _$_CLOSE_SC    _^_ALLOC_P ↔ _$_FREE_P
_^_ARENA_B ↔ _$_ARENA_E     _^_ACTIVATE↔ _$_DEACT
```

---

## 8. Ce que le stress test démontre pour TSCG

**① Les 16 primitifs sont suffisants et non redondants**
256 opcodes couvrent une VM complète (Wolf3D + Doom) sans forcer
ni inventer de catégorie. Aucun chevauchement après révision.

**② La transdisciplinarité est opérationnelle**
F_ = flux d'exécution = même structure abstraite que flux sanguin,
flux financier, flux thermique. Pas une métaphore — même concept.

**③ La symétrie _^_/_$_ est une validation**
14 paires exactes sans résidu → pôles structurellement complets.

**④ Validation croisée K, Ss, L**
Les 3 primitifs Gs qui résolvent 17 collisions M2 sont les mêmes
qui complètent la Base16 de l'ISA. Double validation indépendante.

**⑤ Argument anti-Brainfuck**
Chaque catégorie d'opcodes est déductible de la sémantique M3
de son primitif. L'ISA est déduit de la Grammaire Structurelle,
pas inventé ad hoc.

---

## 9. Changelog

```
v0.2.0  2026-05-31
  ISA mapping révisé (stress test sémantique complet).
  Notation obligatoire St_/It_/Ss_/Im_.
  Ss_=signes (pas valeurs It_). 14 paires _^_/_$_ formalisées.
  Structure Cargo workspace initiée.

v0.1.0  2026-05-30
  Release initiale. ISA 256 opcodes, format .tvm/.tvx,
  registres 32×64b, tsk-asm/tsk-dis/tsk-link, scores ASFID/REVOI.
```

---

*TriskeleToolchain — Design Process & Specification README v0.2.0*
*Echopraxium with the collaboration of Claude AI — 2026-05-31*
