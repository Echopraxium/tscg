"""
tscg_poclet_generator.py
========================
TSCG Poclet Generator — PySide6 Desktop Application
Author: Echopraxium with the collaboration of Claude AI

Supports 4 LLM backends:
  - Anthropic Claude API
  - Google Gemini (free tier via aistudio)
  - Ollama (local)
  - OpenAI-compatible (LM Studio, Jan, vLLM, etc.)

Features:
  - RAG Augmentor panel (requires tscg_rag_augmentor.py)
  - Tabbed output: M0 JSON-LD / README / sim.py
  - JSON-LD and Python syntax highlighting
  - Save current tab or all files at once
  - Generation history
  - Load existing poclet (.jsonld)
  - README template selector
  - sim.py UI layout template selector
  - Non-blocking generation (QThread)
  - Dark theme, settings persistence (QSettings)

Dependencies:
  pip install PySide6 anthropic google-genai openai requests
  pip install chromadb sentence-transformers   # optional, for RAG
"""

import sys
print('[TSCG] Python interpreter started', flush=True)
print('[TSCG] Loading stdlib modules...', flush=True)
import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Optional

import warnings
# Suppress Google warnings (quota-project, deprecated SDK, Python version)
warnings.filterwarnings('ignore', message='.*quota project.*',
    category=UserWarning, module='google.auth._default')
warnings.filterwarnings('ignore', category=FutureWarning,
    module='google')
warnings.filterwarnings('ignore', category=FutureWarning,
    module='google.api_core')
import os
os.environ.setdefault('GRPC_VERBOSITY', 'ERROR')   # silence gRPC logs
os.environ.setdefault('GLOG_minloglevel', '3')     # silence Abseil logs

print('[TSCG] Loading PySide6 (may take a few seconds on first run)...', flush=True)
from PySide6.QtCore import Qt, QThread, Signal, QObject, QSettings, QTimer, QRect
from PySide6.QtGui import (
    QFont, QSyntaxHighlighter, QTextCharFormat, QColor,
    QTextCursor, QPalette, QPainter, QPixmap, QBitmap,
)
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QLabel, QLineEdit, QPlainTextEdit,
    QPushButton, QComboBox, QTabWidget, QGroupBox, QSplitter, QSplitterHandle,
    QProgressBar, QStatusBar, QFileDialog, QMessageBox,
    QListWidget, QListWidgetItem, QSizePolicy,
    QDialog, QDialogButtonBox,
)

# ---------------------------------------------------------------------------
# Custom splitter handle — required under Fusion + dark palette on Windows.
# ---------------------------------------------------------------------------
class DragHandle(QSplitterHandle):
    def paintEvent(self, event):
        painter = QPainter(self)
        r = self.rect()
        painter.fillRect(r, QColor("#444"))
        if self.orientation() == Qt.Orientation.Vertical:
            mid = r.height() // 2
            painter.fillRect(
                QRect(r.left() + 20, mid - 1, r.width() - 40, 2), QColor("#888"))
        else:
            mid = r.width() // 2
            painter.fillRect(
                QRect(mid - 1, r.top() + 20, 2, r.height() - 40), QColor("#888"))

    def sizeHint(self):
        sh = super().sizeHint()
        if self.orientation() == Qt.Orientation.Vertical:
            sh.setHeight(8)
        else:
            sh.setWidth(8)
        return sh


class _Splitter(QSplitter):
    """QSplitter that always uses DragHandle — fixes Fusion/dark on Windows."""
    def createHandle(self):
        return DragHandle(self.orientation(), self)


# RAG Augmentor — imported lazily after window shows (chromadb/PyTorch are slow)
RAG_AVAILABLE      = False   # updated by _RagLoader thread
TscgRagAugmentor   = None    # type: ignore
RagAugmentorWidget = None    # type: ignore
print('[TSCG] RAG import deferred to background thread', flush=True)

# ---------------------------------------------------------------------------
# Repository root resolution
# Walks upward from this script until src/tscg/rag/ is found.
# Falls back to the script's own directory if the layout is flat.
# ---------------------------------------------------------------------------
def _find_repo_root() -> Path:
    candidate = Path(__file__).resolve().parent
    for _ in range(8):
        if (candidate / "src" / "tscg" / "rag").exists():
            return candidate
        parent = candidate.parent
        if parent == candidate:
            break
        candidate = parent
    return Path(__file__).resolve().parent   # flat layout fallback

_REPO_ROOT = _find_repo_root()
_RAG_DB   = _REPO_ROOT / "src" / "tscg" / "rag" / "db_tscg_rag"
_RAG_TAR  = _REPO_ROOT / "src" / "tscg" / "rag" / "db_tscg_rag.tar"

APP_NAME    = "TSCG Poclet Generator"
APP_VERSION = "1.0.0"
APP_AUTHOR  = "Echopraxium with the collaboration of Claude AI"

# ---------------------------------------------------------------------------
# Backend definitions
# ---------------------------------------------------------------------------

BACKENDS = {
    "Anthropic": {
        "models"          : ["claude-opus-4-5", "claude-sonnet-4-5", "claude-haiku-4-5"],
        "needs_key"       : True,
        "needs_endpoint"  : False,
        "auth_modes"      : ["API Key", "Google Auth (Vertex AI)"],
        "key_placeholder" : "sk-ant-…",
    },
    "Gemini": {
        "models"          : ["gemini-2.0-flash", "gemini-1.5-pro", "gemini-1.5-flash"],
        "needs_key"       : True,
        "needs_endpoint"  : False,
        "auth_modes"      : ["API Key", "Google Auth (ADC)"],
        "key_placeholder" : "AIzaSy…  (aistudio.google.com)",
    },
    "Ollama": {
        "models"          : ["llama3.2", "llama3.1", "mistral", "qwen2.5", "deepseek-r1"],
        "needs_key"       : False,
        "needs_endpoint"  : True,
        "auth_modes"      : [],
        "default_endpoint": "http://localhost:11434",
    },
    "OpenAI-compatible": {
        "models"          : ["local-model", "lm-studio-model"],
        "needs_key"       : False,
        "needs_endpoint"  : True,
        "auth_modes"      : [],
        "default_endpoint": "http://localhost:1234/v1",
    },
}

# ---------------------------------------------------------------------------
# README templates
# ---------------------------------------------------------------------------

README_TEMPLATES = {
    "Standard": (
        "# {system_name} Poclet\n\n"
        "## Overview\n{description}\n\n"
        "## TSCG Analysis\n\n"
        "### ASFID (Territory — Eagle Eye)\n"
        "| Dimension | Score | Description |\n"
        "|-----------|-------|-------------|\n"
        "| A (Attractor)  | - | |\n"
        "| S (Structure)  | - | |\n"
        "| F (Flow)       | - | |\n"
        "| I (Information)| - | |\n"
        "| D (Dynamics)   | - | |\n\n"
        "### REVOI (Map — Sphinx Eye)\n"
        "| Dimension            | Score | Description |\n"
        "|----------------------|-------|-------------|\n"
        "| R (Representability) | - | |\n"
        "| E (Evolvability)     | - | |\n"
        "| V (Verifiability)    | - | |\n"
        "| O (Observability)    | - | |\n"
        "| I (Interoperability) | - | |\n\n"
        "### Epistemic Gap δ\n`δ = ||ASFID - REVOI|| = -`\n\n"
        "## GenericConcepts Mobilized\n- ...\n\n"
        "## Run simulation\n`python {sim_name}_sim.py`\n"
    ),
    "Minimal": (
        "# {system_name}\n\n{description}\n\n"
        "**Domain:** {domain}  \n"
        "**ASFID mean:** -  **REVOI mean:** -  **δ:** -\n\n"
        "## Key GenericConcepts\n- ...\n\n"
        "## Run simulation\n`python {sim_name}_sim.py`\n"
    ),
    "Academic": (
        "# {system_name} — TSCG Poclet Analysis\n\n"
        "**Framework:** TSCG v15.9.0  \n"
        "**Author:** {author}  \n"
        "**Date:** {date}  \n"
        "**Domain:** {domain}\n\n"
        "---\n\n"
        "## Abstract\n{description}\n\n"
        "---\n\n"
        "## 1. Territory Space (ASFID / Eagle Eye)\n...\n\n"
        "## 2. Map Space (REVOI / Sphinx Eye)\n...\n\n"
        "## 3. Epistemic Gap Analysis\n...\n\n"
        "## 4. GenericConcepts Mobilized\n...\n\n"
        "## 5. Transdisciplinary Validation\n...\n\n"
        "## References\n"
        "- Korzybski, A. (1933). *Science and Sanity*.\n"
        "- TSCG Framework v15.9.0 — https://github.com/Echopraxium/tscg\n"
    ),
}

SIM_TEMPLATES = {
    "Radial (default)"  : "radial",
    "Linear horizontal" : "linear_h",
    "Linear vertical"   : "linear_v",
    "Grid 2×N"          : "grid",
    "FSM state diagram" : "fsm",
}

# ---------------------------------------------------------------------------
# Syntax highlighters
# ---------------------------------------------------------------------------

class JsonLdHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        self._rules = []

        def rule(pattern, r, g, b, bold=False):
            fmt = QTextCharFormat()
            fmt.setForeground(QColor(r, g, b))
            if bold:
                fmt.setFontWeight(QFont.Bold)
            self._rules.append((re.compile(pattern), fmt))

        rule(r':\s*"[^"]*"',             206, 145, 120)   # string values
        rule(r'"[^"]*"\s*:',             156, 220, 254)   # keys
        rule(r'\b\d+\.?\d*\b',           181, 206, 168)   # numbers
        rule(r'\b(true|false|null)\b',    86, 156, 214, bold=True)
        rule(r'[{}\[\]]',               255, 215,   0)   # braces
        rule(r'"@[a-zA-Z]+"',            78, 201, 176, bold=True)  # @keywords
        rule(r'"(m[0-3]|dcterms|owl|rdf|rdfs|skos|xsd):[^"]*"', 220, 180, 100)

    def highlightBlock(self, text):
        for pattern, fmt in self._rules:
            for m in pattern.finditer(text):
                self.setFormat(m.start(), m.end() - m.start(), fmt)


class PythonHighlighter(QSyntaxHighlighter):
    _KEYWORDS = (
        r'\b(def|class|import|from|return|if|else|elif|for|while|in|not|and|or'
        r'|True|False|None|with|as|try|except|raise|pass|break|continue'
        r'|lambda|yield|global|nonlocal|self)\b'
    )

    def __init__(self, document):
        super().__init__(document)
        self._rules = []

        def rule(pattern, r, g, b, bold=False):
            fmt = QTextCharFormat()
            fmt.setForeground(QColor(r, g, b))
            if bold:
                fmt.setFontWeight(QFont.Bold)
            self._rules.append((re.compile(pattern), fmt))

        rule(self._KEYWORDS,        197, 134, 192, bold=True)
        rule(r'#[^\n]*',            106, 153,  85)
        rule(r'"""[\s\S]*?"""',     206, 145, 120)
        rule(r"'''[\s\S]*?'''",     206, 145, 120)
        rule(r'"[^"]*"',            206, 145, 120)
        rule(r"'[^']*'",            206, 145, 120)
        rule(r'\b\d+\.?\d*\b',      181, 206, 168)
        rule(r'\b(pygame|sys|os|math|json|re|Path)\b', 78, 201, 176)

    def highlightBlock(self, text):
        for pattern, fmt in self._rules:
            for m in pattern.finditer(text):
                self.setFormat(m.start(), m.end() - m.start(), fmt)


# ---------------------------------------------------------------------------
# LLM worker thread
# ---------------------------------------------------------------------------

class LlmWorker(QObject):
    finished = Signal(str)
    error    = Signal(str)

    def __init__(self, backend, model, api_key, endpoint,
                 system_prompt, user_request, max_tokens=8192,
                 auth_mode='API Key'):
        super().__init__()
        self.backend       = backend
        self.model         = model
        self.api_key       = api_key
        self.endpoint      = endpoint
        self.system_prompt = system_prompt
        self.user_request  = user_request
        self.max_tokens    = max_tokens
        self.auth_mode     = auth_mode

    def run(self):
        try:
            self.finished.emit(self._call())
        except Exception as e:
            self.error.emit(str(e))

    def _call(self) -> str:
        b = self.backend
        if b == "Anthropic":
            return self._anthropic()
        if b == "Gemini":
            return self._gemini()
        if b == "Ollama":
            return self._ollama()
        if b == "OpenAI-compatible":
            return self._openai_compat()
        raise ValueError(f"Unknown backend: {b}")

    def _anthropic(self) -> str:
        if self.auth_mode == 'Google Auth (Vertex AI)':
            from anthropic import AnthropicVertex
            import google.auth, google.auth.transport.requests
            creds, project = google.auth.default()
            try:
                creds.refresh(google.auth.transport.requests.Request())
            except Exception:
                pass
            project = self.gcp_project or project
            if not project:
                raise RuntimeError(
                    'No GCP Project ID found.\n'
                    'Enter it in the "GCP Project ID" field\n'
                    'or run: gcloud config set project YOUR_PROJECT_ID')
            c = AnthropicVertex(region='us-east5', project_id=project)
            msg = c.messages.create(
                model=self.model, max_tokens=self.max_tokens,
                system=self.system_prompt,
                messages=[{'role': 'user', 'content': self.user_request}],
            )
        else:
            import anthropic
            c = anthropic.Anthropic(api_key=self.api_key)
            msg = c.messages.create(
                model=self.model, max_tokens=self.max_tokens,
                system=self.system_prompt,
                messages=[{'role': 'user', 'content': self.user_request}],
            )
        return msg.content[0].text

    def _gemini(self) -> str:
        # New SDK: google-genai (replaces deprecated google-generativeai)
        from google import genai
        from google.genai import types
        if self.api_key:
            client = genai.Client(api_key=self.api_key)
        else:
            # ADC — uses gcloud credentials
            import google.auth
            creds, _ = google.auth.default(
                scopes=['https://www.googleapis.com/auth/generative-language']
            )
            client = genai.Client(credentials=creds)
        response = client.models.generate_content(
            model=self.model,
            contents=self.user_request,
            config=types.GenerateContentConfig(
                system_instruction=self.system_prompt,
                max_output_tokens=self.max_tokens,
            ),
        )
        return response.text

    def _ollama(self) -> str:
        import requests
        url = self.endpoint.rstrip("/") + "/api/chat"
        r = requests.post(url, json={
            "model": self.model, "stream": False,
            "messages": [
                {"role": "system", "content": self.system_prompt},
                {"role": "user",   "content": self.user_request},
            ],
        }, timeout=300)
        r.raise_for_status()
        return r.json()["message"]["content"]

    def _openai_compat(self) -> str:
        from openai import OpenAI
        c = OpenAI(api_key=self.api_key or "local", base_url=self.endpoint)
        r = c.chat.completions.create(
            model=self.model, max_tokens=self.max_tokens,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user",   "content": self.user_request},
            ],
        )
        return r.choices[0].message.content


# ---------------------------------------------------------------------------
# Google identity probe worker — runs google.auth in background
# ---------------------------------------------------------------------------

class _GoogleProbeWorker(QObject):
    # (email, picture_url_or_None, error_or_None)
    result = Signal(str, str, str)

    def run(self):
        try:
            import google.auth, google.auth.transport.requests
            creds, project = google.auth.default()
            creds.refresh(google.auth.transport.requests.Request())
            token = getattr(creds, 'token', None)
            email, pic = self._userinfo(token)
            self.result.emit(email, pic or '', '')
        except Exception as e:
            self.result.emit('', '', str(e))

    def _userinfo(self, token):
        if not token:
            return 'Google account', None
        try:
            import urllib.request, json as _j
            req = urllib.request.Request(
                'https://www.googleapis.com/oauth2/v2/userinfo',
                headers={'Authorization': f'Bearer {token}'})
            with urllib.request.urlopen(req, timeout=5) as r:
                info = _j.loads(r.read())
            return info.get('email', 'Google account'), info.get('picture')
        except Exception:
            return 'Google account', None


# ---------------------------------------------------------------------------
# Avatar downloader — fetches Google profile picture in background
# ---------------------------------------------------------------------------

class _AvatarDownloader(QObject):
    done = Signal(bytes)   # raw image bytes (empty on failure)

    def __init__(self, url: str):
        super().__init__()
        self.url = url

    def run(self):
        try:
            import urllib.request
            with urllib.request.urlopen(self.url, timeout=5) as r:
                self.done.emit(bytes(r.read()))
        except Exception:
            self.done.emit(bytes())


# ---------------------------------------------------------------------------
# Connection check worker — sends a minimal 1-token request
# ---------------------------------------------------------------------------

class _ConnCheckWorker(QObject):
    result = Signal(bool, str)   # (ok, message)

    def __init__(self, backend, model, api_key, endpoint, gcp_project=''):
        super().__init__()
        self.backend     = backend
        self.model       = model
        self.api_key     = api_key
        self.endpoint    = endpoint
        self.gcp_project = gcp_project

    def run(self):
        try:
            reply = self._ping()
            self.result.emit(True, reply)
        except Exception as e:
            self.result.emit(False, str(e)[:120])

    def _ping(self) -> str:
        b = self.backend
        if b == "Anthropic":
            if self.api_key:
                import anthropic
                c = anthropic.Anthropic(api_key=self.api_key)
                r = c.messages.create(
                    model=self.model, max_tokens=1,
                    messages=[{"role": "user", "content": "hi"}],
                )
                return f"{self.model} — {r.stop_reason}"
            else:
                from anthropic import AnthropicVertex
                import google.auth, google.auth.transport.requests
                creds, project = google.auth.default()
                # Refresh to ensure we have a valid token
                try:
                    creds.refresh(google.auth.transport.requests.Request())
                except Exception:
                    pass
                project = self.gcp_project or project
                if not project:
                    raise RuntimeError(
                        'No GCP Project ID found.\n'
                        'Enter it in the "GCP Project ID" field\n'
                        'or run: gcloud config set project YOUR_PROJECT_ID')
                c = AnthropicVertex(region="us-east5", project_id=project)
                r = c.messages.create(
                    model=self.model, max_tokens=1,
                    messages=[{"role": "user", "content": "hi"}],
                )
                return f"{self.model} via Vertex [{project}] — {r.stop_reason}"
        elif b == "Gemini":
            from google import genai
            from google.genai import types
            if self.api_key:
                client = genai.Client(api_key=self.api_key)
            else:
                import google.auth
                creds, _ = google.auth.default(
                    scopes=['https://www.googleapis.com/auth/generative-language'])
                client = genai.Client(credentials=creds)
            r = client.models.generate_content(
                model=self.model,
                contents='hi',
                config=types.GenerateContentConfig(max_output_tokens=1),
            )
            return f"{self.model} — OK"
        elif b == "Ollama":
            import requests
            ep = self.endpoint.rstrip("/")
            r  = requests.get(f"{ep}/api/tags", timeout=5)
            r.raise_for_status()
            models = [m["name"] for m in r.json().get("models", [])]
            return f"Ollama OK — {len(models)} model(s) available"
        else:  # OpenAI-compatible
            from openai import OpenAI
            c = OpenAI(api_key=self.api_key or "local",
                       base_url=self.endpoint)
            models = [m.id for m in c.models.list().data[:3]]
            return f"OK — {', '.join(models)}"


# ---------------------------------------------------------------------------
# RAG lazy loader — imports chromadb / sentence-transformers in background
# ---------------------------------------------------------------------------

class _RagLoader(QObject):
    finished = Signal(bool, str)   # (success, error_message)

    def run(self):
        print('[TSCG] [BG] Loading RAG modules...', flush=True)
        try:
            global RAG_AVAILABLE, TscgRagAugmentor, RagAugmentorWidget
            from tscg_rag_augmentor import (
                TscgRagAugmentor   as _TA,
                RagAugmentorWidget as _RW,
            )
            TscgRagAugmentor   = _TA
            RagAugmentorWidget = _RW
            RAG_AVAILABLE = True
            print('[TSCG] [BG] RAG modules loaded OK', flush=True)
            self.finished.emit(True, '')
        except Exception as e:
            print(f'[TSCG] [BG] RAG not available: {e}', flush=True)
            self.finished.emit(False, str(e))


# ---------------------------------------------------------------------------
# gcloud login worker — QThread, launches browser OAuth flow
# ---------------------------------------------------------------------------

class _GcloudLoginWorker(QObject):
    success = Signal()
    failure = Signal(str)

    def run(self):
        import subprocess, shutil, os
        gcloud = shutil.which('gcloud') or shutil.which('gcloud.cmd')
        if not gcloud:
            candidates = [
                os.path.join(os.environ.get('LOCALAPPDATA', ''),
                    'Google', 'Cloud SDK', 'google-cloud-sdk', 'bin', 'gcloud.cmd'),
                r'C:\Program Files (x86)\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd',
                r'C:\Program Files\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd',
            ]
            for c in candidates:
                if os.path.exists(c):
                    gcloud = c
                    break
        if not gcloud:
            self.failure.emit(
                'gcloud not found in PATH.\n'
                'Install Google Cloud SDK: https://cloud.google.com/sdk/docs/install')
            return
        try:
            result = subprocess.run(
                [gcloud, 'auth', 'application-default', 'login'],
                timeout=300,
            )
            if result.returncode == 0:
                self.success.emit()
            else:
                self.failure.emit(f'gcloud exited with code {result.returncode}')
        except subprocess.TimeoutExpired:
            self.failure.emit('Login timed out (5 min)')
        except Exception as e:
            self.failure.emit(str(e))


# ---------------------------------------------------------------------------
# History item
# ---------------------------------------------------------------------------

class HistoryItem:
    def __init__(self, timestamp, request, backend, model,
                 jsonld="", readme="", sim=""):
        self.timestamp = timestamp
        self.request   = request
        self.backend   = backend
        self.model     = model
        self.jsonld    = jsonld
        self.readme    = readme
        self.sim       = sim

    def label(self):
        short = self.request[:50] + ("…" if len(self.request) > 50 else "")
        return f"[{self.timestamp}]  {self.backend}/{self.model}  {short}"


# ---------------------------------------------------------------------------
# Main Window
# ---------------------------------------------------------------------------

class PocletGeneratorWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        print(f"[TSCG] {APP_NAME} v{APP_VERSION} — starting up…")
        self.setWindowTitle(f"{APP_NAME}  v{APP_VERSION}")
        # Adapt to screen — 80 % of available geometry, capped at 1340×880
        screen = QApplication.primaryScreen().availableGeometry()
        w = min(int(screen.width()  * 0.82), 1340)
        h = min(int(screen.height() * 0.85), 880)
        self.resize(w, h)
        # Centre on screen
        self.move(screen.center() - self.rect().center())

        self._history: list[HistoryItem] = []
        self._rag_augmented_prompt: Optional[str] = None
        self._worker: Optional[LlmWorker]  = None
        self._worker_thread: Optional[QThread] = None
        self._smart_prompt_path: Optional[str] = None
        self._smart_prompt_cache: str = ""
        self._google_badge: Optional[QLabel] = None   # created in _build_ui

        self.rag_augmentor = None   # populated by _RagLoader after window shown

        print("[TSCG] Building UI…")
        self._build_ui()
        print("[TSCG] Loading settings…")
        self._load_settings()
        self._update_backend_ui()
        print("[TSCG] Ready.")

    # ------------------------------------------------------------------ UI --

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(6, 6, 6, 2)
        root.setSpacing(4)

        main_split = _Splitter(Qt.Horizontal)
        main_split.setHandleWidth(8)
        main_split.setChildrenCollapsible(False)
        root.addWidget(main_split, stretch=1)
        main_split.addWidget(self._left_panel())
        main_split.addWidget(self._right_panel())
        main_split.setSizes([280, 820])

        self._progress = QProgressBar()
        self._progress.setRange(0, 0)
        self._progress.setVisible(False)
        self._progress.setMaximumHeight(14)
        root.addWidget(self._progress)

        self._statusbar = QStatusBar()
        self.setStatusBar(self._statusbar)
        self._statusbar.showMessage("Ready")

        # Google account badge — composite widget: avatar + email
        self._google_badge = QWidget()          # container (kept for guard checks)
        _blay = QHBoxLayout(self._google_badge)
        _blay.setContentsMargins(4, 0, 8, 0)
        _blay.setSpacing(5)
        self._avatar_lbl = QLabel()
        self._avatar_lbl.setFixedSize(20, 20)
        self._avatar_lbl.setScaledContents(True)
        self._avatar_lbl.hide()
        _blay.addWidget(self._avatar_lbl)
        self._email_lbl = QLabel('⬜ Not connected')
        self._email_lbl.setStyleSheet('color:#888; font-size:9pt;')
        self._email_lbl.setToolTip(
            'Google account\n'
            'Used by Anthropic (Vertex AI) and Gemini (ADC) auth modes'
        )
        _blay.addWidget(self._email_lbl)
        self._statusbar.addPermanentWidget(self._google_badge)

    # ── Left panel ────────────────────────────────────────────────────

    def _left_panel(self) -> QWidget:
        w = QWidget()
        w.setMinimumWidth(220)
        w.setMaximumWidth(360)
        lay = QVBoxLayout(w)
        lay.setContentsMargins(4, 4, 4, 4)
        lay.setSpacing(8)

        # Backend
        box = QGroupBox("🔌 Backend")
        g = QVBoxLayout(box)

        self._combo_backend = QComboBox()
        self._combo_backend.addItems(list(BACKENDS.keys()))
        self._combo_backend.currentTextChanged.connect(self._update_backend_ui)
        g.addWidget(self._combo_backend)

        row = QHBoxLayout()
        row.addWidget(QLabel("Model:"))
        self._combo_model = QComboBox()
        self._combo_model.setEditable(True)
        row.addWidget(self._combo_model, stretch=1)
        g.addLayout(row)

        # Auth mode selector (visible only when backend offers multiple modes)
        self._lbl_auth = QLabel("Auth:")
        g.addWidget(self._lbl_auth)
        self._combo_auth = QComboBox()
        self._combo_auth.currentTextChanged.connect(self._on_auth_mode_changed)
        g.addWidget(self._combo_auth)
        self._lbl_auth.setVisible(False)
        self._combo_auth.setVisible(False)

        self._lbl_key  = QLabel("API Key:")
        g.addWidget(self._lbl_key)
        self._edit_key = QLineEdit()
        self._edit_key.setEchoMode(QLineEdit.Password)
        self._edit_key.setPlaceholderText("sk-ant-…")
        g.addWidget(self._edit_key)

        self._lbl_ep  = QLabel("Endpoint URL:")
        g.addWidget(self._lbl_ep)
        self._edit_ep = QLineEdit()
        self._edit_ep.setPlaceholderText("http://localhost:11434")
        g.addWidget(self._edit_ep)

        # GCP Project ID (Vertex AI only — hidden by default)
        self._lbl_project = QLabel("GCP Project ID:")
        g.addWidget(self._lbl_project)
        self._edit_project = QLineEdit()
        self._edit_project.setPlaceholderText("my-project-123456  (Vertex AI only)")
        self._edit_project.setToolTip(
            "Google Cloud Project ID — required for Anthropic via Vertex AI.\n"
            "Leave empty to use gcloud default project.\n"
            "Run: gcloud config set project YOUR_PROJECT_ID"
        )
        g.addWidget(self._edit_project)
        self._lbl_project.setVisible(False)
        self._edit_project.setVisible(False)

        # Check connection
        self._btn_check = QPushButton("🔍 Check connection")
        self._btn_check.setToolTip("Send a minimal ping to the selected backend")
        self._btn_check.clicked.connect(self._check_connection)
        g.addWidget(self._btn_check)

        self._lbl_conn = QLabel("")
        self._lbl_conn.setWordWrap(True)
        self._lbl_conn.setStyleSheet("font-size:9pt; padding:2px 0;")
        g.addWidget(self._lbl_conn)

        lay.addWidget(box)

        # Smart Prompt
        box2 = QGroupBox("📋 Smart Prompt")
        g2 = QHBoxLayout(box2)
        self._lbl_sp = QLabel("Not loaded")
        self._lbl_sp.setStyleSheet("color:#888; font-size:9pt;")
        self._lbl_sp.setWordWrap(True)
        g2.addWidget(self._lbl_sp, stretch=1)
        btn = QPushButton("📂")
        btn.setFixedWidth(30)
        btn.setToolTip("Load Smart Prompt (.md)")
        btn.clicked.connect(self._load_smart_prompt)
        g2.addWidget(btn)
        lay.addWidget(box2)

        # Templates
        box3 = QGroupBox("📄 Templates")
        g3 = QGridLayout(box3)
        g3.addWidget(QLabel("README:"), 0, 0)
        self._combo_readme_tmpl = QComboBox()
        self._combo_readme_tmpl.addItems(list(README_TEMPLATES.keys()))
        g3.addWidget(self._combo_readme_tmpl, 0, 1)
        g3.addWidget(QLabel("sim.py UI:"), 1, 0)
        self._combo_sim_tmpl = QComboBox()
        self._combo_sim_tmpl.addItems(list(SIM_TEMPLATES.keys()))
        g3.addWidget(self._combo_sim_tmpl, 1, 1)
        lay.addWidget(box3)

        # History
        box4 = QGroupBox("📜 History")
        g4 = QVBoxLayout(box4)
        self._list_history = QListWidget()
        self._list_history.setMinimumHeight(120)
        self._list_history.itemClicked.connect(self._on_history_clicked)
        g4.addWidget(self._list_history)
        btn_clr = QPushButton("🗑 Clear")
        btn_clr.setStyleSheet("font-size:9pt; padding:2px;")
        btn_clr.clicked.connect(lambda: (self._history.clear(), self._list_history.clear()))
        g4.addWidget(btn_clr)
        lay.addWidget(box4)

        lay.addStretch()
        return w

    # ── Right panel ───────────────────────────────────────────────────

    def _right_panel(self) -> QSplitter:
        """
        Returns self._vs (QSplitter vertical) directly — no wrapper widget.
        3 panes: Request (30%) | RAG Augmentor (20%) | Output tabs (50%)
        """
        self._vs = _Splitter(Qt.Vertical)
        self._vs.setObjectName("vSplit")
        self._vs.setChildrenCollapsible(False)
        self._vs.setHandleWidth(8)
        self._vs.setOpaqueResize(True)
        # No stylesheet — custom border/background CSS blocks mouse events on Windows
        # Handle width alone is sufficient for reliable drag behaviour

        # ── pane 0 : Poclet Request ───────────────────────────────────
        box_req = QGroupBox("✏️ Poclet Request")
        bg = QVBoxLayout(box_req)
        bg.setContentsMargins(4, 4, 4, 4)

        self._edit_request = QPlainTextEdit()
        self._edit_request.setPlaceholderText(
            "Describe the system to model as a TSCG poclet…\n"
            "e.g.  'Model the human heart as a poclet'\n"
            "      'Create a poclet for the Krebs cycle'"
        )
        self._edit_request.setFont(QFont("Segoe UI", 10))
        bg.addWidget(self._edit_request, stretch=1)

        btn_row = QHBoxLayout()

        # Combo-button: main action + dropdown to switch mode
        from PySide6.QtWidgets import QMenu
        from PySide6.QtGui import QAction
        _BTN_STYLE = (
            "QPushButton{background:#4a7ebf;color:white;font-weight:bold;"
            "font-size:11pt;padding:6px 14px;border-radius:5px 0 0 5px;}"
            "QPushButton:hover{background:#3a6eaf;}"
            "QPushButton:disabled{background:#555;}"
        )
        _DROP_STYLE = (
            "QPushButton{background:#3a6eaf;color:white;font-weight:bold;"
            "font-size:11pt;padding:6px 6px;border-radius:0 5px 5px 0;"
            "border-left:1px solid #2a5e9f;}"
            "QPushButton:hover{background:#2a5e9f;}"
            "QPushButton:disabled{background:#555;}"
        )
        self._gen_modes = ["❓ Question mode", "⚡ Generate Poclet"]
        self._gen_mode  = self._gen_modes[0]   # default: Question mode

        self._btn_gen = QPushButton(self._gen_mode)
        self._btn_gen.setStyleSheet(_BTN_STYLE)
        self._btn_gen.clicked.connect(self._on_generate)

        self._btn_gen_drop = QPushButton("▾")
        self._btn_gen_drop.setFixedWidth(24)
        self._btn_gen_drop.setStyleSheet(_DROP_STYLE)
        self._btn_gen_drop.setToolTip("Switch generation mode")

        def _show_gen_menu():
            menu = QMenu(self)
            for m in self._gen_modes:
                act = QAction(m, self)
                act.setCheckable(True)
                act.setChecked(m == self._gen_mode)
                def _pick(checked, mode=m):
                    self._gen_mode = mode
                    self._btn_gen.setText(mode)
                act.triggered.connect(_pick)
                menu.addAction(act)
            menu.exec(self._btn_gen_drop.mapToGlobal(
                self._btn_gen_drop.rect().bottomLeft()))

        self._btn_gen_drop.clicked.connect(_show_gen_menu)

        gen_combo = QWidget()
        gen_combo_lay = QHBoxLayout(gen_combo)
        gen_combo_lay.setContentsMargins(0, 0, 0, 0)
        gen_combo_lay.setSpacing(0)
        gen_combo_lay.addWidget(self._btn_gen)
        gen_combo_lay.addWidget(self._btn_gen_drop)
        btn_row.addWidget(gen_combo)

        btn_load = QPushButton("📂 Load Poclet")
        btn_load.setStyleSheet(
            "QPushButton{background:#5a5a5a;color:white;font-size:10pt;"
            "padding:6px 12px;border-radius:5px;}"
            "QPushButton:hover{background:#4a4a4a;}"
        )
        btn_load.clicked.connect(self._load_poclet)
        btn_row.addWidget(btn_load)

        self._btn_stop = QPushButton("⛔ Stop")
        self._btn_stop.setEnabled(False)
        self._btn_stop.setStyleSheet(
            "QPushButton{background:#8a2020;color:white;font-size:10pt;"
            "padding:6px 12px;border-radius:5px;}"
            "QPushButton:disabled{background:#555;}"
        )
        self._btn_stop.clicked.connect(self._on_stop)
        btn_row.addWidget(self._btn_stop)
        btn_row.addStretch()
        bg.addLayout(btn_row)
        self._vs.addWidget(box_req)

        # ── pane 1 : RAG Augmentor ────────────────────────────────────
        if RAG_AVAILABLE and self.rag_augmentor:
            self._rag_widget = RagAugmentorWidget(
                parent         = self._vs,
                augmentor      = self.rag_augmentor,
                on_augment_cb  = self._on_rag_augmented,
                get_request_cb = self._get_current_request,
            )
            pane1 = self._rag_widget.group_box
        else:
            pane1 = QGroupBox("🔍 RAG Augmentor")
            lbl = QLabel(
                "ℹ RAG Augmentor unavailable\n"
                "pip install chromadb sentence-transformers"
            )
            lbl.setStyleSheet("color:#888; font-size:9pt; padding:4px;")
            QVBoxLayout(pane1).addWidget(lbl)
        self._vs.addWidget(pane1)

        # ── pane 2 : Output tabs ──────────────────────────────────────
        self._vs.addWidget(self._output_panel())

        # Clear minimum sizes so every pane can shrink freely when dragging
        for i in range(self._vs.count()):
            self._vs.widget(i).setMinimumSize(0, 0)

        return self._vs
    def _output_panel(self) -> QWidget:
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(4)

        self._tabs = QTabWidget()
        self._tabs.setDocumentMode(True)

        dark_edit = "QPlainTextEdit{background:#1e1e1e;color:#d4d4d4;border:none;}"
        mono = QFont("Courier New", 10)

        self._edit_jsonld = QPlainTextEdit()
        self._edit_jsonld.setFont(mono)
        self._edit_jsonld.setStyleSheet(dark_edit)
        self._hl_jsonld = JsonLdHighlighter(self._edit_jsonld.document())
        self._tabs.addTab(self._edit_jsonld, "📐 M0_xxx.jsonld")

        self._edit_readme = QPlainTextEdit()
        self._edit_readme.setFont(mono)
        self._edit_readme.setStyleSheet(dark_edit)
        self._tabs.addTab(self._edit_readme, "📖 README.md")

        self._edit_sim = QPlainTextEdit()
        self._edit_sim.setFont(mono)
        self._edit_sim.setStyleSheet(dark_edit)
        self._hl_sim = PythonHighlighter(self._edit_sim.document())
        self._tabs.addTab(self._edit_sim, "🐍 sim.py")

        lay.addWidget(self._tabs, stretch=1)

        save_row = QHBoxLayout()
        for label, slot in [
            ("💾 Save All Files…", self._save_all),
            ("💾 Save Current Tab…", self._save_current_tab),
        ]:
            btn = QPushButton(label)
            btn.setStyleSheet(
                "QPushButton{background:#3a5a3a;color:white;padding:4px 12px;"
                "border-radius:4px;font-size:9pt;}"
                "QPushButton:hover{background:#2a4a2a;}"
            )
            btn.clicked.connect(slot)
            save_row.addWidget(btn)
        save_row.addStretch()
        lay.addLayout(save_row)
        return w

    # ---------------------------------------------------------------- Backend

    def _check_connection(self):
        """Send a minimal 1-token request to verify credentials & reachability."""
        b   = self._combo_backend.currentText()
        mdl = self._combo_model.currentText()
        auth_mode = self._combo_auth.currentText()
        is_google  = auth_mode in ("Google Auth (ADC)", "Google Auth (Vertex AI)")
        key = "" if is_google else self._edit_key.text().strip()
        ep  = self._edit_ep.text().strip()
        self._lbl_conn.setText("⏳ Checking...")
        self._lbl_conn.setStyleSheet("color:#ff9800; font-size:9pt;")
        self._btn_check.setEnabled(False)
        self._check_thread = QThread()
        self._check_worker = _ConnCheckWorker(b, mdl, key, ep,
                                              gcp_project=self._edit_project.text().strip())
        self._check_worker.moveToThread(self._check_thread)
        self._check_thread.started.connect(self._check_worker.run)
        self._check_worker.result.connect(self._on_check_result)
        self._check_worker.result.connect(self._check_thread.quit)
        self._check_thread.start()

    def _on_check_result(self, ok: bool, msg: str):
        self._btn_check.setEnabled(True)
        if ok:
            self._lbl_conn.setText(f"🟢 {msg}")
            self._lbl_conn.setStyleSheet(
                "color:#4caf50; font-size:9pt; font-weight:bold;")
            self._statusbar.showMessage(f"Connection OK — {msg}", 5000)
        else:
            self._lbl_conn.setText(f"🔴 {msg}")
            self._lbl_conn.setStyleSheet("color:#f44336; font-size:9pt;")
            self._statusbar.showMessage(f"Connection failed: {msg}", 6000)

    def _update_backend_ui(self):
        b   = self._combo_backend.currentText()
        cfg = BACKENDS.get(b, {})
        self._combo_model.clear()
        self._combo_model.addItems(cfg.get("models", []))

        # Auth mode combo
        modes = cfg.get("auth_modes", [])
        self._combo_auth.blockSignals(True)
        self._combo_auth.clear()
        self._combo_auth.addItems(modes)
        self._combo_auth.blockSignals(False)
        has_modes = len(modes) > 1
        self._lbl_auth.setVisible(has_modes)
        self._combo_auth.setVisible(has_modes)

        # Endpoint
        ne = cfg.get("needs_endpoint", False)
        self._lbl_ep.setVisible(ne)
        self._edit_ep.setVisible(ne)
        if ne and not self._edit_ep.text():
            self._edit_ep.setText(cfg.get("default_endpoint", ""))

        # Placeholder + key visibility
        ph = cfg.get("key_placeholder", "")
        if ph:
            self._edit_key.setPlaceholderText(ph)
        self._on_auth_mode_changed(self._combo_auth.currentText())

    def _on_auth_mode_changed(self, mode: str):
        b   = self._combo_backend.currentText()
        cfg = BACKENDS.get(b, {})
        nk  = cfg.get('needs_key', True)
        is_google = mode in ('Google Auth (ADC)', 'Google Auth (Vertex AI)')
        self._lbl_key.setVisible(nk and not is_google)
        self._edit_key.setVisible(nk and not is_google)
        if self._google_badge is None:
            return
        if is_google:
            self._probe_google_identity()
        else:
            self._email_lbl.setText('□ Not connected')
            self._email_lbl.setStyleSheet('color:#888; font-size:9pt;')
            self._avatar_lbl.hide()

    def _probe_google_identity(self):
        if self._google_badge is None:
            return
        # Show 'pending' badge immediately — probe runs in background
        self._email_lbl.setText('🟠 Google Auth connection pending…')
        self._email_lbl.setStyleSheet(
            'color:#ff9800; font-size:9pt; font-weight:bold;')
        self._avatar_lbl.hide()
        self._statusbar.showMessage('Google Auth: connecting…')
        # Run blocking auth in background thread
        self._probe_thread = QThread()
        self._probe_worker = _GoogleProbeWorker()
        self._probe_worker.moveToThread(self._probe_thread)
        self._probe_thread.started.connect(self._probe_worker.run)
        self._probe_worker.result.connect(self._on_probe_result)
        self._probe_worker.result.connect(self._probe_thread.quit)
        self._probe_thread.start()

    def _on_probe_result(self, email: str, pic: str, err: str):
        if err:
            # No valid credentials — offer gcloud login
            self._offer_gcloud_login()
        else:
            self._set_google_badge_ok(email, pic or None)

    def _set_google_badge_ok(self, email: str, picture_url: str = None):
        self._email_lbl.setText(email)
        self._email_lbl.setStyleSheet(
            'color:#4caf50; font-size:9pt; font-weight:bold;')
        self._email_lbl.setToolTip(f'Connected as: {email}')
        # Fetch and display round avatar
        if picture_url:
            self._load_avatar(picture_url)
        else:
            self._set_default_avatar()
        self._statusbar.showMessage(f'Google Auth OK — {email}', 4000)

    def _load_avatar(self, url: str):
        """Download avatar in background QThread then update UI."""
        self._avatar_dl_thread = QThread()
        self._avatar_dl_worker = _AvatarDownloader(url)
        self._avatar_dl_worker.moveToThread(self._avatar_dl_thread)
        self._avatar_dl_thread.started.connect(self._avatar_dl_worker.run)
        self._avatar_dl_worker.done.connect(self._on_avatar_data)
        self._avatar_dl_worker.done.connect(self._avatar_dl_thread.quit)
        self._avatar_dl_thread.start()

    def _on_avatar_data(self, data: bytes):
        if data:
            px = QPixmap()
            if px.loadFromData(data) and not px.isNull():
                self._set_round_avatar(px)
                return
        self._set_default_avatar()

    def _set_round_avatar(self, px: QPixmap):
        """Crop pixmap to circle and show it."""
        size = 20
        px   = px.scaled(size, size)
        # Create circular mask
        mask = QBitmap(size, size)
        mask.clear()
        p = QPainter(mask)
        p.setBrush(Qt.white)
        p.setPen(Qt.NoPen)
        p.drawEllipse(0, 0, size, size)
        p.end()
        px.setMask(mask)
        self._avatar_lbl.setPixmap(px)
        self._avatar_lbl.show()

    def _set_default_avatar(self):
        """Show a simple coloured circle when no picture is available."""
        size = 20
        px   = QPixmap(size, size)
        px.fill(Qt.transparent)
        p = QPainter(px)
        p.setRenderHint(QPainter.Antialiasing)
        p.setBrush(QColor('#4caf50'))
        p.setPen(Qt.NoPen)
        p.drawEllipse(0, 0, size, size)
        p.end()
        self._avatar_lbl.setPixmap(px)
        self._avatar_lbl.show()

    def _offer_gcloud_login(self):
        reply = QMessageBox.question(
            self, 'Google Authentication',
            'No Google credentials found.\n\n'
            'Click OK to open your browser for Google account login.\n'
            '(runs: gcloud auth application-default login)\n\n'
            'Requirement: Google Cloud SDK must be installed.\n'
            'https://cloud.google.com/sdk/docs/install',
            QMessageBox.Ok | QMessageBox.Cancel,
        )
        if reply != QMessageBox.Ok:
            self._email_lbl.setText('□ Not connected')
            self._email_lbl.setStyleSheet('color:#888; font-size:9pt;')
            self._avatar_lbl.hide()
            return

        # ── Boîte de progression pendant l'auth ──────────────────────
        self._auth_dlg = QDialog(self)
        self._auth_dlg.setWindowTitle('Google Authentication')
        self._auth_dlg.setWindowFlags(
            self._auth_dlg.windowFlags() & ~Qt.WindowCloseButtonHint)
        self._auth_dlg.setMinimumWidth(420)
        _dlg_lay = QVBoxLayout(self._auth_dlg)
        _dlg_lay.setSpacing(12)
        _dlg_lay.setContentsMargins(20, 20, 20, 20)

        _ico = QLabel('🔑')
        _ico.setStyleSheet('font-size:28pt;')
        _ico.setAlignment(Qt.AlignCenter)
        _dlg_lay.addWidget(_ico)

        _title = QLabel('<b>Waiting for Google login…</b>')
        _title.setAlignment(Qt.AlignCenter)
        _title.setStyleSheet('font-size:11pt;')
        _dlg_lay.addWidget(_title)

        _msg = QLabel(
            'Your browser should open automatically.\n'
            'Log in with your Google account, then\n'
            'return here — this dialog will close automatically.')
        _msg.setAlignment(Qt.AlignCenter)
        _msg.setStyleSheet('color:#aaa; font-size:9pt;')
        _msg.setWordWrap(True)
        _dlg_lay.addWidget(_msg)

        _bar = QProgressBar()
        _bar.setRange(0, 0)   # indeterminate / marquee
        _bar.setTextVisible(False)
        _bar.setMaximumHeight(8)
        _dlg_lay.addWidget(_bar)

        _cancel_btn = QDialogButtonBox(QDialogButtonBox.Cancel)
        _cancel_btn.rejected.connect(self._cancel_gcloud_login)
        _dlg_lay.addWidget(_cancel_btn)

        self._email_lbl.setText('⏳ Waiting for browser login…')
        self._email_lbl.setStyleSheet('color:#ff9800; font-size:9pt;')
        self._statusbar.showMessage('Opening browser for Google login…')

        self._gcloud_thread = QThread()
        self._gcloud_worker = _GcloudLoginWorker()
        self._gcloud_worker.moveToThread(self._gcloud_thread)
        self._gcloud_thread.started.connect(self._gcloud_worker.run)
        self._gcloud_worker.success.connect(self._on_gcloud_ok)
        self._gcloud_worker.failure.connect(self._on_gcloud_fail)
        self._gcloud_worker.success.connect(self._gcloud_thread.quit)
        self._gcloud_worker.failure.connect(self._gcloud_thread.quit)
        self._gcloud_thread.start()

        self._auth_dlg.exec()   # bloquant mais le QThread tourne en parallèle

    def _on_gcloud_ok(self):
        if hasattr(self, '_auth_dlg') and self._auth_dlg.isVisible():
            self._auth_dlg.accept()
        self._probe_google_identity()

    def _on_gcloud_fail(self, err: str):
        if hasattr(self, '_auth_dlg') and self._auth_dlg.isVisible():
            self._auth_dlg.reject()
        self._email_lbl.setText('🔴 Login failed')
        self._email_lbl.setStyleSheet('color:#f44336; font-size:9pt;')
        self._avatar_lbl.hide()
        self._statusbar.showMessage(f'gcloud error: {err}', 8000)
        QMessageBox.warning(self, 'Google Login Failed',
            f'Could not complete Google login:\n\n{err}\n\n'
            'Install Google Cloud SDK:\nhttps://cloud.google.com/sdk/docs/install')

    def _cancel_gcloud_login(self):
        if hasattr(self, '_gcloud_thread') and self._gcloud_thread.isRunning():
            self._gcloud_thread.terminate()
            self._gcloud_thread.wait(1000)
        if hasattr(self, '_auth_dlg'):
            self._auth_dlg.reject()
        self._email_lbl.setText('□ Not connected')
        self._email_lbl.setStyleSheet('color:#888; font-size:9pt;')
        self._avatar_lbl.hide()
        self._statusbar.showMessage('Google login cancelled.', 3000)
    # ---------------------------------------------------------- Smart Prompt

    def _load_smart_prompt(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Load Smart Prompt", "",
            "Markdown files (*.md);;All files (*)"
        )
        if not path:
            return
        try:
            self._smart_prompt_cache = Path(path).read_text(encoding="utf-8")
            self._smart_prompt_path  = path
            self._lbl_sp.setText(f"✓ {Path(path).name}")
            self._lbl_sp.setStyleSheet("color:#2d7a2d; font-size:9pt;")
            self._statusbar.showMessage(f"Smart Prompt loaded: {Path(path).name}", 3000)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Cannot load Smart Prompt:\n{e}")

    def _get_smart_prompt(self) -> str:
        if self._rag_augmented_prompt:
            p = self._rag_augmented_prompt
            self._rag_augmented_prompt = None
            return p
        if self._smart_prompt_cache:
            return self._smart_prompt_cache
        return (
            "You are a TSCG (Transdisciplinary System Construction Game) expert.\n"
            "Generate a complete poclet deliverable set:\n"
            "1. M0_SystemName.jsonld  — JSON-LD ontology\n"
            "2. README.md             — poclet documentation\n"
            "3. system_name_sim.py    — Pygame simulation\n\n"
            "TSCG v15.9.0 conventions:\n"
            "- dcterms:creator: 'Echopraxium with the collaboration of Claude AI'\n"
            "- @base: 'https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/'\n"
            "- Include ASFID (A,S,F,I,D) and REVOI (R,E,V,O,I) scores [0.0–1.0]\n"
            "- R = Representability (never Reproducibility)\n"
            "- Compute epistemic gap δ = ||ASFID_vec - REVOI_vec||\n"
            "- List mobilized M2 GenericConcepts with tensor formulas\n"
            "- Keep changelog to 3 most recent entries\n"
            "- Output each file in a fenced code block: ```jsonld, ```markdown, ```python\n"
        )

    # ------------------------------------------------------------- Generation

    def _on_generate(self):
        request = self._get_current_request()
        if not request:
            QMessageBox.warning(self, "No request", "Please enter a poclet request.")
            return

        b   = self._combo_backend.currentText()
        mdl = self._combo_model.currentText()
        auth_mode = self._combo_auth.currentText()
        is_google  = auth_mode in ("Google Auth (ADC)", "Google Auth (Vertex AI)")
        key        = "" if is_google else self._edit_key.text().strip()
        ep  = self._edit_ep.text().strip()

        if BACKENDS[b]["needs_key"] and not key and not is_google:
            QMessageBox.warning(self, "API Key missing",
                                f"Please enter an API key for {b}.")
            return

        if "Generate Poclet" in self._gen_mode:
            full_request = (
                f"{request}\n\n"
                f"[README template style: {self._combo_readme_tmpl.currentText()}]\n"
                f"[sim.py UI layout: {self._combo_sim_tmpl.currentText()}]\n"
            )
        else:
            # Question mode — free-form Q&A, no poclet output expected
            full_request = request

        self._set_busy(True)
        self._statusbar.showMessage(f"⏳ Generating with {b} / {mdl}…")

        self._worker = LlmWorker(
            backend       = b,
            model         = mdl,
            api_key       = key,
            endpoint      = ep,
            system_prompt = self._get_smart_prompt(),
            user_request  = full_request,
            auth_mode     = auth_mode,
            gcp_project   = self._edit_project.text().strip(),
        )
        self._worker_thread = QThread(self)
        self._worker.moveToThread(self._worker_thread)
        self._worker_thread.started.connect(self._worker.run)
        self._worker.finished.connect(self._on_done)
        self._worker.error.connect(self._on_error)
        self._worker.finished.connect(self._worker_thread.quit)
        self._worker.error.connect(self._worker_thread.quit)
        self._worker_thread.finished.connect(self._worker.deleteLater)
        self._worker_thread.start()

    def _on_stop(self):
        if self._worker_thread and self._worker_thread.isRunning():
            self._worker_thread.terminate()
            self._worker_thread.wait(2000)
        self._set_busy(False)
        self._statusbar.showMessage("Generation stopped.", 3000)

    def _on_done(self, text: str):
        self._set_busy(False)
        jsonld, readme, sim = self._parse_output(text)
        self._edit_jsonld.setPlainText(jsonld)
        self._edit_readme.setPlainText(readme)
        self._edit_sim.setPlainText(sim)
        self._statusbar.showMessage("✓ Generation complete", 5000)

        item = HistoryItem(
            timestamp = datetime.now().strftime("%H:%M:%S"),
            request   = self._get_current_request(),
            backend   = self._combo_backend.currentText(),
            model     = self._combo_model.currentText(),
            jsonld    = jsonld, readme = readme, sim = sim,
        )
        self._history.insert(0, item)
        self._list_history.insertItem(0, QListWidgetItem(item.label()))

    def _on_error(self, err: str):
        self._set_busy(False)
        self._statusbar.showMessage(f"✗ {err[:80]}", 6000)
        QMessageBox.critical(self, "Generation Error", err)

    def _parse_output(self, text: str) -> tuple[str, str, str]:
        """Extract JSON-LD, README and sim.py from fenced code blocks."""
        jsonld = readme = sim = ""

        m = re.search(r'```(?:json|jsonld)\s*\n(.*?)```', text, re.DOTALL | re.IGNORECASE)
        if m:
            jsonld = m.group(1).strip()
        else:
            m2 = re.search(r'(\{[\s\S]*?"@context"[\s\S]*?\})\s*$', text, re.MULTILINE)
            if m2:
                jsonld = m2.group(1).strip()

        m = re.search(r'```(?:markdown|md)\s*\n(.*?)```', text, re.DOTALL | re.IGNORECASE)
        if m:
            readme = m.group(1).strip()
        else:
            m2 = re.search(r'(^# .+?)(?=```|\Z)', text, re.DOTALL | re.MULTILINE)
            if m2:
                readme = m2.group(1).strip()

        m = re.search(r'```(?:python|py)\s*\n(.*?)```', text, re.DOTALL | re.IGNORECASE)
        if m:
            sim = m.group(1).strip()

        if not any([jsonld, readme, sim]):
            jsonld = text  # raw fallback

        return jsonld, readme, sim

    def _set_busy(self, busy: bool):
        self._btn_gen.setEnabled(not busy)
        self._btn_stop.setEnabled(busy)
        self._progress.setVisible(busy)

    # ------------------------------------------------------------------- RAG

    def _get_current_request(self) -> str:
        return self._edit_request.toPlainText().strip()

    def _on_rag_augmented(self, augmented_prompt: str):
        self._rag_augmented_prompt = augmented_prompt
        self._statusbar.showMessage(
            "✓ RAG context loaded — next generation will use it", 5000
        )

    # -------------------------------------------------------- Load / Save

    def _load_poclet(self):
        default_dir = str(_REPO_ROOT / "instances" / "poclets")
        if not Path(default_dir).exists():
            default_dir = str(_REPO_ROOT)
        path, _ = QFileDialog.getOpenFileName(
            self, "Load Poclet", default_dir,
            "JSON-LD files (*.jsonld);;All files (*)"
        )
        if not path:
            return
        try:
            self._edit_jsonld.setPlainText(Path(path).read_text(encoding="utf-8"))
            self._tabs.setCurrentIndex(0)
            self._statusbar.showMessage(f"Loaded: {Path(path).name}", 3000)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Cannot load file:\n{e}")

    def _save_all(self):
        folder = QFileDialog.getExistingDirectory(self, "Select output folder")
        if not folder:
            return
        folder = Path(folder)
        jsonld = self._edit_jsonld.toPlainText()
        readme = self._edit_readme.toPlainText()
        sim    = self._edit_sim.toPlainText()

        # Infer system name from label in JSON-LD
        name = "M0_PocletName"
        m = re.search(r'"rdfs:label"\s*:\s*"([^"]+)"', jsonld)
        if m:
            slug = re.sub(r'[^a-zA-Z0-9_]', '_', m.group(1).split()[0])
            name = f"M0_{slug}"
        sim_name = name[3:].lower()

        saved = []
        if jsonld:
            (folder / f"{name}.jsonld").write_text(jsonld, encoding="utf-8")
            saved.append(f"{name}.jsonld")
        if readme:
            (folder / f"{name}_README.md").write_text(readme, encoding="utf-8")
            saved.append(f"{name}_README.md")
        if sim:
            (folder / f"{sim_name}_sim.py").write_text(sim, encoding="utf-8")
            saved.append(f"{sim_name}_sim.py")

        if saved:
            self._statusbar.showMessage(
                f"✓ Saved {len(saved)} file(s) → {folder}", 5000
            )
        else:
            QMessageBox.information(self, "Nothing to save", "Output tabs are empty.")

    def _save_current_tab(self):
        idx  = self._tabs.currentIndex()
        eds  = [self._edit_jsonld, self._edit_readme, self._edit_sim]
        exts = [".jsonld", ".md", ".py"]
        txt  = eds[idx].toPlainText()
        if not txt.strip():
            QMessageBox.information(self, "Empty", "Current tab has no content.")
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Save file", "",
            f"Files (*{exts[idx]});;All files (*)"
        )
        if path:
            Path(path).write_text(txt, encoding="utf-8")
            self._statusbar.showMessage(f"✓ Saved: {Path(path).name}", 3000)

    # --------------------------------------------------------------- History

    def _on_history_clicked(self, item: QListWidgetItem):
        row = self._list_history.row(item)
        if 0 <= row < len(self._history):
            h = self._history[row]
            self._edit_request.setPlainText(h.request)
            self._edit_jsonld.setPlainText(h.jsonld)
            self._edit_readme.setPlainText(h.readme)
            self._edit_sim.setPlainText(h.sim)

    # ------------------------------------------------------------ Settings

    def _load_settings(self):
        s = QSettings("Echopraxium", "TscgPocletGenerator")
        backend = s.value("backend", "Anthropic")
        idx = self._combo_backend.findText(backend)
        if idx >= 0:
            self._combo_backend.setCurrentIndex(idx)
            self._update_backend_ui()
        model = s.value("model", "")
        if model:
            midx = self._combo_model.findText(model)
            if midx >= 0:
                self._combo_model.setCurrentIndex(midx)
            else:
                self._combo_model.setCurrentText(model)
        ep = s.value("endpoint", "")
        if ep:
            self._edit_ep.setText(ep)
        gcp = s.value("gcp_project", "")
        if gcp:
            self._edit_project.setText(gcp)
        sp = s.value("smart_prompt_path", "")
        if sp and Path(sp).exists():
            try:
                self._smart_prompt_cache = Path(sp).read_text(encoding="utf-8")
                self._smart_prompt_path  = sp
                self._lbl_sp.setText(f"✓ {Path(sp).name}")
                self._lbl_sp.setStyleSheet("color:#2d7a2d; font-size:9pt;")
            except Exception:
                pass

    def _save_settings(self):
        s = QSettings("Echopraxium", "TscgPocletGenerator")
        s.setValue("backend",     self._combo_backend.currentText())
        s.setValue("model",       self._combo_model.currentText())
        s.setValue("endpoint",    self._edit_ep.text())
        s.setValue("gcp_project", self._edit_project.text())
        if self._smart_prompt_path:
            s.setValue("smart_prompt_path", self._smart_prompt_path)

    def closeEvent(self, event):
        self._save_settings()
        super().closeEvent(event)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def _dark_palette() -> QPalette:
    p = QPalette()
    p.setColor(QPalette.Window,         QColor( 45,  45,  45))
    p.setColor(QPalette.WindowText,     QColor(220, 220, 220))
    p.setColor(QPalette.Base,           QColor( 30,  30,  30))
    p.setColor(QPalette.AlternateBase,  QColor( 53,  53,  53))
    p.setColor(QPalette.Text,           QColor(220, 220, 220))
    p.setColor(QPalette.Button,         QColor( 60,  60,  60))
    p.setColor(QPalette.ButtonText,     QColor(220, 220, 220))
    p.setColor(QPalette.Link,           QColor( 78, 150, 220))
    p.setColor(QPalette.Highlight,      QColor( 74, 126, 191))
    p.setColor(QPalette.HighlightedText, Qt.white)
    return p


    # -------------------------------------------------------------- layout --

    def showEvent(self, event):
        """Schedule split sizing after the event loop finalises layout."""
        super().showEvent(event)
        if not getattr(self, "_vs_sized", False):
            self._vs_sized = True
            QTimer.singleShot(0, self._apply_vs_sizes)
        if not getattr(self, "_rag_loader_started", False):
            self._rag_loader_started = True
            QTimer.singleShot(200, self._start_rag_loader)

    def _start_rag_loader(self):
        self._statusbar.showMessage("Loading RAG modules in background...")
        self._rag_thread = QThread()
        self._rag_worker = _RagLoader()
        self._rag_worker.moveToThread(self._rag_thread)
        self._rag_thread.started.connect(self._rag_worker.run)
        self._rag_worker.finished.connect(self._on_rag_loaded)
        self._rag_worker.finished.connect(self._rag_thread.quit)
        self._rag_thread.start()

    def _on_rag_loaded(self, ok: bool, err: str):
        if ok:
            self.rag_augmentor = TscgRagAugmentor(
                db_path  = str(_RAG_DB),
                tar_path = str(_RAG_TAR),
                top_k    = 6,
            )
            self._statusbar.showMessage("RAG ready", 3000)
            print(f"[TSCG] RAG augmentor ready — db={_RAG_DB}", flush=True)
        else:
            self._statusbar.showMessage(
                "RAG not available (chromadb/sentence-transformers missing)", 5000)

    def _apply_vs_sizes(self):
        """Called from the event loop — geometry is final at this point."""
        h = self._vs.height()
        if h > 10:
            # Request 30 % | RAG 20 % | Output 50 %
            self._vs.setSizes([int(h * 0.30), int(h * 0.20), int(h * 0.50)])


def main():
    print(f"[TSCG] Python {sys.version.split()[0]}")
    print(f"[TSCG] Repo root : {_REPO_ROOT}")
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)
    app.setOrganizationName("Echopraxium")
    app.setStyle("Fusion")
    app.setPalette(_dark_palette())
    print("[TSCG] QApplication ready — loading window…")
    win = PocletGeneratorWindow()
    win.show()
    print("[TSCG] Window shown — entering event loop.")
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
