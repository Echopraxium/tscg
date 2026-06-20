# TriskeleVM — WASM Hello World Spike

## Ce que c'est

Un premier backend WASM qui valide la conception du trait `DisplayBackend`
(TODO-3, Handover v0.3.22 §3) : la VM tourne dans le navigateur, `printf`
route vers la page HTML, sans SDL2 ni `std::fs`.

## Prérequis Windows

```cmd
rustup target add wasm32-unknown-unknown
cargo install wasm-pack
```

## Compiler

Depuis la racine du workspace :

```cmd
cd crates\triskele-vm-wasm
wasm-pack build --target web --out-dir www\pkg
```

Ça génère `www\pkg\triskele_vm_wasm.js` + `www\pkg\triskele_vm_wasm_bg.wasm`.

## Préparer un .tvmx Hello World

Depuis la racine du workspace :

```cmd
echo int printf(const char *fmt, ...); int main() { printf("Hello from TriskeleVM WASM!\n"); return 0; } > hello.c
clang -O0 -emit-llvm -S hello.c -o hello.ll
target\release\tsk-cc hello.ll -o hello.tobj
target\release\tsk-link hello.tobj -o hello.tvmx
```

## Servir la page HTML

Le navigateur bloque les imports WASM depuis `file://`. Il faut un serveur HTTP local :

```cmd
cd crates\triskele-vm-wasm\www
python -m http.server 8080
```

Puis ouvrir `http://localhost:8080` dans le navigateur, déposer `hello.tvmx`,
cliquer ▶ Run.

## Résultat attendu

```
Exit: 0
Hello from TriskeleVM WASM!
```

## Structure de la crate

```
crates/triskele-vm-wasm/
  Cargo.toml          — dépend de triskele-vm sans feature "native"
  src/lib.rs          — WasmBackend (DisplayBackend no-op) + run_tvmx()
  www/
    index.html        — page HTML avec drag-drop .tvmx
    pkg/              — généré par wasm-pack (à ne pas committer)
```

## Notes techniques

- `triskele-vm` est compilé **sans** la feature `native` (pas de SDL2,
  pas de `std::fs`, pas de `libloading`).
- `WasmBackend` implémente `DisplayBackend` avec des no-ops — suffisant
  pour un programme qui ne fait que `printf`.
- `printf` est capturé via un `ArcWriter` qui redirige la sortie VM vers
  un `Vec<u8>` récupéré après `cpu.run()`.
- La feature `native` (défaut du workspace) reste inchangée — `cargo build`
  normal compile toujours le binaire `tskvm.exe` natif avec SDL2.

## Étapes suivantes (hors scope de ce spike)

1. Implémenter `fb_blit_pixels` dans `WasmBackend` via `ImageData` + `putImageData`
   sur un `<canvas>` HTML — ce qui permettra d'afficher un vrai framebuffer.
2. Implémenter `poll_events` via des event listeners DOM (keyboard).
3. Remplacer `frame_sync` (blocking sleep) par `requestAnimationFrame`.
