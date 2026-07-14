# Compilation du code de test:
cd projects/Test_ZMachine
_00_open_cmd_window.bat
clang -O0 -emit-llvm -S hello_input.c -o hello_input.ll
cargo run --release -p tsk-cc -- hello_input.ll -o hello_input.tobj
cargo run --release -p tsk-link -- hello_input.tobj -o hello_input.tvmx

# Compilation de "triskele-vm-wasm"
_00_open_cmd_window.bat
cd crates/triskele-vm-wasm
wasm-pack build --target web --out-dir www\pkg

# relancer le serveur
cd E:\...\TriskeleToolchain\crates\triskele-vm-wasm\www
python server.py