#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
restore_tscg_rag.py - Restore a TSCG RAG database from its compressed archive

Reverses the two-step pipeline applied by create_tscg_rag.py:
  1. Extract the .tar.gz archive
  2. Dequantize float16 → float32 in chroma.sqlite3 (if quantization was applied)

The HNSW index (data_level0.bin) is not touched — it was never quantized.

Usage:
  python restore_tscg_rag.py db_tscg_rag.tar.gz
  python restore_tscg_rag.py db_tscg_rag.tar.gz --out ./restored_db
  python restore_tscg_rag.py db_tscg_rag.tar.gz --no-dequantize
  python restore_tscg_rag.py db_tscg_rag.tar.gz --dim 768   # for larger models

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

# Default embedding dimension for all-MiniLM-L6-v2
DEFAULT_DIM = 384


# ==============================================================================
# ARGUMENT PARSING
# ==============================================================================

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Restore a TSCG RAG database from its .tar.gz archive",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXAMPLES:
  python restore_tscg_rag.py db_tscg_rag.tar.gz
  python restore_tscg_rag.py db_tscg_rag.tar.gz --out ./my_restored_db
  python restore_tscg_rag.py db_tscg_rag.tar.gz --no-dequantize
  python restore_tscg_rag.py db_tscg_rag.tar.gz --dim 768 --verbose

WHAT THIS DOES:
  1. Extracts the .tar.gz archive to --out directory
  2. Detects whether chroma.sqlite3 contains float16 embedding BLOBs
  3. If yes, repacks them to float32 (required by ChromaDB)

  The HNSW index (data_level0.bin) is never modified.

NOTE:
  If create_tscg_rag.py was run with --no-quantize, use --no-dequantize here.
  The script auto-detects float16 vs float32 so --no-dequantize is mainly
  useful to skip the detection pass entirely.
        """
    )

    parser.add_argument(
        "archive",
        help="Path to the .tar.gz archive created by create_tscg_rag.py"
    )

    parser.add_argument(
        "--out",
        default=None,
        help=(
            "Output directory for the restored database "
            "(default: archive name without .tar.gz, in the same folder)"
        )
    )

    parser.add_argument(
        "--dim",
        type=int,
        default=DEFAULT_DIM,
        help=(
            f"Embedding dimension (default: {DEFAULT_DIM} for all-MiniLM-L6-v2; "
            "use 768 for larger models)"
        )
    )

    parser.add_argument(
        "--no-dequantize",
        action="store_true",
        help="Skip float16→float32 dequantization (use if DB was not quantized)"
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed progress"
    )

    return parser.parse_args()


# ==============================================================================
# STEP 1 — EXTRACT
# ==============================================================================

def extract_archive(archive_path: str, out_dir: str, verbose: bool = False) -> str:
    """
    Extract a .tar.gz archive.

    Returns the path to the extracted ChromaDB directory.
    """
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
        # Security: strip absolute paths
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

    # Find the chroma.sqlite3 to confirm extraction
    sqlite_candidates = list(out.rglob("chroma.sqlite3"))
    if not sqlite_candidates:
        print(f"❌ chroma.sqlite3 not found after extraction in {out}")
        sys.exit(1)

    db_dir = sqlite_candidates[0].parent
    if verbose:
        print(f"  Found chroma.sqlite3 in: {db_dir}")

    return str(db_dir)


# ==============================================================================
# STEP 2 — DEQUANTIZE
# ==============================================================================

def detect_embedding_dtype(sqlite_path: str, dim: int) -> str:
    """
    Detect whether embedding BLOBs are float16 or float32.

    Heuristic: sample the first non-null BLOB in any embedding column.
      - len == dim * 2  →  float16
      - len == dim * 4  →  float32
      - other           →  unknown

    Returns: 'float16' | 'float32' | 'unknown'
    """
    conn = sqlite3.connect(sqlite_path)
    try:
        tables = [
            r[0] for r in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )
        ]
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
                # Unknown length — try both common dims
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
    """
    Repack float16 embedding BLOBs → float32 in chroma.sqlite3.

    This is the exact inverse of quantize_sqlite_embeddings() in create_tscg_rag.py.
    Only columns whose BLOB length matches dim×2 (float16) are touched;
    columns that are already float32 (dim×4) are skipped.

    Returns dict with size_before_mb, size_after_mb, rows_updated.
    """
    sqlite_path = Path(db_path) / "chroma.sqlite3"
    if not sqlite_path.exists():
        return {"error": f"chroma.sqlite3 not found in {db_path}"}

    # Auto-detect dtype first
    dtype = detect_embedding_dtype(str(sqlite_path), dim)
    if verbose:
        print(f"  Detected embedding dtype: {dtype}")

    if 'float32' in dtype:
        print("  ℹ️  Embeddings are already float32 — dequantization not needed")
        return {"rows_updated": 0, "already_float32": True}

    if 'unknown' in dtype:
        print("  ⚠️  Cannot determine embedding dtype — skipping dequantization")
        print(f"      Try --dim with a different value (current: {dim})")
        return {"rows_updated": 0, "unknown_dtype": True}

    size_before = sqlite_path.stat().st_size

    conn = sqlite3.connect(str(sqlite_path))
    try:
        tables = [
            r[0] for r in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )
        ]

        rows_updated = 0
        for table in tables:
            cols = conn.execute(f"PRAGMA table_info({table})").fetchall()
            blob_cols = [
                c[1] for c in cols
                if 'embed' in c[1].lower() or c[2].upper() in ('BLOB', '')
            ]
            for col in blob_cols:
                sample = conn.execute(
                    f"SELECT rowid, {col} FROM {table} "
                    f"WHERE {col} IS NOT NULL LIMIT 1"
                ).fetchone()
                if sample is None:
                    continue
                blob = sample[1]
                if not isinstance(blob, bytes):
                    continue
                if len(blob) != dim * 2:      # not float16 at this dim
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
                    floats = struct.unpack(f'<{dim}e', blob16)   # float16
                    blob32 = struct.pack(f'<{dim}f', *floats)    # float32
                    conn.execute(
                        f"UPDATE {table} SET {col}=? WHERE rowid=?",
                        (blob32, rowid)
                    )
                    updated += 1
                conn.execute("COMMIT")
                rows_updated += updated

        # VACUUM to reclaim freed pages after expansion
        # Note: float32 is larger than float16, so the file grows — VACUUM
        # ensures pages are laid out cleanly for ChromaDB's sequential reads.
        if rows_updated > 0 and verbose:
            print("  Running VACUUM...")
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
# SANITY CHECK
# ==============================================================================

def verify_restored_db(db_dir: str, dim: int, verbose: bool = False) -> bool:
    """
    Quick sanity check after restoration:
      - chroma.sqlite3 exists and is readable
      - Embedding BLOBs are now float32 (dim × 4 bytes)
      - metadata.json is present (if created by create_tscg_rag.py)
    """
    sqlite_path = Path(db_dir) / "chroma.sqlite3"
    ok = True

    # 1. SQLite readable
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

    # 2. Embeddings are float32
    dtype = detect_embedding_dtype(str(sqlite_path), dim)
    if 'float32' in dtype:
        print(f"  ✓ Embeddings: float32 (dim={dim})")
    elif 'float16' in dtype:
        print(f"  ❌ Embeddings still float16 — dequantization may have failed")
        ok = False
    else:
        print(f"  ⚠️  Embedding dtype: {dtype} (may be OK if --no-dequantize was used)")

    # 3. HNSW index present
    hnsw = Path(db_dir) / "data_level0.bin"
    if hnsw.exists():
        print(f"  ✓ HNSW index: {hnsw.stat().st_size / (1024*1024):.1f} MB")
    else:
        # ChromaDB sometimes puts it in a subdirectory
        candidates = list(Path(db_dir).rglob("data_level0.bin"))
        if candidates:
            print(f"  ✓ HNSW index found: {candidates[0]}")
        else:
            print("  ℹ️  data_level0.bin not found (will be rebuilt on first query)")

    # 4. metadata.json
    meta_path = Path(db_dir) / "metadata.json"
    if meta_path.exists():
        with open(meta_path, encoding='utf-8') as f:
            meta = json.load(f)
        print(f"  ✓ metadata.json: {meta.get('total_segments_final', '?')} segments, "
              f"created {meta.get('created_at', '?')[:10]}")
    else:
        if verbose:
            print("  ℹ️  metadata.json not found (not created by create_tscg_rag.py)")

    return ok


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    args = parse_arguments()

    print("\n" + "="*70)
    print("  TSCG RAG Database Restore")
    print("="*70)
    print(f"Archive : {args.archive}")

    # Resolve output directory
    archive = Path(args.archive)
    if args.out:
        out_dir = args.out
    else:
        # Strip .tar.gz → use archive stem as output dir name, same folder
        name = archive.name
        for suffix in ('.tar.gz', '.tgz'):
            if name.endswith(suffix):
                name = name[:-len(suffix)]
                break
        out_dir = str(archive.parent / name)

    print(f"Output  : {out_dir}")
    print(f"Dim     : {args.dim}")
    print("="*70)

    # ── Step 1: Extract ───────────────────────────────────────────────────────
    db_dir = extract_archive(args.archive, out_dir, verbose=args.verbose)

    # ── Step 2: Dequantize ────────────────────────────────────────────────────
    if not args.no_dequantize:
        print(f"\n🔬 Dequantizing sqlite3 embeddings float16→float32...")
        result = dequantize_sqlite_embeddings(
            db_dir, dim=args.dim, verbose=args.verbose
        )

        if "error" in result:
            print(f"  ❌ {result['error']}")
        elif result.get("already_float32") or result.get("unknown_dtype"):
            pass   # message already printed inside the function
        else:
            print(f"  ✓ Dequantized {result['rows_updated']} rows")
            print(f"    sqlite3: {result['size_before_mb']:.1f} MB → "
                  f"{result['size_after_mb']:.1f} MB "
                  f"(+{result['grown_mb']:.1f} MB, float32 is larger)")
    else:
        print("\n  (Dequantization skipped by --no-dequantize)")

    # ── Step 3: Verify ────────────────────────────────────────────────────────
    print("\n🔎 Verifying restored database...")
    ok = verify_restored_db(db_dir, dim=args.dim, verbose=args.verbose)

    # ── Summary ───────────────────────────────────────────────────────────────
    print("\n" + "="*70)
    if ok:
        print("  ✅ TSCG RAG Database Restored Successfully!")
    else:
        print("  ⚠️  Restoration completed with warnings — check output above")
    print("="*70)
    print(f"\n  Restored DB : {db_dir}")
    print("\n💡 Next steps:")
    print("  1. Point query_tscg_rag.py to the restored DB path")
    print("  2. Or load it with: chromadb.PersistentClient(path='<restored_db>')")
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
