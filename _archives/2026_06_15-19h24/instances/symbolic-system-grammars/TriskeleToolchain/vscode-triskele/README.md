# triskele-debug — VS Code Extension

**Author**: Echopraxium with the collaboration of Claude AI  
**Version**: 0.1.0

Extension VS Code qui enregistre le type de debugger `"triskele"` et connecte
VS Code à `tsk-dbg` via TCP (DAP over TCP).

---

## Installation

### Méthode 1 — Développement local (recommandé)

```cmd
; Copier le dossier vscode-triskele dans le répertoire des extensions VS Code
xcopy /E /I vscode-triskele "%USERPROFILE%\.vscode\extensions\triskele-debug-0.1.0"
```

Puis **redémarrer VS Code** (Ctrl+Shift+P → "Developer: Reload Window").

### Méthode 2 — Via le panneau Extensions

Pas encore publiée sur le Marketplace — utiliser la méthode 1.

---

## Utilisation

### Workflow standard (deux terminaux)

**Terminal 1 — Assembler et lancer tsk-dbg :**
```cmd
; Assembler avec symbol table
cargo run -p tsk-asm -- src\wolf3d_v2_clean.tasm --emit-symbols

; Lancer le debugger (attend la connexion VS Code)
cargo run -p tsk-dbg -- src\wolf3d_v2_clean.tvmx --symbols src\wolf3d_v2_clean.sym
; → "tsk-dbg: DAP server listening on 127.0.0.1:4711"
```

**VS Code :**
1. Copier `launch.json` dans `.vscode/launch.json` du workspace
2. F5 → sélectionner "Debug wolf3d"
3. VS Code se connecte à tsk-dbg sur le port 4711

### Workflow auto-launch (un seul terminal)

Avec `autoLaunchDebugger: true` dans `launch.json`, VS Code lance `tsk-dbg`
automatiquement avant de se connecter :

```json
{
    "type": "triskele",
    "request": "launch",
    "name": "Debug wolf3d (auto-launch)",
    "program": "${workspaceFolder}/src/wolf3d_v2_clean.tvmx",
    "symbols": "${workspaceFolder}/src/wolf3d_v2_clean.sym",
    "autoLaunchDebugger": true,
    "tskDbgPath": "${workspaceFolder}/target/debug/tsk-dbg.exe"
}
```

---

## Fonctionnalités

- **Breakpoints par label** : Shift+F9 → "Add Function Breakpoint" → `ray_loop`
- **Variables panel** :
  - `Registers` : R0–R31 avec détail hex / i64 / fixed 16.16 / f32
  - `Stack` : top 16 entrées
  - `Disassembly` : PC ± 5 instructions avec labels
- **Debug Console (REPL)** :
  ```
  R12          → valeur de R12 en 4 formats
  pc           → PC courant avec label
  flags        → ZF/SF/OF/CF
  sym ray_loop → adresse du label
  mem 0x400 32 → dump mémoire
  ```
- **Syntax highlighting** pour `.tasm` (opcodes, registres, directives, labels)

---

## Structure

```
vscode-triskele/
├── package.json              ← déclaration du debugger "triskele"
├── language-configuration.json ← config syntaxique .tasm
├── syntaxes/
│   └── tasm.tmLanguage.json  ← grammaire TextMate pour .tasm
├── src/
│   └── extension.js          ← logique de connexion TCP (DebugAdapterServer)
└── launch.json               ← copier dans .vscode/launch.json
```

---

## Pourquoi cette architecture ?

VS Code s'attend à ce que chaque type de debugger soit déclaré par une extension.
Sans extension, il cherche un adapter C# (d'où les logs `.NET` que tu as observés).

L'extension ne contient **aucune logique de debug** — elle dit juste à VS Code :
> "Pour le type `triskele`, connecte-toi sur TCP port 4711."

Toute la logique DAP est dans `tsk-dbg` (le serveur Rust).

---

*triskele-debug v0.1.0 — Echopraxium with the collaboration of Claude AI — 2026-06-01*
