#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
metaconcept_classifier.py - Zero-shot TSCG metaconcept classifier

Given a natural language description of a system (poclet, case study, or
systemic framework), returns ranked M2 metaconcept candidates and analogous
existing systems — using the ChromaDB RAG database as the sole knowledge base.

No training required. Works immediately from the database built by
create_tscg_rag.py using two signals:
  1. Cosine similarity to M2 metaconcept NL summaries (ontology/docs segments)
  2. Cosine similarity to existing poclets and systemic frameworks

Usage (CLI):
  python metaconcept_classifier.py "A thermostat maintains temperature via negative feedback"
  python metaconcept_classifier.py "The immune system neutralises pathogens" --top-k 8
  python metaconcept_classifier.py "VSM recursively embeds viable systems" --verbose
  python metaconcept_classifier.py "..." --json

Usage (API):
  from tscg.engine.classifier import MetaconceptClassifier
  clf = MetaconceptClassifier()
  result = clf.classify("A thermostat maintains temperature via negative feedback")
  clf.display(result)

Author: Echopraxium with the collaboration of Claude AI
"""

import sys
import json
import hashlib
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from datetime import datetime

# Force UTF-8 output on Windows terminals
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# RAG database location: src/tscg/engine/classifier/ -> src/tscg/rag/db_tscg_rag
_SCRIPT_DIR = Path(__file__).resolve().parent
_DEFAULT_DB_PATH = str(_SCRIPT_DIR.parent.parent / "rag" / "db_tscg_rag")


# ==============================================================================
# DATA CLASSES
# ==============================================================================

@dataclass
class MetaconceptCandidate:
    """A ranked M2 metaconcept candidate for the input description."""
    label: str
    score: float                    # cosine similarity [0, 1]
    tensor_formula: Optional[str]
    definition_excerpt: str
    source_file: str
    uri: Optional[str] = None


@dataclass
class AnalogousSystem:
    """An existing poclet or systemic framework similar to the input."""
    name: str
    score: float
    source_file: str
    excerpt: str
    source_type: str = "poclet"     # "poclet" | "framework" | "case_study"


@dataclass
class ClassificationResult:
    """Full output of MetaconceptClassifier.classify()."""
    query: str
    metaconcept_candidates: List[MetaconceptCandidate] = field(default_factory=list)
    analogous_systems: List[AnalogousSystem] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())


# ==============================================================================
# CLASSIFIER
# ==============================================================================

class MetaconceptClassifier:
    """
    Zero-shot classifier mapping a NL system description to TSCG M2 metaconcepts.

    Uses the ChromaDB RAG database (built by create_tscg_rag.py) as its
    knowledge base — no training, no separate index, works immediately.

    Two query signals are combined:
      - ontology_doc segments  → M2 metaconcept candidates
      - system-models segments → analogous poclets / frameworks

    Example:
        >>> clf = MetaconceptClassifier()
        >>> result = clf.classify(
        ...     "A thermostat that maintains room temperature "
        ...     "through negative feedback and setpoint regulation"
        ... )
        >>> clf.display(result)
    """

    def __init__(
        self,
        db_path: str = _DEFAULT_DB_PATH,
        top_k_metaconcepts: int = 7,
        top_k_systems: int = 3,
        min_score: float = 0.30,
    ):
        """
        Args:
            db_path: Path to the ChromaDB database directory (or its .tar.gz).
            top_k_metaconcepts: Number of metaconcept candidates to return.
            top_k_systems: Number of analogous systems to return.
            min_score: Minimum cosine similarity to include a result [0, 1].
        """
        self.db_path = db_path
        self.top_k_metaconcepts = top_k_metaconcepts
        self.top_k_systems = top_k_systems
        self.min_score = min_score
        self._collection = None
        self._embedder = None
        self._metadata: Dict[str, Any] = {}

    # ------------------------------------------------------------------
    # Lazy initialisation
    # ------------------------------------------------------------------

    def _ensure_ready(self):
        """Connect to ChromaDB and load the embedder on first use."""
        if self._collection is not None:
            return

        if not _decompress_if_needed(self.db_path):
            raise FileNotFoundError(
                f"RAG database not found: {self.db_path}\n"
                f"Build it first:  python src/tscg/rag/create_tscg_rag.py local"
            )

        meta_path = Path(self.db_path) / "metadata.json"
        if meta_path.exists():
            with open(meta_path) as f:
                self._metadata = json.load(f)

        try:
            import chromadb
            from chromadb.config import Settings
        except ImportError:
            raise ImportError("chromadb not installed. Run:  pip install chromadb")

        client = chromadb.PersistentClient(
            path=self.db_path,
            settings=Settings(anonymized_telemetry=False),
        )
        self._collection = client.get_collection("tscg_rag")
        self._embedder = _load_embedder(self._metadata.get("embedding_model", "local"))

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def classify(
        self,
        description: str,
        top_k_metaconcepts: Optional[int] = None,
        top_k_systems: Optional[int] = None,
    ) -> ClassificationResult:
        """
        Classify a natural language system description.

        Args:
            description: NL description of a poclet, case study, or
                         systemic framework.
            top_k_metaconcepts: Override instance-level default.
            top_k_systems: Override instance-level default.

        Returns:
            ClassificationResult with ranked M2 candidates and analogous systems.
        """
        self._ensure_ready()

        top_k_mc = top_k_metaconcepts or self.top_k_metaconcepts
        top_k_sys = top_k_systems or self.top_k_systems

        # Embed once, reuse for both queries
        query_vec = _embed(self._embedder, self._metadata, description)

        return ClassificationResult(
            query=description,
            metaconcept_candidates=self._query_metaconcepts(query_vec, top_k_mc),
            analogous_systems=self._query_analogous_systems(query_vec, top_k_sys),
        )

    # ------------------------------------------------------------------
    # Internal query helpers
    # ------------------------------------------------------------------

    def _query_metaconcepts(
        self, query_vec: list, top_k: int
    ) -> List[MetaconceptCandidate]:
        """Query M2 jsonld_entry segments for metaconcept candidates."""
        raw = self._collection.query(
            query_embeddings=[query_vec],
            n_results=top_k * 3,            # over-fetch to absorb duplicates
            where={
                "$and": [
                    {"type": {"$eq": "jsonld_entry"}},
                    {"layer": {"$eq": "M2"}},
                ]
            },
        )

        candidates: List[MetaconceptCandidate] = []
        seen: set = set()

        for doc, meta, dist in zip(
            raw["documents"][0],
            raw["metadatas"][0],
            raw["distances"][0],
        ):
            score = 1.0 - dist
            if score < self.min_score:
                continue

            label = (
                meta.get("label")
                or meta.get("header")
                or Path(meta.get("source", "unknown")).stem
            )

            # Deduplicate by URI first, then fall back to label, then content hash
            dedup_key = meta.get("uri") or label or hashlib.md5(doc.encode()).hexdigest()
            if dedup_key in seen:
                continue
            seen.add(dedup_key)

            candidates.append(MetaconceptCandidate(
                label=label,
                score=round(score, 4),
                tensor_formula=_extract_formula(doc),
                definition_excerpt=doc[:300].replace("\n", " "),
                source_file=Path(meta.get("source", "")).name,
                uri=meta.get("uri"),
            ))

            if len(candidates) == top_k:
                break

        return candidates

    def _query_analogous_systems(
        self, query_vec: list, top_k: int
    ) -> List[AnalogousSystem]:
        """Query for segments from system-models/ to find analogous systems."""
        # Fetch broadly — system-models is a subset, so we need more candidates
        raw = self._collection.query(
            query_embeddings=[query_vec],
            n_results=top_k * 10,
        )

        systems: List[AnalogousSystem] = []
        seen_files: set = set()

        for doc, meta, dist in zip(
            raw["documents"][0],
            raw["metadatas"][0],
            raw["distances"][0],
        ):
            score = 1.0 - dist
            if score < self.min_score:
                continue

            source = meta.get("source", "").replace("\\", "/")
            if "system-models" not in source:
                continue

            src_name = Path(source).name
            if src_name in seen_files:
                continue
            seen_files.add(src_name)

            if "systemic-frameworks" in source:
                src_type = "framework"
            elif "poclets" in source:
                src_type = "poclet"
            else:
                src_type = "case_study"

            systems.append(AnalogousSystem(
                name=Path(source).stem,
                score=round(score, 4),
                source_file=src_name,
                excerpt=doc[:200].replace("\n", " "),
                source_type=src_type,
            ))

            if len(systems) == top_k:
                break

        return systems

    # ------------------------------------------------------------------
    # Output
    # ------------------------------------------------------------------

    def display(self, result: ClassificationResult, verbose: bool = False):
        """Pretty-print a ClassificationResult to stdout."""
        print("\n" + "=" * 70)
        print("  TSCG Metaconcept Classifier")
        print("=" * 70)
        print(f"Input : {result.query[:120]}")
        print(f"Time  : {result.timestamp}")

        # M2 metaconcept candidates
        print(f"\n{'─' * 70}")
        print(f"  M2 Metaconcept Candidates  ({len(result.metaconcept_candidates)})")
        print(f"{'─' * 70}")
        if not result.metaconcept_candidates:
            print("  No candidates above score threshold.")
        else:
            for i, mc in enumerate(result.metaconcept_candidates, 1):
                bar = _score_bar(mc.score)
                print(f"\n  {i:2}. {mc.label}")
                print(f"      Score  : {bar} {mc.score:.3f}")
                if mc.tensor_formula:
                    print(f"      Formula: {mc.tensor_formula}")
                if mc.uri:
                    print(f"      URI    : {mc.uri}")
                print(f"      Source : {mc.source_file}")
                if verbose:
                    print(f"      Excerpt: {mc.definition_excerpt}")

        # Analogous systems
        if result.analogous_systems:
            print(f"\n{'─' * 70}")
            print(f"  Analogous Systems  ({len(result.analogous_systems)})")
            print(f"{'─' * 70}")
            for i, sys_ in enumerate(result.analogous_systems, 1):
                bar = _score_bar(sys_.score)
                print(f"\n  {i:2}. [{sys_.source_type}] {sys_.name}")
                print(f"      Score  : {bar} {sys_.score:.3f}")
                print(f"      Source : {sys_.source_file}")
                if verbose:
                    print(f"      Excerpt: {sys_.excerpt}")

        print(f"\n{'=' * 70}\n")

    def to_dict(self, result: ClassificationResult) -> Dict[str, Any]:
        """Serialize a ClassificationResult to a JSON-serialisable dict."""
        return {
            "query": result.query,
            "timestamp": result.timestamp,
            "metaconcept_candidates": [
                {
                    "label": mc.label,
                    "score": mc.score,
                    "tensor_formula": mc.tensor_formula,
                    "uri": mc.uri,
                    "source_file": mc.source_file,
                    "definition_excerpt": mc.definition_excerpt,
                }
                for mc in result.metaconcept_candidates
            ],
            "analogous_systems": [
                {
                    "name": s.name,
                    "score": s.score,
                    "source_type": s.source_type,
                    "source_file": s.source_file,
                    "excerpt": s.excerpt,
                }
                for s in result.analogous_systems
            ],
        }


# ==============================================================================
# UTILITIES
# ==============================================================================

def _decompress_if_needed(db_path: str) -> bool:
    """Decompress .tar.gz archive if the db directory is absent."""
    import tarfile
    db = Path(db_path)
    archive = db.parent / f"{db.name}.tar.gz"
    if db.exists():
        return True
    if not archive.exists():
        return False
    print(f"Decompressing {archive.name} ...")
    with tarfile.open(archive, "r:gz") as tar:
        tar.extractall(db.parent)
    print(f"Decompressed to {db_path}")
    return True


def _load_embedder(mode: str):
    """Load the embedding model matching the one used to build the DB."""
    if "MiniLM" in mode or mode == "local":
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError:
            raise ImportError(
                "sentence-transformers not installed. "
                "Run:  pip install sentence-transformers"
            )
        return SentenceTransformer("all-MiniLM-L6-v2")
    else:
        try:
            from langchain_google_genai import GoogleGenerativeAIEmbeddings
        except ImportError:
            raise ImportError(
                "langchain-google-genai not installed. "
                "Run:  pip install langchain-google-genai"
            )
        return GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")


def _embed(embedder, metadata: dict, text: str) -> list:
    """Embed a string and return a plain Python list."""
    mode = metadata.get("embedding_model", "local")
    if "MiniLM" in mode or mode == "local":
        return embedder.encode([text])[0].tolist()
    else:
        return embedder.embed_query(text)


def _fix_mojibake(text: str) -> str:
    """
    Repair UTF-8 text that was decoded as cp1252 (Windows mojibake).

    Applies up to two rounds of encode('cp1252') → decode('utf-8') to handle
    both single-mojibake (e.g. 'âŠ—' → '⊗') and double-mojibake
    (e.g. 'Ã¢Å â€"' → '⊗').  Returns the original string unchanged if it
    contains no cp1252-encodable/UTF-8-decodable mojibake.
    """
    for _ in range(2):
        try:
            fixed = text.encode("cp1252").decode("utf-8")
            text = fixed
        except (UnicodeEncodeError, UnicodeDecodeError):
            break
    return text


def _extract_formula(text: str) -> Optional[str]:
    """
    Extract a tensor formula from an _entry_to_text() NL summary.
    Matches lines like:  Tensor formula: A ⊗ S ⊗ F (Attractor, Structure, Flow)
    Repairs cp1252 mojibake that may be present in the indexed document text.
    """
    for line in text.splitlines():
        low = line.lower()
        if "tensor formula" in low or ("formula" in low and ":" in line):
            parts = line.split(":", 1)
            if len(parts) == 2 and parts[1].strip():
                return _fix_mojibake(parts[1].strip())
    return None


def _score_bar(score: float, width: int = 12) -> str:
    """ASCII progress bar for a [0, 1] score."""
    filled = round(score * width)
    return "[" + "█" * filled + "░" * (width - filled) + "]"


# ==============================================================================
# CLI ENTRY POINT
# ==============================================================================

def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="TSCG Zero-Shot Metaconcept Classifier",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXAMPLES:
  python metaconcept_classifier.py "A thermostat maintains temperature via negative feedback"
  python metaconcept_classifier.py "The immune system neutralises pathogens" --top-k 8
  python metaconcept_classifier.py "VSM recursively embeds viable systems" --verbose
  python metaconcept_classifier.py "..." --json
        """,
    )
    parser.add_argument("description", help="Natural language system description")
    parser.add_argument(
        "--db",
        default=_DEFAULT_DB_PATH,
        help=f"ChromaDB path (default: {_DEFAULT_DB_PATH})",
    )
    parser.add_argument(
        "--top-k", type=int, default=7,
        help="Number of metaconcept candidates (default: 7)",
    )
    parser.add_argument(
        "--top-k-systems", type=int, default=3,
        help="Number of analogous systems (default: 3)",
    )
    parser.add_argument(
        "--min-score", type=float, default=0.30,
        help="Minimum cosine similarity threshold (default: 0.30)",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="Show definition excerpts and system excerpts",
    )
    parser.add_argument(
        "--json", dest="as_json", action="store_true",
        help="Output result as JSON",
    )
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    clf = MetaconceptClassifier(
        db_path=args.db,
        top_k_metaconcepts=args.top_k,
        top_k_systems=args.top_k_systems,
        min_score=args.min_score,
    )
    result = clf.classify(args.description)
    if args.as_json:
        print(json.dumps(clf.to_dict(result), ensure_ascii=False, indent=2))
    else:
        clf.display(result, verbose=args.verbose)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nInterrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
