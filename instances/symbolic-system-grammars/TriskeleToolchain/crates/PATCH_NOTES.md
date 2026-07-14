# tsk-cc patch — nonnull attribute + dead alloca eliminator

**Version:** parser.rs 0.3.0 → 0.3.1 / codegen.rs 0.3.3 → 0.3.4
**Goal:** fix two `tsk-cc` bugs that prevented `hello_input.tvmx` (with `fgets`)
from running correctly, blocking M2c validation.

## Bug 1 — `nonnull` attribute not in `skip_flags` (parser.rs)

**Symptom:** `clang -O1 --target=x86_64-pc-linux-gnu` generates:
```llvm
call ptr @fgets(ptr noundef nonnull @buf, i32 noundef 256, ptr noundef null)
```
`skip_flags()` did not list `nonnull` (nor `captures`, `immarg`, `returned`,
`signext`, `zeroext`), so the parser treated `nonnull` as an SSA value name
`%nonnull`, producing:
```
CODEGEN FAILED for @main: undefined SSA value '%nonnull'
```

**Fix:** add `"nonnull"|"captures"|"immarg"|"returned"|"signext"|"zeroext"` to
the `skip_flags` match arm. These are all LLVM parameter attributes that appear
with `-O1` optimisation and must be ignored by the parser.

## Bug 2 — Dead alloca (return-value slot) causes linker relocation crash (codegen.rs)

**Symptom:** `clang -O0 --target=x86_64-pc-linux-gnu` generates:
```llvm
%1 = alloca i32, align 4
store i32 0, ptr %1, align 4
ret i32 0
```
`%1` is the implicit return-value slot — allocated, written once with 0, never
read (the `ret` uses `Const(0)` directly). `tsk-cc` generated a frame slot for
it, then emitted a `D_Store32` whose address register was incorrectly left as 0
by a subtle codegen path, triggering a linker fixup that patched it with the
first data symbol address (`0x801000`) → `Memory fault: addr=0x801000, size=4`.

**Fix:** `eliminate_dead_allocas()` — a pre-codegen pass that removes alloca +
store pairs where the alloca address is never loaded or passed to a call.
Called just before `FuncGen::new` in `generate_module`, on a `func.clone()` so
the original module is not mutated.

## Validation

```cmd
cargo build --release -p tsk-cc
clang -O1 -emit-llvm -S --target=x86_64-pc-linux-gnu hello_input.c -o hello_input.ll
cargo run --release -p tsk-cc -- hello_input.ll -o hello_input.tobj
cargo run --release -p tsk-link -- hello_input.tobj -o hello_input.tvmx
target\release\tskvm.exe hello_input.tvmx
```

Expected (native): program waits for input on stdin, then prints "Bonjour, [name]".

```cmd
python run_all_tests.py --clean
```

Expected: all 12 suites pass (zero regression).

---

*Authorship: Echopraxium with the collaboration of Claude AI.*
