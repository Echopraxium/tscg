# TriskeleVM — ISA Reference (Revised)

**Author**: Echopraxium with the collaboration of Claude AI
**Version**: 0.2.0
**Date**: 2026-05-31
**Status**: Draft — TriskeleToolchain
**Supersedes**: TriskeleVM_Format_TVM.md §8 (ISA section v0.1.0)

---

## 1. Notation Convention (Mandatory)

All category prefixes use the **indexed form** to eliminate ambiguity:

```
St_   Structure     (Territory/Gt)   — never S_
It_   Information   (Territory/Gt)   — never I_
Ss_   Symbol        (Stereopsis/Gs)  — never S_
Im_   Interoperability (Map/Gm)      — never I_
```

This convention mirrors M3 hybrid formula notation where Territory and
Map types carry their monoid index (St, It, O) to prevent ambiguity.

---

## 2. The 16 Opcode Categories — Mapping Définitif

Encoding: `opcode_byte = [4-bit category | 4-bit instruction_index]`

Each category is **semantically motivated** by its M3 primitive identity —
the ISA is *deduced* from the Structural Grammar, not invented ad hoc.

---

### Gt — Territory Grammar (monoïde ×)

```
0x0_  A_   Attractor
      M3 question : "Where do data converge?"
      Sémantique  : point de convergence/attraction
                    les 2 puits gravitationnels mémoire de la VM
      Couverture  : Pile (Stack — attracteur LIFO)
                    Tas  (Heap — attracteur dynamique)

      Pile (Stack attractor — LIFO)
        A_PUSH      empile registre → SP          (0x00)
        A_POP       dépile SP → registre           (0x01)
        A_PUSH_I    empile immédiat 32b → SP       (0x02)
        A_PEEK      lit sommet sans dépiler         (0x03)
        A_SWAP      échange les 2 premiers          (0x04)
        A_DUP       duplique le sommet              (0x05)
        A_DEPTH     profondeur de pile → reg        (0x06)
        A_STACK_F   crée frame d'activation         (0x07)
        A_ENTER     prologue procédure (auto)        (0x08)
        A_LEAVE     épilogue procédure (auto)        (0x09)

      Tas (Heap attractor — dynamique)
        A_ALLOC     alloue N bytes → ptr            (0x0A)
        A_ALLOC_Z   alloue N bytes zérisés → ptr    (0x0B)
        A_REALLOC   redimensionne bloc              (0x0C)
        A_FREE      libère bloc                     (0x0D)
        A_HEAP_SZ   taille heap disponible → reg    (0x0E)
        A_GC_RUN    force cycle GC                  (0x0F)

───────────────────────────────────────────────────────────────────
0x1_  St_  Structure
      M3 question : "How are data organized?"
      Sémantique  : organisation spatiale statique
                    types et structures de données
                    layout, topologie statique
      Couverture  : déclaration de types, layout mémoire,
                    NOP (préservation pure de la structure)

        St_NOP        no operation — structure préservée    (0x10)
        St_DEF_STRUCT définit type struct (champs+offsets)  (0x11)
        St_DEF_ARRAY  définit type tableau (élément+taille) (0x12)
        St_DEF_UNION  définit type union                    (0x13)
        St_DEF_ENUM   définit type énuméré                  (0x14)
        St_DEF_ALIAS  définit alias de type                 (0x15)
        St_FIELD_OFF  offset champ dans struct → reg        (0x16)
        St_ELEM_OFF   offset élément tableau → reg          (0x17)
        St_SIZEOF     taille type en bytes → reg            (0x18)
        St_ALIGNOF    alignement requis → reg               (0x19)
        St_STRIDE     pas d'itération tableau → reg         (0x1A)
        St_PACK       alignement compact (no padding)       (0x1B)
        St_UNPACK     alignement naturel                    (0x1C)
        St_ENDIAN     endianness d'un type (FFI C)          (0x1D)
        St_LAYOUT     layout complet d'un type → buffer     (0x1E)
        St_CAST_LAY   reinterpret_cast (reinterprète bytes) (0x1F)

───────────────────────────────────────────────────────────────────
0x2_  F_   Flow
      M3 question : "How does execution flow?"
      Sémantique  : flux d'exécution — tout ce qui modifie
                    l'ordre d'exécution des instructions
                    (transdisciplinaire : flux != flux physique)
      Couverture  : JMP/CALL/RET/IF/LOOP + coroutines
                    (une coroutine = flux d'exécution alternatif)

      Flux d'exécution principal
        F_JMP       saut inconditionnel (offset 24b)         (0x20)
        F_JMP_R     saut relatif (offset 16b signé)          (0x21)
        F_CALL      appel fonction (sauvegarde LR)           (0x22)
        F_RET       retour (restaure LR)                     (0x23)
        F_RET_N     retour + dépile N args                   (0x24)
        F_JZ        saut si zéro (flags)                     (0x25)
        F_JNZ       saut si non-zéro                         (0x26)
        F_JL        saut si inférieur (signé)                (0x27)
        F_JLE       saut si inférieur ou égal                (0x28)
        F_JG        saut si supérieur (signé)                (0x29)
        F_JGE       saut si supérieur ou égal                (0x2A)
        F_LOOP      décrémente CX, saute si CX≠0            (0x2B)
        F_SWITCH    saut table (reg, table_addr, N)          (0x2C)
        F_TRAP      exception/trap (code 8b)                 (0x2D)
        F_HALT      arrêt du flux VM                         (0x2E)

      Coroutines / fibres (flux alternatifs)
        F_YIELD     cède le flux courant (coopératif)        (0x2F)

───────────────────────────────────────────────────────────────────
0x3_  It_  Information
      M3 question : "What is the informational state?"
      Sémantique  : état informationnel du système
                    définition, test et changement d'état
                    événements, interruptions, callbacks
                    + valeurs encodées brutes (It = signifié)
      Note        : It_ vs Ss_ — la valeur encodée (It)
                    vs le signe qui la désigne (Ss)

      Définition d'état
        It_DEF_FLAG   définit flag nommé                     (0x30)
        It_DEF_STATE  définit état nommé (FSM)               (0x31)
        It_DEF_EVENT  définit type d'événement               (0x32)
        It_DEF_IRQ    définit interruption                   (0x33)

      Test d'état (lecture seule)
        It_GET_FLAG   lit flag → reg                         (0x34)
        It_TEST_FLAG  teste flag → bool                      (0x35)
        It_GET_STATE  état courant → reg                     (0x36)
        It_PENDING    événement en attente ? → bool          (0x37)

      Changement d'état
        It_SET_FLAG   active flag                            (0x38)
        It_CLR_FLAG   désactive flag                         (0x39)
        It_TOG_FLAG   bascule flag                           (0x3A)
        It_SET_STATE  transition vers nouvel état            (0x3B)

      Événements
        It_EMIT       émet événement                         (0x3C)
        It_SUBSCRIBE  s'abonne à événement                   (0x3D)
        It_UNSUB      se désabonne                           (0x3E)

      Interruptions / callbacks
        It_IRQ_ON     active interruption                    (0x3F)
        ; NOTE: It_IRQ_OFF, It_IRQ_SET, It_CALLBACK
        ;       → extension via E_FEATURE si > 16 opcodes

───────────────────────────────────────────────────────────────────
0x4_  D_   Dynamics
      M3 question : "What modifies data?"
      Sémantique  : toute modification brute d'état
                    registres, mémoire, contexte
                    arithmétique (modifie un registre)
                    bitwise (modifie l'encodage d'un registre)
      Note        : D_ vs It_ — modification brute sans
                    sémantique d'état (D_) vs changement
                    d'état nommé et signifiant (It_)

      Transfert registres/mémoire
        D_MOV       reg = reg                                (0x40)
        D_MOV_I     reg = imm32                             (0x41)
        D_MOV_I64   reg = imm64                             (0x42)
        D_XCHG      swap reg, reg                           (0x43)
        D_LOAD8     reg = mem8[reg+offset]                  (0x44)
        D_LOAD16    reg = mem16[reg+offset]                 (0x45)
        D_LOAD32    reg = mem32[reg+offset]                 (0x46)
        D_LOAD64    reg = mem64[reg+offset]                 (0x47)
        D_STORE8    mem8[reg+offset] = reg                  (0x48)
        D_STORE16   mem16[reg+offset] = reg                 (0x49)
        D_STORE32   mem32[reg+offset] = reg                 (0x4A)
        D_STORE64   mem64[reg+offset] = reg                 (0x4B)
        D_MEMCPY    memcpy(dst, src, n)                     (0x4C)
        D_MEMSET    memset(dst, val, n)                     (0x4D)

      Arithmétique entière (modifie un registre)
        D_ADD       reg = reg + reg                         (0x4E)
        D_SUB       reg = reg - reg                         (0x4F)
        ; NOTE: D_MUL, D_DIV, D_MOD, D_NEG, D_ABS,
        ;       D_INC, D_DEC, D_FIXMUL, D_FIXDIV,
        ;       D_MULDIV, D_SQRT → overflow géré
        ;       par encodage multi-octet (préfixe D_)

      Bitwise (modifie l'encodage d'un registre)
        ; D_AND, D_OR, D_XOR, D_NOT
        ; D_SHL, D_SHR, D_SAR, D_ROL, D_ROR
        ; D_BSET, D_BCLR, D_BTEST, D_POPCT

      Contexte d'exécution
        D_SAVE_CTX  sauvegarde contexte complet → buffer    (voir Fs)
        D_REST_CTX  restaure contexte depuis buffer         (voir Fs)
        D_CLR       reg = 0                                 (0x4E)
        D_FLAGS     reg = registre flags courant            (0x4F)

---

### Gm — Map Grammar (monoïde +)

```
0x5_  R_   Representability
      M3 question : "Can it be encoded in another notation?"
      Sémantique  : encodabilité sémantique
                    conversion entre représentations
                    sans perte de sens
      Couverture  : conversions de types numériques

        R_I2F       int32 → float32                         (0x50)
        R_F2I       float32 → int32 (tronqué)               (0x51)
        R_I2F64     int64 → float64                         (0x52)
        R_F2I64     float64 → int64                         (0x53)
        R_F32_64    float32 → float64                       (0x54)
        R_F64_32    float64 → float32                       (0x55)
        R_SIGN8     sign-extend byte → int32                (0x56)
        R_SIGN16    sign-extend word → int32                (0x57)
        R_ZERO8     zero-extend byte → int32                (0x58)
        R_ZERO16    zero-extend word → int32                (0x59)
        R_TRUNC     tronque float → int (vers zéro)         (0x5A)
        R_ROUND     arrondit float → int                    (0x5B)
        R_FIX2F     fixed 16.16 → float32                  (0x5C)
        R_F2FIX     float32 → fixed 16.16                  (0x5D)
        R_PACK      pack N valeurs en mot                   (0x5E)
        R_UNPACK    unpack mot en N valeurs                 (0x5F)

───────────────────────────────────────────────────────────────────
0x6_  E_   Evolvability
      M3 question : "Does it generate structural novelty?"
      Sémantique  : auto-transformation structurelle
                    du programme en cours d'exécution
                    + gestion mémoire adaptative
      Couverture  : modules dynamiques, hooks, patches,
                    stratégies GC, arènes mémoire

      Auto-modification / extension de capacités
        E_LOAD_MOD  charge module .tvl à chaud              (0x60)
        E_UNLOAD    décharge module                         (0x61)
        E_BIND      lie symbole externe → adresse locale    (0x62)
        E_CAPS      query capacités VM disponibles          (0x63)
        E_FEATURE   active feature runtime                  (0x64)
        E_FALLBACK  définit comportement alternatif         (0x65)
        E_PATCH     modifie instruction en mémoire          (0x66)

      Extension de comportements
        E_HOOK      installe hook sur événement VM          (0x67)
        E_UNHOOK    retire hook                             (0x68)
        E_VERSION   détecte version VM → adapte stratégie  (0x69)
        E_SANDBOX   entre mode restreint                    (0x6A)
        E_SNAPSHOT  capture état VM → buffer (rollback)     (0x6B)
        E_RESTORE   restaure état depuis snapshot           (0x6C)

      Gestion mémoire adaptative (Z_Malloc / Doom style)
        E_GC_CFG    reconfigure stratégie GC                (0x6D)
                    (manual/rc/incremental/generational)
        E_GC_TUNE   ajuste paramètres fins GC               (0x6E)
        E_MEM_POOL  crée pool mémoire dédié                 (0x6F)
        ; E_MEM_ARENA, E_MEM_STRAT, E_COMPACT
        ; → extension préfixe si besoin

───────────────────────────────────────────────────────────────────
0x7_  V_   Verifiability
      M3 question : "Can a condition be tested/falsified?"
      Sémantique  : vérification empirique au sens Poppérien
                    actes de vérification de conditions
      Note        : V_CMP produit des flags (résultat = It_)
                    mais l'ACTE de vérifier est V_

        V_CMP       compare reg, reg → flags                (0x70)
        V_CMP_I     compare reg, imm32 → flags              (0x71)
        V_TEST      AND logique → flags (sans stocker)      (0x72)
        V_EQ        reg = (reg == reg) ? 1 : 0              (0x73)
        V_NEQ       reg = (reg != reg) ? 1 : 0              (0x74)
        V_LT        reg = (reg <  reg) ? 1 : 0              (0x75)
        V_LTE       reg = (reg <= reg) ? 1 : 0              (0x76)
        V_GT        reg = (reg >  reg) ? 1 : 0              (0x77)
        V_GTE       reg = (reg >= reg) ? 1 : 0              (0x78)
        V_ASSERT    assert reg≠0 sinon trap                 (0x79)
        V_CHECK     vérifie bounds mémoire                  (0x7A)
        V_TYPE_EQ   vérifie type tag == expected            (0x7B)
        V_RANGE     reg in [min, max] ? 1 : 0               (0x7C)
        V_NULL      reg == NULL ? 1 : 0                     (0x7D)
        V_OVERFLOW  détecte overflow dernier calcul         (0x7E)
        V_PARITY    parité de reg → flag                    (0x7F)

───────────────────────────────────────────────────────────────────
0x8_  O_   Observability
      M3 question : "Can internal state be measured?"
      Sémantique  : rendre l'état interne observable
                    mesurabilité des variables d'état
      Couverture  : debug, introspection, profiling

        O_DUMP_REG  affiche tous les registres              (0x80)
        O_DUMP_STK  affiche N entrées pile                  (0x81)
        O_DUMP_MEM  dump mémoire [addr, n]                  (0x82)
        O_TRACE_ON  active trace instruction/instruction    (0x83)
        O_TRACE_OFF désactive trace                         (0x84)
        O_BREAK     breakpoint (DAP — VS Code)              (0x85)
        O_WATCH     watchpoint sur adresse mémoire          (0x86)
        O_LOG       log message (ptr string, len)           (0x87)
        O_PERF_RST  reset compteurs performance             (0x88)
        O_PERF_RD   lit compteur perf → reg                 (0x89)
        O_STACK_TR  stack trace symbolique                  (0x8A)
        O_COV_MARK  marque point couverture de code         (0x8B)
        O_INSP_HEAP inspecte état heap                      (0x8C)
        O_TIME_RD   lit timestamp VM (cycles)               (0x8D)
        O_ANNOTATE  annotation sémantique TSCG (.tscg)      (0x8E)
        O_NOP_D     NOP debug (→ O_BREAK en mode debug)     (0x8F)

───────────────────────────────────────────────────────────────────
0x9_  Im_  Interoperability
      M3 question : "Can it interface with other systems?"
      Sémantique  : compatibilité inter-systèmes
                    communication avec le host SDL2/libc
      Couverture  : FFI, syscalls, callbacks, I/O

        Im_SYSCALL      appel système host (id 16b)         (0x90)
        Im_FFI_CALL     appel C natif (ptr, sig_id)         (0x91)
        Im_FB_BLIT      blit framebuffer → écran host       (0x92)  ← Wolf3D
        Im_FB_CLEAR     efface framebuffer host             (0x93)
        Im_INPUT_RD     lit état clavier/souris host        (0x94)
        Im_AUDIO        envoi buffer audio host             (0x95)
        Im_FILE_RD      lecture fichier (fd, buf, n)        (0x96)
        Im_FILE_WR      écriture fichier                    (0x97)
        Im_FILE_OP      open/close/seek fichier             (0x98)
        Im_REGISTER_CB  enregistre callback VM←C           (0x99)  ← SDL2 events
        Im_UNREG_CB     retire callback                     (0x9A)
        Im_CB_INVOKE    invoque callback depuis VM          (0x9B)
        Im_MEM_MAP      mappe mémoire host → espace VM      (0x9C)
        Im_SHARED       mémoire partagée inter-VM           (0x9D)
        Im_TIME_HOST    lit horloge host (ms)               (0x9E)
        Im_EXIT         quitte VM proprement (code 8b)      (0x9F)
```

---

### Gs — Stereopsis Grammar (monoïde |)

```
0xA_  T_   Temporality
      M3 question : "When?"
      Sémantique  : interface temporelle Gt↔Gm
                    synchronisation entre exécution
                    (Territoire) et contraintes
                    temporelles (Carte/modèle)
      Couverture  : timing, synchronisation, timers

        T_TICK      lit compteur ticks VM interne           (0xA0)
        T_WAIT      attend N ticks                          (0xA1)
        T_SLEEP     dort N millisecondes host               (0xA2)
        T_YIELD     cède le CPU (coopératif)                (0xA3)
        T_TIMER_SET arme timer (id, délai, callback_addr)   (0xA4)
        T_TIMER_CLR annule timer                            (0xA5)
        T_FRAME_SYN synchronise sur frame rate cible        (0xA6)  ← Wolf3D 35fps
        T_DELTA     calcule delta depuis dernier T_TICK     (0xA7)
        T_TIMEOUT   teste si timer expiré                   (0xA8)
        T_PAUSE     suspend exécution VM                    (0xA9)
        T_RESUME    reprend exécution VM                    (0xAA)
        T_SCHED     planifie tâche à instant T              (0xAB)
        T_ATOMIC_B  début section atomique                  (0xAC)
        T_ATOMIC_E  fin section atomique                    (0xAD)
        T_BARRIER   barrière synchronisation multi-VM       (0xAE)
        T_WATCHDOG  reset watchdog (évite timeout)          (0xAF)

───────────────────────────────────────────────────────────────────
0xB_  _^_  Positive Pole (Onset)
      M3 rôle  : modificateur de polarité — onset/amplification
                 début d'existence d'une entité
      Sémantique: création / activation / émergence
                  faire émerger une entité dans l'espace
      Symétrie  : chaque opcode _^_ a un symétrique _$_

        _^_NEW_OBJ  crée objet (type_id, taille) → ptr      (0xB0)
        _^_NEW_STR  crée string (len + données) → ptr        (0xB1)
        _^_NEW_ARR  crée tableau typé [N × taille] → ptr     (0xB2)
        _^_CLONE    copie profonde objet → nouvel objet       (0xB3)
        _^_SPAWN    crée nouvelle coroutine/fibre             (0xB4)
        _^_OPEN_CH  ouvre canal communication inter-fibre     (0xB5)
        _^_PUSH_FR  pousse nouveau frame d'activation         (0xB6)
        _^_NEW_CTX  crée nouveau contexte d'exécution         (0xB7)
        _^_INTERN   interne string dans pool global           (0xB8)
        _^_PIN      épingle objet (empêche GC)                (0xB9)
        _^_REF_INC  incrémente compteur référence             (0xBA)
        _^_LOCK     acquiert verrou (mutex)                   (0xBB)
        _^_OPEN_SC  ouvre scope (RAII)                        (0xBC)
        _^_ALLOC_P  alloue dans pool dédié → ptr              (0xBD)
        _^_ARENA_B  début arène mémoire (Z_Malloc style)      (0xBE)
        _^_ACTIVATE active entité dormante                    (0xBF)

───────────────────────────────────────────────────────────────────
0xC_  _$_  Negative Pole (Terminus)
      M3 rôle  : modificateur de polarité — terminus/atténuation
                 fin d'existence d'une entité
      Sémantique: destruction / dissolution / libération
                  retourner une entité au néant
      Symétrie  : symétrique exact de _^_ (même ordre)

        _$_DEL_OBJ  détruit objet (appelle destructeur)      (0xC0)
        _$_DEL_STR  libère string                            (0xC1)
        _$_FREE_ARR libère tableau                           (0xC2)
        _$_KILL     termine coroutine/fibre                  (0xC3)
        _$_CLOSE_CH ferme canal communication                (0xC4)
        _$_POP_FR   dépile frame d'activation                (0xC5)
        _$_DEL_CTX  détruit contexte d'exécution             (0xC6)
        _$_UNPIN    désépingle objet (rend au GC)            (0xC7)
        _$_REF_DEC  décrémente compteur référence            (0xC8)
        _$_UNLOCK   libère verrou (mutex)                    (0xC9)
        _$_CLOSE_SC ferme scope (RAII)                       (0xCA)
        _$_FREE_P   libère dans pool dédié                   (0xCB)
        _$_ARENA_E  fin arène mémoire (libération en bloc)   (0xCC)
        _$_DEACT    désactive entité (mise en dormance)      (0xCD)
        _$_PURGE    vide pool/cache                          (0xCE)
        _$_ABORT    abandon immédiat sans cleanup            (0xCF)

───────────────────────────────────────────────────────────────────
0xD_  K_   Knowledge
      M3 question : "What is known?"
      Sémantique  : connaissance accumulée / réflexivité
                    la VM se connaît elle-même
                    contextualisation cognitive de It
      Note        : K_ vs It_ — la connaissance (K_)
                    vs la valeur brute (It_)
                    K_TYPEOF "que sait-on du type ?"
                    It_GET_FLAG "quelle est la valeur du flag ?"

        K_TYPEOF    type tag de la valeur → reg              (0xD0)
        K_SIZEOF    taille en bytes du type → reg            (0xD1)
        K_ALIGNOF   alignement requis du type → reg          (0xD2)
        K_FIELDS    nombre de champs objet → reg             (0xD3)
        K_FIELD_GET lit champ par index                      (0xD4)
        K_FIELD_SET écrit champ par index                    (0xD5)
        K_IS_A      test héritage/interface → bool           (0xD6)
        K_CAST      cast vérifié (trap si invalide)          (0xD7)
        K_SYM_LOOK  résout symbole nom → adresse             (0xD8)
        K_SYM_NAME  adresse → nom symbole (debug)            (0xD9)
        K_ANN_GET   lit annotation TSCG sur symbole          (0xDA)
        K_ANN_SET   pose annotation TSCG sur symbole         (0xDB)
        K_SCHEMA    retourne schéma type (JSON-LD ptr)       (0xDC)
        K_VALIDATE  valide objet vs schéma                   (0xDD)
        K_VERSION   version du type/module                   (0xDE)
        K_DESCRIBE  description textuelle type (debug)       (0xDF)

───────────────────────────────────────────────────────────────────
0xE_  Ss_  Symbol
      M3 question : "What is the sign?"
      Sémantique  : pont sémiotique signifiant↔signifié
                    (Peirce — signe, objet, interprétant)
      Couverture  : identifiants (le signe, pas la valeur)
                    constantes prédéfinies (signes conventionnels)
      Note        : Ss_ = le SIGNE (identifiant "main", '\0', PI)
                    It_ = la VALEUR signifiée (0x1000, 0x00, 3.14)
                    Ss_LOOKUP résout Ss → It

      Identifiants (noms symboliques)
        Ss_INTERN   interne identifiant dans pool            (0xE0)
        Ss_LOOKUP   identifiant → valeur It associée         (0xE1)
        Ss_HASH     hash d'identifiant → clé rapide          (0xE2)
        Ss_CMP_ID   compare deux identifiants                (0xE3)
        Ss_MANGLE   mangling de nom (namespaces)             (0xE4)
        Ss_DEMANGLE nom manglé → nom lisible                 (0xE5)

      Constantes prédéfinies — délimiteurs et marqueurs
        Ss_NULL_T   '\0'  fin de chaîne                      (0xE6)
        Ss_STR_DLM  '"'   délimiteur de string               (0xE7)
        Ss_NS_SEP   ':'   séparateur namespace               (0xE8)
        Ss_ESCAPE   '\\'  caractère d'échappement            (0xE9)

      Constantes numériques prédéfinies (signes mathématiques)
        Ss_PI       π = 3.14159265358979...                  (0xEA)
        Ss_E_CST    e = 2.71828182845904...                  (0xEB)
        Ss_SQRT2    √2 = 1.41421356237309...                 (0xEC)
        Ss_INF      +∞ IEEE 754                              (0xED)
        Ss_NAN      NaN IEEE 754                             (0xEE)

      Adresses prédéfinies (signes topologiques VM)
        Ss_ADDR_CODE adresse début section .code             (0xEF)
        ; Ss_ADDR_STACK, Ss_ADDR_HEAP, Ss_ADDR_NULL
        ; → via L_GLOB si > 16 opcodes

───────────────────────────────────────────────────────────────────
0xF_  L_   Localizability
      M3 question : "Converging toward which attractor?"
      Sémantique  : indicateur de convergence cybernétique
                    vers un attracteur mémoire
                    un pointeur converge vers une adresse
      Note        : L_FAR_CALL est L_ (pas F_) car la
                    localisation de la cible 64b est
                    le problème dominant, pas le flux

        L_LEA       load effective address (base+offset)     (0xF0)
        L_ADDR      adresse de variable locale → reg         (0xF1)
        L_OFFSET    calcule offset champ dans struct         (0xF2)
        L_IDX       adresse élément tableau (base,idx,stride)(0xF3)
        L_DEREF     déréférence pointeur → valeur            (0xF4)
        L_DEREF_W   déréférence + write                      (0xF5)
        L_NULL      reg = NULL (pointeur nul)                (0xF6)
        L_IS_NULL   test nullité → bool                      (0xF7)
        L_BOUND_CHK vérifie ptr dans région valide           (0xF8)
        L_ALIGN     aligne adresse sur N bytes               (0xF9)
        L_PAGE      retourne page mémoire de l'adresse       (0xFA)
        L_GLOB      adresse variable globale (id 16b)        (0xFB)
        L_TLS       adresse variable thread-local            (0xFC)
        L_RELOCATE  applique relocation (linker support)     (0xFD)
        L_FAR_CALL  appel adresse 64b (cible > ±8MB)        (0xFE)
        L_FAR_JMP   saut adresse 64b (cible > ±8MB)         (0xFF)
```

---

## 3. Récapitulatif — Motivations sémantiques M3

```
Monoïde  Hex   Catégorie  Question M3              Opcodes VM
────────────────────────────────────────────────────────────────────────
Gt  ×    0x0_  A_         Où convergent les données? Pile + Tas
         0x1_  St_        Comment organisées ?       Types/structs/NOP
         0x2_  F_         Comment s'écoule l'exec ?  JMP/CALL/RET/IF/coroutines
         0x3_  It_        Quel état informationnel ?  Flags/events/IRQ/valeurs
         0x4_  D_         Qu'est-ce qui modifie ?    MOV/LOAD/STORE/ADD/AND...

Gm  +    0x5_  R_         Encodable autrement ?      Conversions I2F/F2FIX...
         0x6_  E_         Génère de la nouveauté ?   Modules/hooks/GC adaptatif
         0x7_  V_         Vérifiable/falsifiable ?    CMP/ASSERT/RANGE...
         0x8_  O_         Mesurable internement ?     DUMP/TRACE/BREAK...
         0x9_  Im_        Interfaçable ?              FFI/SYSCALL/SDL2...

Gs  |    0xA_  T_         Quand ?                    TICK/FRAME_SYN/TIMER...
         0xB_  _^_        Onset/activation ?         NEW/SPAWN/OPEN/LOCK...
         0xC_  _$_        Terminus/dissolution ?      DEL/KILL/CLOSE/UNLOCK...
         0xD_  K_         Que sait-on ?              TYPEOF/IS_A/SCHEMA...
         0xE_  Ss_        Quel signe ?               INTERN/LOOKUP/PI/NULL_T...
         0xF_  L_         Vers quel attracteur ?      LEA/DEREF/FAR_CALL...
```

---

## 4. Wolf3D — Opcodes critiques

```
Im_FB_BLIT   (0x92)   blit framebuffer → écran SDL2
T_FRAME_SYN  (0xA6)   synchronisation 35fps
D_FIXMUL     (*)      multiplication virgule fixe 16.16 (raycaster)
D_MEMCPY     (0x4C)   copie framebuffer
D_MEMSET     (0x4D)   effacement écran
F_LOOP       (0x2B)   boucle colonnes raycaster
Im_REGISTER_CB (0x99) callbacks SDL2 (keydown, quit)
L_FAR_CALL   (0xFE)   appels SDL2 > ±8MB
_^_ARENA_B   (0xBE)   Z_Malloc style (Doom Phase 2)
_$_ARENA_E   (0xCC)   libération arène en bloc
```

---

## 5. Symétrie _^_ / _$_ (Poles)

Chaque opcode _^_ a exactement un symétrique _$_ :

```
_^_NEW_OBJ   ↔  _$_DEL_OBJ
_^_NEW_STR   ↔  _$_DEL_STR
_^_NEW_ARR   ↔  _$_FREE_ARR
_^_SPAWN     ↔  _$_KILL
_^_OPEN_CH   ↔  _$_CLOSE_CH
_^_PUSH_FR   ↔  _$_POP_FR
_^_NEW_CTX   ↔  _$_DEL_CTX
_^_PIN       ↔  _$_UNPIN
_^_REF_INC   ↔  _$_REF_DEC
_^_LOCK      ↔  _$_UNLOCK
_^_OPEN_SC   ↔  _$_CLOSE_SC
_^_ALLOC_P   ↔  _$_FREE_P
_^_ARENA_B   ↔  _$_ARENA_E
_^_ACTIVATE  ↔  _$_DEACT
```

Aucun opcode orphelin dans l'une ou l'autre catégorie.

---

## 6. Distinctions sémantiques clés

```
Ss_ vs It_
  Ss_INTERN "main"    → interne le SIGNE (identifiant)
  It_GET_FLAG RUNNING → lit la VALEUR encodée brute
  Ss_LOOKUP "main" → It  → signe Ss → valeur It

St_ vs K_
  St_SIZEOF type      → taille statique connue à compile-time
  K_SIZEOF  obj       → taille réelle connue à runtime

D_ vs It_
  D_STORE32 R0, R1, 0 → modification BRUTE sans sémantique d'état
  It_SET_FLAG GAME_OVER → changement d'état NOMMÉ et signifiant

F_ vs L_
  F_CALL  @near       → flux dominant (cible proche ±8MB)
  L_FAR_CALL @far     → localisation dominante (cible 64b)

A_ vs _^_
  A_ALLOC             → convergence vers le Tas (attracteur)
  _^_NEW_OBJ          → activation/onset d'un objet typé
```

---

*TriskeleToolchain — ISA Reference v0.2.0*
*Echopraxium with the collaboration of Claude AI — 2026-05-31*
