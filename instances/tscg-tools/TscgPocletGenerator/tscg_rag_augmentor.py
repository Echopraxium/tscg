"""
tscg_rag_augmentor.py
=====================
TSCG RAG Augmentor — Reformulates user requests using TSCG ontological grammar.
Author: Echopraxium with the collaboration of Claude AI

Integrates with tscg_poclet_generator.py via a dedicated "Augment with RAG" button.

Architecture:
  User request
      ↓
  ChromaDB query (db_tscg_rag)
      ↓
  Top-K relevant TSCG chunks (poclet examples, GenericConcepts, READMEs, simulations)
      ↓
  Augmented system prompt (Smart Prompt + RAG context)
      ↓
  LLM → output "in TSCG grammar"

Dependencies:
  pip install chromadb sentence-transformers PySide6

Usage (standalone):
    augmentor = TscgRagAugmentor(db_path="src/tscg/rag/db_tscg_rag")
    result = augmentor.augment("model the human heart as a poclet")
    print(result.augmented_prompt)
    print(result.sources_summary)

Usage (PySide6 integration):
    See tscg_rag_augmentor_patch.md for the full integration guide.
"""

import os
import tarfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Optional dependency guard
# ---------------------------------------------------------------------------
try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DEFAULT_DB_PATH    = "src/tscg/rag/db_tscg_rag"
DEFAULT_TAR_PATH   = "src/tscg/rag/db_tscg_rag.tar"
DEFAULT_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
DEFAULT_COLLECTION = "tscg_rag"
DEFAULT_TOP_K      = 6

CHUNK_TYPE_LABELS = {
    "jsonld_entry"   : "📐 Ontology",
    "markdown_block" : "📄 Documentation",
    "python_block"   : "🐍 Simulation",
    "readme_block"   : "📖 README",
}

RAG_CONTEXT_HEADER = """
========================================================================
TSCG FRAMEWORK CONTEXT (retrieved from knowledge base)
The following excerpts from validated TSCG ontologies, documentation,
and simulation examples provide the exact "grammar" to use in your response.
Apply their structure, terminology, and patterns faithfully.
========================================================================
"""

RAG_CONTEXT_FOOTER = """
========================================================================
END OF TSCG CONTEXT — Now apply the above grammar to the user's request.
========================================================================
"""


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class RagChunk:
    """A single retrieved chunk from the TSCG knowledge base."""
    text     : str
    source   : str
    distance : float
    doc_type : str = ""

    @property
    def type_label(self) -> str:
        return CHUNK_TYPE_LABELS.get(self.doc_type, "📦 Chunk")

    @property
    def short_source(self) -> str:
        return Path(self.source).name if self.source else "unknown"

    def format_for_prompt(self) -> str:
        return (
            f"--- [{self.type_label}] {self.short_source} "
            f"(relevance: {1.0 - self.distance:.2f}) ---\n"
            f"{self.text.strip()}\n"
        )

    def format_for_display(self, max_chars: int = 300) -> str:
        excerpt = self.text.strip()[:max_chars]
        if len(self.text.strip()) > max_chars:
            excerpt += "..."
        return (
            f"{self.type_label}  {self.short_source}  "
            f"[score: {1.0 - self.distance:.2f}]\n"
            f"{excerpt}\n"
        )


@dataclass
class AugmentResult:
    """Result of a RAG augmentation call."""
    user_request     : str
    chunks           : list = field(default_factory=list)
    augmented_prompt : str  = ""
    sources_summary  : str  = ""
    error            : Optional[str] = None

    @property
    def success(self) -> bool:
        return self.error is None and len(self.chunks) > 0

    @property
    def chunk_count(self) -> int:
        return len(self.chunks)


# ---------------------------------------------------------------------------
# Core class
# ---------------------------------------------------------------------------

class TscgRagAugmentor:
    """
    Queries the TSCG ChromaDB knowledge base and augments LLM prompts
    with relevant ontological context.

    Lazy initialization: ChromaDB client and embedding model are loaded
    on the first call to augment() / query(), not at __init__.
    This keeps application startup fast.
    """

    def __init__(
        self,
        db_path    : str = DEFAULT_DB_PATH,
        tar_path   : str = DEFAULT_TAR_PATH,
        model_name : str = DEFAULT_MODEL_NAME,
        collection : str = DEFAULT_COLLECTION,
        top_k      : int = DEFAULT_TOP_K,
        verbose    : bool = False,
    ):
        self.db_path    = Path(db_path)
        self.tar_path   = Path(tar_path)
        self.model_name = model_name
        self.collection = collection
        self.top_k      = top_k
        self.verbose    = verbose

        self._client   = None
        self._col      = None
        self._embedder = None
        self._ready    = False

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def is_available(self) -> tuple[bool, str]:
        """Check dependencies and DB presence. Returns (ok, message)."""
        if not CHROMADB_AVAILABLE:
            return False, "chromadb not installed — run: pip install chromadb"
        if not SENTENCE_TRANSFORMERS_AVAILABLE:
            return False, "sentence-transformers not installed — run: pip install sentence-transformers"
        if not self.db_path.exists():
            if self.tar_path.exists():
                return True, f"⚠ DB not extracted yet — will auto-extract from {self.tar_path.name}"
            return False, f"RAG database not found at '{self.db_path}' (no .tar found either)"
        return True, "✓ RAG database ready"

    def initialize(self) -> tuple[bool, str]:
        """Load ChromaDB + embedding model. Auto-extracts tar if needed."""
        if self._ready:
            return True, "Already initialized"

        if not self.db_path.exists():
            ok, msg = self._extract_tar()
            if not ok:
                return False, msg

        try:
            self._client = chromadb.PersistentClient(
                path=str(self.db_path),
                settings=Settings(anonymized_telemetry=False),
            )
            collections = [c.name for c in self._client.list_collections()]
            if self.verbose:
                print(f"[RAG] Collections: {collections}")

            if self.collection in collections:
                self._col = self._client.get_collection(self.collection)
            elif collections:
                self._col = self._client.get_collection(collections[0])
                if self.verbose:
                    print(f"[RAG] Using collection '{collections[0]}'")
            else:
                return False, "No collections in RAG database. Rebuild with create_tscg_rag.py."
        except Exception as e:
            return False, f"ChromaDB error: {e}"

        try:
            if self.verbose:
                print(f"[RAG] Loading embedding model '{self.model_name}'...")
            self._embedder = SentenceTransformer(self.model_name)
        except Exception as e:
            return False, f"Embedding model error: {e}"

        self._ready = True
        count = self._col.count()
        return True, f"✓ RAG initialized — {count} chunks in collection '{self._col.name}'"

    def query(self, user_request: str, top_k: Optional[int] = None) -> list:
        """Query the knowledge base. Auto-initializes if needed."""
        if not self._ready:
            ok, msg = self.initialize()
            if not ok:
                if self.verbose:
                    print(f"[RAG] Init failed: {msg}")
                return []

        k = top_k or self.top_k
        try:
            embedding = self._embedder.encode([user_request]).tolist()
            results   = self._col.query(
                query_embeddings=embedding,
                n_results=min(k, self._col.count()),
                include=["documents", "metadatas", "distances"],
            )
        except Exception as e:
            if self.verbose:
                print(f"[RAG] Query error: {e}")
            return []

        chunks    = []
        docs      = results.get("documents",  [[]])[0]
        metas     = results.get("metadatas",  [[]])[0]
        distances = results.get("distances",  [[]])[0]

        for doc, meta, dist in zip(docs, metas, distances):
            chunks.append(RagChunk(
                text     = doc,
                source   = meta.get("source", ""),
                distance = float(dist),
                doc_type = meta.get("type", ""),
            ))
        return chunks

    def augment(
        self,
        user_request  : str,
        system_prompt : str = "",
        top_k         : Optional[int] = None,
    ) -> AugmentResult:
        """
        Main entry point: query RAG and build the augmented system prompt.
        The augmented_prompt is ready for direct injection into the LLM call.
        """
        result = AugmentResult(user_request=user_request)

        ok, msg = self.is_available()
        if not ok:
            result.error = msg
            return result

        chunks = self.query(user_request, top_k=top_k)
        if not chunks:
            result.error = "No relevant chunks found in the RAG database."
            return result

        result.chunks = chunks

        # Build RAG context block
        context_blocks = [RAG_CONTEXT_HEADER.strip()]
        for i, chunk in enumerate(chunks, 1):
            context_blocks.append(f"[{i}/{len(chunks)}] {chunk.format_for_prompt()}")
        context_blocks.append(RAG_CONTEXT_FOOTER.strip())
        rag_context = "\n\n".join(context_blocks)

        result.augmented_prompt = (
            (system_prompt.rstrip() + "\n\n" + rag_context)
            if system_prompt.strip()
            else rag_context
        )

        label = f'"{user_request[:60]}..."' if len(user_request) > 60 else f'"{user_request}"'
        lines = [f"📚 {len(chunks)} TSCG chunks retrieved for: {label}", ""]
        for i, chunk in enumerate(chunks, 1):
            lines.append(
                f"  {i}. {chunk.type_label}  {chunk.short_source}  "
                f"[score: {1.0 - chunk.distance:.2f}]"
            )
        result.sources_summary = "\n".join(lines)

        return result

    def format_chunks_for_display(self, chunks: list, max_chars: int = 300) -> str:
        if not chunks:
            return "No chunks retrieved."
        lines = []
        for i, chunk in enumerate(chunks, 1):
            lines.append("─" * 60)
            lines.append(f"[{i}] {chunk.format_for_display(max_chars)}")
        lines.append("─" * 60)
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _extract_tar(self) -> tuple[bool, str]:
        if not self.tar_path.exists():
            return False, f"Archive not found: {self.tar_path}"
        try:
            if self.verbose:
                print(f"[RAG] Extracting {self.tar_path.name}...")
            with tarfile.open(self.tar_path, "r") as tar:
                tar.extractall(path=self.tar_path.parent)
            return True, f"Extracted to {self.db_path}"
        except Exception as e:
            return False, f"Extraction failed: {e}"


# ---------------------------------------------------------------------------
# PySide6 widget
# ---------------------------------------------------------------------------

class RagAugmentorWidget:
    """
    Ready-to-use PySide6 panel for the RAG Augmentor.
    Drop into tscg_poclet_generator.py with minimal wiring.

    Usage:
        from tscg_rag_augmentor import TscgRagAugmentor, RagAugmentorWidget

        augmentor  = TscgRagAugmentor(db_path="src/tscg/rag/db_tscg_rag")
        rag_widget = RagAugmentorWidget(
            parent         = some_qwidget,
            augmentor      = augmentor,
            on_augment_cb  = self._on_rag_augmented,   # receives augmented_prompt str
            get_request_cb = self._get_current_request, # returns user request str
        )
        some_layout.addWidget(rag_widget.group_box)
    """

    def __init__(self, parent, augmentor: TscgRagAugmentor,
                 on_augment_cb=None, get_request_cb=None):
        try:
            from PySide6.QtWidgets import (
                QGroupBox, QVBoxLayout, QHBoxLayout, QLabel,
                QPushButton, QSpinBox, QPlainTextEdit,
                QMessageBox, QSizePolicy,
            )
            from PySide6.QtGui import QFont
            from PySide6.QtCore import Qt
        except ImportError:
            raise RuntimeError("PySide6 not available — run: pip install PySide6")

        self._QMessageBox  = QMessageBox
        self._QPlainTextEdit_End = QPlainTextEdit  # kept for moveCursor ref
        self.augmentor       = augmentor
        self.on_augment_cb   = on_augment_cb
        self.get_request_cb  = get_request_cb

        # ── Group box ──────────────────────────────────────────────────
        self.group_box = QGroupBox("🔍 RAG Augmentor", parent)
        root = QVBoxLayout(self.group_box)
        root.setContentsMargins(8, 8, 8, 8)
        root.setSpacing(6)

        # Status label
        self._status_label = QLabel("RAG: not initialized")
        self._status_label.setStyleSheet(
            "color:#888888; font-size:9pt; font-family:monospace;"
        )
        root.addWidget(self._status_label)

        # Controls row
        ctrl = QHBoxLayout()
        ctrl.setSpacing(8)
        ctrl.addWidget(QLabel("Top-K:"))

        self._spin_topk = QSpinBox()
        self._spin_topk.setRange(1, 20)
        self._spin_topk.setValue(augmentor.top_k)
        self._spin_topk.setFixedWidth(56)
        ctrl.addWidget(self._spin_topk)

        self._btn_init = QPushButton("⚡ Initialize RAG")
        self._btn_init.setStyleSheet(
            "QPushButton{background:#5a9a5a;color:white;font-size:9pt;"
            "padding:4px 10px;border-radius:4px;}"
            "QPushButton:hover{background:#4a8a4a;}"
            "QPushButton:disabled{background:#888;}"
        )
        self._btn_init.clicked.connect(self._on_init_click)
        ctrl.addWidget(self._btn_init)

        self._btn_augment = QPushButton("🔍 Augment with RAG")
        self._btn_augment.setStyleSheet(
            "QPushButton{background:#4a7ebf;color:white;font-weight:bold;"
            "font-size:10pt;padding:4px 14px;border-radius:4px;}"
            "QPushButton:hover{background:#3a6eaf;}"
            "QPushButton:disabled{background:#888;}"
        )
        self._btn_augment.clicked.connect(self._on_augment_click)
        ctrl.addWidget(self._btn_augment)

        ctrl.addStretch()
        root.addLayout(ctrl)

        # Output area
        self._output = QPlainTextEdit()
        self._output.setReadOnly(True)
        self._output.setMinimumHeight(160)
        self._output.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._output.setFont(QFont("Courier New", 9))
        self._output.setStyleSheet(
            "QPlainTextEdit{background:#1e1e1e;color:#d4d4d4;border:1px solid #444;}"
        )
        root.addWidget(self._output)

        # Initial availability check
        ok, msg = augmentor.is_available()
        self._set_status(msg, ok=ok)

    # ------------------------------------------------------------------
    # Slots
    # ------------------------------------------------------------------

    def _on_init_click(self):
        self._set_status("⏳ Initializing RAG database...", ok=True)
        self._btn_init.setEnabled(False)
        self._run_in_thread(
            task    = lambda: self.augmentor.initialize(),
            on_done = self._after_init,
        )

    def _after_init(self, result):
        ok, msg = result
        self._btn_init.setEnabled(True)
        self._set_status(msg, ok=ok)
        if ok:
            self._write_output(f"✓ {msg}\n")

    def _on_augment_click(self):
        request = self.get_request_cb() if self.get_request_cb else ""
        if not request.strip():
            self._QMessageBox.warning(
                self.group_box, "RAG Augmentor",
                "Please enter a poclet request first."
            )
            return
        self._set_status("⏳ Querying knowledge base...", ok=True)
        self._btn_augment.setEnabled(False)
        top_k = self._spin_topk.value()
        self._run_in_thread(
            task    = lambda: self.augmentor.augment(request, top_k=top_k),
            on_done = self._after_augment,
        )

    def _after_augment(self, result: AugmentResult):
        self._btn_augment.setEnabled(True)
        if not result.success:
            self._set_status(f"✗ {result.error}", ok=False)
            self._write_output(f"Error: {result.error}\n")
            return

        self._set_status(f"✓ {result.chunk_count} chunks retrieved", ok=True)
        self._write_output(
            result.sources_summary
            + "\n\n"
            + self.augmentor.format_chunks_for_display(result.chunks, max_chars=400)
        )
        if self.on_augment_cb:
            self.on_augment_cb(result.augmented_prompt)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _set_status(self, msg: str, ok: bool = True):
        color = "#2d7a2d" if ok else "#b03030"
        self._status_label.setText(msg)
        self._status_label.setStyleSheet(
            f"color:{color}; font-size:9pt; font-family:monospace;"
        )

    def _write_output(self, text: str):
        self._output.setPlainText(text)
        cursor = self._output.textCursor()
        from PySide6.QtGui import QTextCursor
        cursor.movePosition(QTextCursor.End)
        self._output.setTextCursor(cursor)

    def _run_in_thread(self, task, on_done):
        """Run a blocking task in a QThread; deliver result to the GUI thread."""
        from PySide6.QtCore import QThread, QObject, Signal

        class _Worker(QObject):
            finished = Signal(object)

            def __init__(self, fn):
                super().__init__()
                self._fn = fn

            def run(self):
                self.finished.emit(self._fn())

        thread = QThread(self.group_box)
        worker = _Worker(task)
        worker.moveToThread(thread)
        thread.started.connect(worker.run)
        worker.finished.connect(lambda r: (thread.quit(), on_done(r)))
        worker.finished.connect(worker.deleteLater)
        thread.finished.connect(thread.deleteLater)
        thread.start()


# ---------------------------------------------------------------------------
# CLI test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys

    request = " ".join(sys.argv[1:]) or "model the human heart as a poclet"
    db      = os.environ.get("TSCG_RAG_DB", DEFAULT_DB_PATH)

    print(f"\n{'='*70}")
    print(f"  TSCG RAG Augmentor — CLI test")
    print(f"  DB path  : {db}")
    print(f"  Request  : {request}")
    print(f"{'='*70}\n")

    aug = TscgRagAugmentor(db_path=db, verbose=True)

    ok, msg = aug.is_available()
    print(f"Available : {msg}\n")

    ok, msg = aug.initialize()
    print(f"Init      : {msg}\n")
    if not ok:
        sys.exit(1)

    result = aug.augment(request)
    if not result.success:
        print(f"Error: {result.error}")
        sys.exit(1)

    print(result.sources_summary)
    print()
    print("─── Augmented system prompt preview (first 1000 chars) ───")
    print(result.augmented_prompt[:1000])
    print("...")
