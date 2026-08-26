#!/usr/bin/env python3
"""
check-M0 notation hygiene — remove every LITERAL ⊗ (U+2297) glyph from the
checker source, so the tool that forbids ⊗ no longer contains/prints it.

The DETECTION logic (line ~317) already uses the escape "\\u2297" and is left
untouched — that is the correct, glyph-free way to detect the operator. Only the
banner print and the doc/comments carry the bare glyph; those are reworded.

Run from repo root. Each replacement is asserted (fails loud if not found once).
"""
import sys

SRC = "ontology/cli-tools/check-M0/check_m0_instances.py"
DST = SRC

with open(SRC, encoding="utf-8") as f:
    t = f.read()

OT = "\u2297"  # ⊗

REPL = [
    # banner print — the one actually DISPLAYED
    ('    print("C12 extended: hasTensorFormula + tensorFormula key + '
     + OT + ' operator")',
     '    print("C12 extended: hasTensorFormula + tensorFormula key + '
     'tensor-product (U+2297) operator")'),
    # docstring / comments — literal glyph in source
    ('         (c) "' + OT + '" operator absent from all formula values',
     '         (c) "U+2297" (tensor-product) operator absent from all formula values'),
    ('  C12: Extended to detect tensorFormula in nested objects and '
     + OT + ' in formula values',
     '  C12: Extended to detect tensorFormula in nested objects and '
     'U+2297 in formula values'),
    ('        #   (c) "' + OT + '" operator in any string value               (both)',
     '        #   (c) "U+2297" operator in any string value              (both)'),
    ('        # (c) "' + OT + '" tensor product operator in any formula value',
     '        # (c) "U+2297" tensor product operator in any formula value'),
    # inline comment next to the detection code (keep the code, reword the comment)
    ('        if "\\u2297" in raw_str:  # ' + OT + ' = U+2297',
     '        if "\\u2297" in raw_str:  # U+2297 tensor-product operator'),
]

missing = []
for old, new in REPL:
    if t.count(old) != 1:
        missing.append((old[:70], t.count(old)))
    else:
        t = t.replace(old, new)

if missing:
    print("ABORT — source strings not found exactly once:")
    for frag, n in missing:
        print(f"  count={n}  «{frag}...»")
    sys.exit(1)

# ---- FUNCTIONAL FIX (behavioral): C12(c) could not detect ⊗ in a formula VALUE.
# json.dumps(graph) defaults to ensure_ascii=True, which escapes ⊗ to the 6-char
# sequence \\u2297; the membership test then looks for the single ⊗ char and never
# matches. ensure_ascii=False keeps the literal char so the test works.
det_old = ('        raw_str = json.dumps(graph)\n'
           '        if "\\u2297" in raw_str:  # U+2297 tensor-product operator')
det_new = ('        raw_str = json.dumps(graph, ensure_ascii=False)\n'
           '        if "\\u2297" in raw_str:  # U+2297 tensor-product operator')
if t.count(det_old) != 1:
    print(f"ABORT — detection anchor not found exactly once (count={t.count(det_old)})")
    sys.exit(1)
t = t.replace(det_old, det_new)

# safety: the ONLY remaining U+2297 in the file must be the escaped detection literal
assert OT not in t, "literal ⊗ still present after patch"
assert '"\\u2297"' in t, "detection escape \\u2297 must remain intact"

with open(DST, "w", encoding="utf-8") as f:
    f.write(t)

print("Patched", DST)
print("  literal ⊗ remaining:", t.count(OT))
print("  detection escape \\u2297 intact:", '"\\u2297"' in t)
