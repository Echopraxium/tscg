# TriskeleToolchain — Patch v0.3.25
# Author: Echopraxium with the collaboration of Claude AI

## Scope
M2 — libc parity (Handover v0.3.22 §1): expand `tsk-libc-gen`'s
`LIBC_FUNCTIONS` table from 23 to 59 entries to match every
`LibcSyscall` variant already implemented in `triskele-vm`. No changes
to `triskele-common` (LIBC_SYMBOLS) or `triskele-vm` — the VM-side
implementations existed; only the generator table was lagging.

## File changed
- `crates/tsk-libc-gen/src/main.rs`

## What changed

### LIBC_FUNCTIONS extended: 23 → 59 entries

36 functions added, grouped by category:

**String** (7): `strrchr`, `strstr`, `strdup`, `strcasecmp`,
`strncasecmp`, `strlcat`, `strlcpy` — IDs `0x16`–`0x1C`.

**Stdlib** (5): `malloc`, `free`, `exit`, `atoi`, `strtol` —
IDs `0x33`–`0x37`.

**I/O** (7): `fprintf`, `vfprintf`, `sprintf`, `puts`, `vsprintf`,
`snprintf`, `vsnprintf` — IDs `0x41`–`0x47`.

**Ctype** (6): `toupper`, `tolower`, `isspace`, `isdigit`, `isalpha`,
`isprint` — IDs `0x50`–`0x55`.

**File I/O** (8): `fopen`, `fclose`, `fread`, `fwrite`, `fseek`,
`ftell`, `feof`, `fflush` — IDs `0x60`–`0x67`.

**String utils** (2): `strerror`, `sscanf` — IDs `0x68`–`0x69`.

**Stdlib extra** (1): `calloc` — ID `0x6A`.

All IDs verified against `triskele_vm::libc::LibcSyscall` enum values.

### Confirmed failures this closes
- `test_variadic`: exit 79 instead of 255 — `vsprintf` (0x45) was
  missing from the generator table.
- `test_doom_libc`: memory fault (`addr=0x0`) — `strdup` (0x18),
  `strcasecmp` (0x19), `snprintf` (0x46) and others were missing.

## Validation
- `cargo test --release -p tsk-libc-gen` — **7/7 pass**, including
  `test_all_functions_have_unique_ids` and
  `test_all_functions_have_unique_names` (no duplicates introduced).
- Smoke test (sprintf + strlen + toupper + isdigit + malloc + free,
  all newly added) — exit 99, correct output, VM executes correctly.
- `run_all_tests.py --clean` on Windows required to confirm
  `test_variadic` (255/255) and `test_doom_libc` (expected exit code)
  now pass. The 12 existing stable projects should be unaffected.
