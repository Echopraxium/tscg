# uuid: 11223344-5566-7788-9900-aabbccddeeff
# ---------------------------------------------------------------------------
# create_RAG.py  —  TSCG RAG System
# Model targets (Feb 2026):
#   LLM        → gemini-2.5-flash   (stable, replaces retired 1.5-flash)
#   Embeddings → models/gemini-embedding-001  (unchanged)
# ---------------------------------------------------------------------------
import os
import sys
import time
import hashlib
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document

# ---------------------------------------------------------------------------
# 0. Package-version guard
#    chromadb 1.x rewrote the storage layer; langchain_chroma < 0.2.x may
#    silently corrupt the persist directory.  We warn early.
# ---------------------------------------------------------------------------
def _check_versions():
    import importlib.metadata as _meta
    chroma_ver = tuple(int(x) for x in _meta.version("chromadb").split(".")[:2])
    lc_chroma_ver = tuple(
        int(x) for x in _meta.version("langchain-chroma").split(".")[:2]
    )
    if chroma_ver >= (1, 0):
        if lc_chroma_ver < (0, 2):
            print(
                "⚠️  chromadb >= 1.0 detected but langchain-chroma < 0.2. "
                "Run:  pip install --upgrade langchain-chroma chromadb"
            )
            sys.exit(1)
    print(f"  chromadb {'.'.join(map(str,chroma_ver))}  |  "
          f"langchain-chroma {'.'.join(map(str,lc_chroma_ver))}  ✓")
# End of _check_versions


# ---------------------------------------------------------------------------
# 1. API key loader
# ---------------------------------------------------------------------------
def load_api_key():
    try:
        with open(".api_key", "r", encoding="utf-8") as f:
            key = f.read().strip()
            os.environ["GOOGLE_API_KEY"] = key
            return key
        # End of with
    except FileNotFoundError:
        print("Error: .api_key file not found.")
        return None
    # End of except
# End of load_api_key


# ---------------------------------------------------------------------------
# 2. Safe document loader (encoding-tolerant)
# ---------------------------------------------------------------------------
class SafeTSCGLoader(TextLoader):
    def __init__(self, file_path: str):
        super().__init__(file_path, encoding="utf-8")
    # End of __init__

    def load(self):
        try:
            with open(self.file_path, encoding="utf-8", errors="replace") as f:
                text = f.read()
            return [Document(page_content=text, metadata={"source": self.file_path})]
        except Exception:
            return []
    # End of load
# End of SafeTSCGLoader


# ---------------------------------------------------------------------------
# 3. Dedup helper  —  deterministic SHA-256 per chunk
#    More reliable than prefix-matching (handles edits inside a chunk).
# ---------------------------------------------------------------------------
def _chunk_hash(doc: Document) -> str:
    raw = f"{doc.metadata.get('source', '')}::{doc.page_content}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()
# End of _chunk_hash


# ---------------------------------------------------------------------------
# 4. Core RAG builder
# ---------------------------------------------------------------------------
def build_tscg_rag():
    print("Initializing TSCG RAG System …")
    _check_versions()
    if not load_api_key():
        return None

    # --- 4a. Ingestion ----------------------------------------------------
    exts    = ["**/*.cs", "**/*.fs", "**/*.jsonld", "**/*.md"]
    ignored = ["obj\\", "bin\\", "_archives\\", ".git\\", ".api_key"]
    all_docs: list[Document] = []

    print("Scanning local files …")
    for ext in exts:
        loader = DirectoryLoader(
            ".", glob=ext, loader_cls=SafeTSCGLoader, silent_errors=True
        )
        all_docs.extend(
            d for d in loader.load()
            if not any(p in d.metadata["source"] for p in ignored)
        )
    # End of extension loop
    print(f"  Loaded {len(all_docs)} source file(s).")

    # --- 4b. Semantic splitting --------------------------------------------
    splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
    chunks   = splitter.split_documents(all_docs)
    print(f"  Split into {len(chunks)} chunk(s).")

    # --- 4c. Vector store  +  hash-based dedup ----------------------------
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    db_dir     = "./db_vector"

    vectorstore = Chroma(
        embedding_function=embeddings,
        persist_directory=db_dir,
        collection_name="tscg"          # explicit name → safer with chroma 1.x
    )

    # Build the set of hashes already in the DB
    print("Checking existing index …")
    existing_data = vectorstore.get(include=["metadatas", "documents"])

    indexed_hashes: set[str] = set()
    if existing_data["documents"]:
        for doc_text, meta in zip(existing_data["documents"],
                                  existing_data["metadatas"]):
            dummy = Document(
                page_content=doc_text,
                metadata=meta if meta else {}
            )
            indexed_hashes.add(_chunk_hash(dummy))
        # End of for
    # End of if
    print(f"  Database contains {len(indexed_hashes)} indexed chunk(s).")

    # Keep only genuinely new chunks
    new_chunks = [c for c in chunks if _chunk_hash(c) not in indexed_hashes]
    skipped    = len(chunks) - len(new_chunks)
    if skipped:
        print(f"  Skipping {skipped} already-indexed chunk(s).")

    # --- 4d. Rate-limited upsert ------------------------------------------
    if not new_chunks:
        print("  All content is up to date — no embedding calls needed.")
    else:
        print(f"  Syncing {len(new_chunks)} new chunk(s) (rate-limited) …")
        batch_size = 5
        for i in range(0, len(new_chunks), batch_size):
            batch = new_chunks[i : i + batch_size]
            try:
                vectorstore.add_documents(batch)
                print(f"    [{i + len(batch)}/{len(new_chunks)}] ✓")
                time.sleep(15)                          # stay under free-tier RPM
            except Exception as e:
                if "429" in str(e):
                    print("\n  ⚠️  Rate limit (429). Progress saved to disk.")
                    print("  Re-run the script after ~24 h to continue.")
                    return None
                else:
                    print(f"  ✗ Unexpected error: {e}")
                    break
                # End of if/else
            # End of try/except
        # End of batch loop
    # End of if/else new_chunks

    # --- 4e. RAG chain ----------------------------------------------------
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",       # ← retired 1.5-flash → 2.5-flash
        temperature=0
    )

    template = """You are a TSCG (Transdisciplinary System Construction Game) knowledge assistant.
Use ONLY the retrieved context below to answer the question.
If the answer is not present in the context, say so explicitly.

Context:
{context}

Question:
{question}

Answer:"""

    prompt = ChatPromptTemplate.from_template(template)

    rag_chain = (
        {
            "context" : vectorstore.as_retriever(search_kwargs={"k": 8}),
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain
# End of build_tscg_rag


# ---------------------------------------------------------------------------
# 5. Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    chain = build_tscg_rag()
    if chain:
        print("\n--- TSCG RAG Ready ---\n")
        # Exemple de requête en français (le modèle supporte le français)
        query = "Fais un résumé des concepts sémantiques principaux indexés."
        print(f"Query : {query}\n")
        print(chain.invoke(query))
    # End of if
# End of main block
