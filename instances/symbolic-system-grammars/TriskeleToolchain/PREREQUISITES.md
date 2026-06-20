# TriskeleToolchain — Prerequisites

## Required (native build)

| Tool | Version | Install |
|------|---------|---------|
| Rust + Cargo | stable | https://rustup.rs |
| clang | 16+ | https://releases.llvm.org |
| Python | 3.8+ | https://python.org |
| SDL2 dev libs | 2.x | https://libsdl.org (or via vcpkg) |

## Required (WASM build)

| Tool | Version | Install |
|------|---------|---------|
| wasm32 target | — | `rustup target add wasm32-unknown-unknown` |
| wasm-pack | latest | `cargo install wasm-pack` |

## One-time setup (Windows)

```cmd
rustup target add wasm32-unknown-unknown
cargo install wasm-pack
```

## Build native toolchain

```cmd
cargo build --release
python run_all_tests.py --clean
```

## Build WASM spike

```cmd
cd crates\triskele-vm-wasm
wasm-pack build --target web --out-dir www\pkg
cd ..\..
```

Then serve `crates\triskele-vm-wasm\www\` with any HTTP server:

```cmd
python -m http.server 8080
```

Open `http://localhost:8080`, drop a `.tvmx` file, click ▶ Run.
