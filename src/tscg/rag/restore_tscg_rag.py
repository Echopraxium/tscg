#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
restore_tscg_rag.py - Restore a TSCG RAG database from its compressed archive

Reverses the pipeline applied by create_tscg_rag.py:
  1. Reassemble split parts (if archive was split into .part00, .part01, ...)
  2. Extract the .tar.gz archive
  3. Dequantize float16 → float32 in chroma.sqlite3 (if quantization was applied)

The HNSW index (data_level0.bin) is not touched — it was never quantized.

Usage:
  # Single archive
  python restore_tscg_rag.py db_tscg_rag.tar.gz

  # Split archive — pass any one part or the manifest
  python restore_tscg_rag.py db_tscg_rag.tar.gz.part00
  python restore_tscg_rag.py db_tscg_rag.tar.gz.manifest.json

  # Options
  python restore_tscg_rag.py db_tscg_rag.tar.gz.part00 --out ./restored_db
  python restore_tscg_rag.py db_tscg_rag.tar.gz --no-dequantize
  python restore_tscg_rag.py db_tscg_rag.tar.gz --dim 768

Author: Echopraxium with the collaboration of Claude AI
"""

import os
import sys
import argparse
import sqlite3
import struct
import tarfile
import json
from pathlib import Path

# Force UTF-8 output
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

DEFAULT_DIM = 384


# ==============================================================================
# ARGUMENT PARSING
# ==============================================================================

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Restore a TSCG RAG database from its .tar.gz archive (or split parts)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXAMPLES:
  # Single archive (no split)
  python restore_tscg_rag.py db_tscg_rag.tar.gz

  # Split archive — pass any .part?? file or the .manifest.json
  python restore_tscg_rag.py db_tscg_rag.tar.gz.part00
  python restore_tscg_rag.py db_tscg_rag.tar.gz.manifest.json

  # Custom output dir
  python restore_tscg_rag.py db_tscg_rag.tar.gz.part00 --out ./my_db

  # If DB was created with --no-quantize
  python restore_tscg_rag.py db_tscg_rag.tar.gz --no-dequantize

  # Larger embedding model (768 dims)
  python restore_tscg_rag.py db_tscg_rag.tar.gz --dim 768

WHAT THIS DOES:
  1. Detects split parts via .manifest.json (auto-discovered next to the input file)
  2. Reassembles parts → single .tar.gz  (pure binary concatenation, no external tools)
  3. Extracts the .tar.gz
  4. Dequantizes float16→float32 in chroma.sqlite3 (auto-detected, skipped if not needed)
  5. Verifies the restored database
        """
    )

    parser.add_argument(
        "input",
        help=(
            "Path to: (a) the .tar.gz archive, "
            "(b) any .part?? file, or "
            "(c) the .manifest.json file"
        )
    )

    parser.add_argument(
        "--out",
        default=None,
        help="Output directory for the restored database (default: derived from archive name)"
    )

    parser.add_argument(
        "--dim",
        type=int,
        default=DEFAULT_DIM,
        help=f"Embedding dimension (default: {DEFAULT_DIM} for all-MiniLM-L6-v2)"
    )

    parser.add_argument(
        "--no-dequantize",
        action="store_true",
        help="Skip float16→float32 dequantization"
    )

    parser.add_argument(
        "--keep-archive",
        action="store_true",
        help="Keep the reassembled .tar.gz after extraction (deleted by default)"
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed progress"
    )

    return parser.parse_args()


# ==============================================================================
# STEP 1 — REASSEMBLE SPLIT PARTS
# ==============================================================================

def resolve_input(input_path: str) -> tuple:
    """
    Given any of: a .tar.gz, a .part?? file, or a .manifest.json,
    return (archive_path, parts_list_or_None).

    archive_path : the final (possibly reassembled) .tar.gz path
    parts        : list of part paths if split, else None
    """
    p = Path(input_path).resolve()

    # Case 1 — plain .tar.gz, no split
    if p.suffix in ('.gz', '.tgz') and p.exists():
        return str(p), None

    # Case 2 — manifest.json
    if p.name.endswith('.manifest.json'):
        manifest_path = p
    else:
        # Case 3 — a .part?? file  (e.g. db.tar.gz.part00)
        # Manifest sits next to the parts: db.tar.gz.manifest.json
        # Strip ".partNN" suffix to find the archive base name
        name = p.name
        import re
        name_base = re.sub(r'\.part\d+$', '', name)
        manifest_path = p.parent / f"{name_base}.manifest.json"

    if not manifest_path.exists():
        # No manifest → treat input as a single archive
        if p.exists():
            return str(p), None
        print(f"❌ Cannot find archive or manifest for: {input_path}")
        sys.exit(1)

    with open(manifest_path, encoding='utf-8') as f:
        manifest = json.load(f)

    archive_name = manifest['archive_name']
    part_names   = manifest['parts']
    base_dir     = manifest_path.parent

    parts = [str(base_dir / pname) for pname in part_names]
    missing = [p for p in parts if not Path(p).exists()]
    if missing:
        print(f"❌ Missing part files: {', '.join(Path(m).name for m in missing)}")
        sys.exit(1)

    archive_path = str(base_dir / archive_name)
    return archive_path, parts


def join_parts(parts: list, archive_path: str, verbose: bool = False) -> str:
    """
    Concatenate ordered binary part files into a single .tar.gz archive.

    This is the exact inverse of split_archive() in create_tscg_rag.py.
    No format knowledge needed — raw binary concatenation is sufficient.

    Returns the path to the reassembled archive.
    """
    total_bytes = sum(Path(p).stat().st_size for p in parts)
    print(f"🔗 Reassembling {len(parts)} parts "
          f"({total_bytes / (1024*1024):.1f} MB total)...")

    with open(archive_path, 'wb') as dst:
        for i, part in enumerate(parts):
            chunk = Path(part).read_bytes()
            dst.write(chunk)
            if verbose:
                print(f"  Part {i:02d}: {Path(part).name}  "
                      f"({len(chunk)/(1024*1024):.1f} MB)")

    actual = Path(archive_path).stat().st_size
    if actual != total_bytes:
        print(f"❌ Size mismatch after join: expected {total_bytes}, got {actual}")
        sys.exit(1)

    print(f"✓ Reassembled → {Path(archive_path).name} ({actual/(1024*1024):.1f} MB)")
    return archive_path


# ==============================================================================
# STEP 2 — EXTRACT
# ==============================================================================

def extract_archive(archive_path: str, out_dir: str, verbose: bool = False) -> str:
    """Extract a .tar.gz archive. Returns the ChromaDB directory path."""
    archive = Path(archive_path)
    if not archive.exists():
        print(f"❌ Archive not found: {archive_path}")
        sys.exit(1)

    if not tarfile.is_tarfile(str(archive)):
        print(f"❌ Not a valid tar archive: {archive_path}")
        sys.exit(1)

    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    print(f"📦 Extracting {archive.name} → {out}/...")
    with tarfile.open(str(archive), "r:gz") as tar:
        members = []
        for m in tar.getmembers():
            if m.name.startswith('/') or '..' in m.name:
                if verbose:
                    print(f"  ⚠️  Skipping unsafe path: {m.name}")
                continue
            members.append(m)
        tar.extractall(path=str(out), members=members)

    size_mb = archive.stat().st_size / (1024 * 1024)
    print(f"✓ Extracted ({size_mb:.1f} MB archive)")

    sqlite_candidates = list(out.rglob("chroma.sqlite3"))
    if not sqlite_candidates:
        print(f"❌ chroma.sqlite3 not found after extraction in {out}")
        sys.exit(1)

    db_dir = sqlite_candidates[0].parent
    if verbose:
        print(f"  chroma.sqlite3 found in: {db_dir}")
    return str(db_dir)


# ==============================================================================
# STEP 3 — DEQUANTIZE
# ==============================================================================

def detect_embedding_dtype(sqlite_path: str, dim: int) -> str:
    """Detect whether embedding BLOBs are float16 (dim×2) or float32 (dim×4)."""
    conn = sqlite3.connect(sqlite_path)
    try:
        tables = [r[0] for r in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )]
        for table in tables:
            cols = conn.execute(f"PRAGMA table_info({table})").fetchall()
            for col in cols:
                cname = col[1]
                if 'embed' not in cname.lower():
                    continue
                row = conn.execute(
                    f"SELECT {cname} FROM {table} WHERE {cname} IS NOT NULL LIMIT 1"
                ).fetchone()
                if not row or not isinstance(row[0], bytes):
                    continue
                blob_len = len(row[0])
                if blob_len == dim * 2:
                    return 'float16'
                if blob_len == dim * 4:
                    return 'float32'
                for d in (384, 768, 1536):
                    if blob_len == d * 2:
                        return f'float16 (detected dim={d}, expected {dim})'
                    if blob_len == d * 4:
                        return f'float32 (detected dim={d}, expected {dim})'
    finally:
        conn.close()
    return 'unknown'


def dequantize_sqlite_embeddings(
    db_path: str,
    dim: int = DEFAULT_DIM,
    verbose: bool = False,
) -> dict:
    """Repack float16 embedding BLOBs → float32 in chroma.sqlite3."""
    sqlite_path = Path(db_path) / "chroma.sqlite3"
    if not sqlite_path.exists():
        return {"error": f"chroma.sqlite3 not found in {db_path}"}

    dtype = detect_embedding_dtype(str(sqlite_path), dim)
    if verbose:
        print(f"  Detected embedding dtype: {dtype}")

    if 'float32' in dtype:
        print("  ℹ️  Embeddings already float32 — dequantization not needed")
        return {"rows_updated": 0, "already_float32": True}

    if 'unknown' in dtype:
        print(f"  ⚠️  Cannot determine dtype — skipping (try --dim with a different value)")
        return {"rows_updated": 0, "unknown_dtype": True}

    size_before = sqlite_path.stat().st_size
    conn = sqlite3.connect(str(sqlite_path))
    try:
        tables = [r[0] for r in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )]
        rows_updated = 0
        for table in tables:
            cols = conn.execute(f"PRAGMA table_info({table})").fetchall()
            blob_cols = [
                c[1] for c in cols
                if 'embed' in c[1].lower() or c[2].upper() in ('BLOB', '')
            ]
            for col in blob_cols:
                sample = conn.execute(
                    f"SELECT rowid, {col} FROM {table} WHERE {col} IS NOT NULL LIMIT 1"
                ).fetchone()
                if sample is None or not isinstance(sample[1], bytes):
                    continue
                if len(sample[1]) != dim * 2:
                    continue

                count = conn.execute(
                    f"SELECT COUNT(*) FROM {table} WHERE {col} IS NOT NULL"
                ).fetchone()[0]
                if verbose:
                    print(f"  Repacking {table}.{col}: "
                          f"{count} rows × {dim} dims float16→float32...")

                conn.execute("BEGIN")
                updated = 0
                for rowid, blob16 in conn.execute(
                    f"SELECT rowid, {col} FROM {table} WHERE {col} IS NOT NULL"
                ):
                    floats  = struct.unpack(f'<{dim}e', blob16)
                    blob32  = struct.pack(f'<{dim}f', *floats)
                    conn.execute(
                        f"UPDATE {table} SET {col}=? WHERE rowid=?",
                        (blob32, rowid)
                    )
                    updated += 1
                conn.execute("COMMIT")
                rows_updated += updated

        if rows_updated > 0:
            conn.execute("VACUUM")
    finally:
        conn.close()

    size_after = sqlite_path.stat().st_size
    return {
        "size_before_mb": round(size_before / (1024 * 1024), 2),
        "size_after_mb":  round(size_after  / (1024 * 1024), 2),
        "rows_updated":   rows_updated,
        "grown_mb":       round((size_after - size_before) / (1024 * 1024), 2),
    }


# ==============================================================================
# STEP 4 — VERIFY
# ==============================================================================

def verify_restored_db(db_dir: str, dim: int, verbose: bool = False) -> bool:
    """Quick sanity check: sqlite3 readable, embeddings float32, metadata present."""
    sqlite_path = Path(db_dir) / "chroma.sqlite3"
    ok = True

    try:
        conn = sqlite3.connect(str(sqlite_path))
        tables = [r[0] for r in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )]
        conn.close()
        if verbose:
            print(f"  sqlite3 tables: {', '.join(tables)}")
    except Exception as e:
        print(f"  ❌ sqlite3 unreadable: {e}")
        return False

    dtype = detect_embedding_dtype(str(sqlite_path), dim)
    if 'float32' in dtype:
        print(f"  ✓ Embeddings: float32 (dim={dim})")
    elif 'float16' in dtype:
        print(f"  ❌ Embeddings still float16 — dequantization may have failed")
        ok = False
    else:
        print(f"  ⚠️  Embedding dtype: {dtype}")

    hnsw_candidates = list(Path(db_dir).rglob("data_level0.bin"))
    if hnsw_candidates:
        mb = hnsw_candidates[0].stat().st_size / (1024 * 1024)
        print(f"  ✓ HNSW index: {mb:.1f} MB")
    else:
        print("  ℹ️  data_level0.bin not found (rebuilt on first query)")

    meta_path = Path(db_dir) / "metadata.json"
    if meta_path.exists():
        with open(meta_path, encoding='utf-8') as f:
            meta = json.load(f)
        print(f"  ✓ metadata.json: {meta.get('total_segments_final','?')} segments, "
              f"created {meta.get('created_at','?')[:10]}")
    elif verbose:
        print("  ℹ️  metadata.json not found")

    return ok


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    args = parse_arguments()

    print("\n" + "="*70)
    print("  TSCG RAG Database Restore")
    print("="*70)
    print(f"Input   : {args.input}")

    # ── Resolve: single archive or split parts? ───────────────────────────────
    archive_path, parts = resolve_input(args.input)

    # Determine output directory
    if args.out:
        out_dir = args.out
    else:
        base = Path(archive_path).name
        for suffix in ('.tar.gz', '.tgz'):
            if base.endswith(suffix):
                base = base[:-len(suffix)]
                break
        out_dir = str(Path(args.input).resolve().parent / base)

    print(f"Output  : {out_dir}")
    print(f"Dim     : {args.dim}")
    print("="*70)

    # ── Step 1: Reassemble parts (if split) ───────────────────────────────────
    assembled_archive = archive_path
    if parts:
        assembled_archive = join_parts(parts, archive_path, verbose=args.verbose)

    # ── Step 2: Extract ───────────────────────────────────────────────────────
    db_dir = extract_archive(assembled_archive, out_dir, verbose=args.verbose)

    # Clean up reassembled archive (it's a temp artefact)
    if parts and not args.keep_archive:
        Path(assembled_archive).unlink(missing_ok=True)
        if args.verbose:
            print(f"  Deleted temporary reassembled archive")

    # ── Step 3: Dequantize ────────────────────────────────────────────────────
    if not args.no_dequantize:
        print(f"\n🔬 Dequantizing sqlite3 embeddings float16→float32...")
        result = dequantize_sqlite_embeddings(db_dir, dim=args.dim, verbose=args.verbose)
        if "error" in result:
            print(f"  ❌ {result['error']}")
        elif not result.get("already_float32") and not result.get("unknown_dtype"):
            print(f"  ✓ Dequantized {result['rows_updated']} rows  "
                  f"({result['size_before_mb']:.1f} MB → {result['size_after_mb']:.1f} MB)")
    else:
        print("\n  (Dequantization skipped by --no-dequantize)")

    # ── Step 4: Verify ────────────────────────────────────────────────────────
    print("\n🔎 Verifying restored database...")
    ok = verify_restored_db(db_dir, dim=args.dim, verbose=args.verbose)

    # ── Summary ───────────────────────────────────────────────────────────────
    print("\n" + "="*70)
    if ok:
        print("  ✅ TSCG RAG Database Restored Successfully!")
    else:
        print("  ⚠️  Restoration completed with warnings")
    print("="*70)
    print(f"\n  Restored DB : {db_dir}")
    print("\n💡 Next steps:")
    print("  python query_tscg_rag.py --db <restored_db>")
    print("  chromadb.PersistentClient(path='<restored_db>')")
    print()
    return 0 if ok else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        if "--verbose" in sys.argv:
            import traceback
            traceback.print_exc()
        sys.exit(1)


