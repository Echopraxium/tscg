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
import glob
from typing import List
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document

# ---------------------------------------------------------------------------
# 0. Package-version guard
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
    except FileNotFoundError:
        print("Error: .api_key file not found.")
        return None
# End of load_api_key


# ---------------------------------------------------------------------------
# 2. Custom document loader (Windows-compatible)
# ---------------------------------------------------------------------------
class TSCGDocumentLoader:
    """Custom document loader that handles Windows paths and encoding issues"""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
    
    def load(self) -> List[Document]:
        try:
            # Normalize path for Windows
            file_path = os.path.normpath(self.file_path)
            
            # Try multiple encodings
            encodings = ['utf-8', 'latin-1', 'cp1252', 'utf-16']
            
            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding, errors='replace') as f:
                        content = f.read()
                    
                    # Only accept if we got meaningful content
                    if content and len(content.strip()) > 0:
                        metadata = {
                            "source": file_path,
                            "filename": os.path.basename(file_path)
                        }
                        return [Document(page_content=content, metadata=metadata)]
                except UnicodeDecodeError:
                    continue
            
            # If all encodings fail, try with binary fallback
            with open(file_path, 'rb') as f:
                binary_content = f.read()
                try:
                    content = binary_content.decode('utf-8', errors='replace')
                except:
                    content = binary_content.decode('latin-1', errors='replace')
                
                metadata = {
                    "source": file_path,
                    "filename": os.path.basename(file_path),
                    "encoding": "fallback"
                }
                return [Document(page_content=content, metadata=metadata)]
                
        except Exception as e:
            print(f"  ⚠️  Could not load {self.file_path}: {type(e).__name__}")
            return []
# End of TSCGDocumentLoader


# ---------------------------------------------------------------------------
# 3. Safe directory loader
# ---------------------------------------------------------------------------
def load_documents_from_directory(
    root_dir: str = ".",
    extensions: List[str] = None,
    ignored_patterns: List[str] = None
) -> List[Document]:
    """Load documents from directory with given extensions"""
    
    if extensions is None:
        extensions = ["*.cs", "*.fs", "*.py", "*.jsonld", "*.md", "*.txt", "*.sparql", "*.ttl"]
    
    if ignored_patterns is None:
        ignored_patterns = ["obj\\", "bin\\", "_archives\\", ".git\\", ".api_key"]
    
    all_docs = []
    
    # Convert patterns to use os.path.sep for cross-platform compatibility
    ignored_patterns = [p.replace('\\', os.path.sep) for p in ignored_patterns]
    
    for ext in extensions:
        # Use glob to find files
        pattern = os.path.join(root_dir, "**", ext)
        files = glob.glob(pattern, recursive=True)
        
        for file_path in files:
            # Skip ignored paths
            skip = False
            for pattern in ignored_patterns:
                if pattern in file_path:
                    skip = True
                    break
            
            if skip:
                continue
            
            try:
                loader = TSCGDocumentLoader(file_path)
                docs = loader.load()
                if docs:
                    all_docs.extend(docs)
            except Exception as e:
                print(f"  ⚠️  Error loading {file_path}: {type(e).__name__}")
                continue
    
    return all_docs
# End of load_documents_from_directory


# ---------------------------------------------------------------------------
# 4. Dedup helper
# ---------------------------------------------------------------------------
def _chunk_hash(doc: Document) -> str:
    raw = f"{doc.metadata.get('source', '')}::{doc.page_content}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()
# End of _chunk_hash


# ---------------------------------------------------------------------------
# 5. Format documents function
# ---------------------------------------------------------------------------
def format_documents(docs: List[Document]) -> str:
    """Format documents for context"""
    return "\n\n".join([doc.page_content for doc in docs])
# End of format_documents


# ---------------------------------------------------------------------------
# 6. Core RAG builder
# ---------------------------------------------------------------------------
def build_tscg_rag():
    print("Initializing TSCG RAG System …")
    _check_versions()
    if not load_api_key():
        return None

    # --- 6a. Ingestion ----------------------------------------------------
    extensions = ["*.cs", "*.fs", "*.jsonld", "*.md", "*.txt"]
    ignored = ["obj\\", "bin\\", "_archives\\", ".git\\", ".api_key"]
    
    print("Scanning local files …")
    
    all_docs = load_documents_from_directory(
        root_dir=".",
        extensions=extensions,
        ignored_patterns=ignored
    )
    
    if not all_docs:
        print("  ❌ No documents found. Check file paths and extensions.")
        return None
    
    print(f"  ✓ Loaded {len(all_docs)} source file(s).")
    
    # Show some sample files
    sample_files = list(set([doc.metadata.get("source", "unknown") for doc in all_docs[:5]]))
    print(f"  Sample files: {', '.join([os.path.basename(f) for f in sample_files])}")

    # --- 6b. Semantic splitting --------------------------------------------
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500, 
        chunk_overlap=200,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    chunks = splitter.split_documents(all_docs)
    print(f"  ✓ Split into {len(chunks)} chunk(s).")

    # --- 6c. Vector store  +  hash-based dedup ----------------------------
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    db_dir = "./db_vector"
    
    # Create directory if it doesn't exist
    os.makedirs(db_dir, exist_ok=True)

    vectorstore = Chroma(
        embedding_function=embeddings,
        persist_directory=db_dir,
        collection_name="tscg"
    )

    # Build the set of hashes already in the DB
    print("Checking existing index …")
    try:
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
        print(f"  ✓ Database contains {len(indexed_hashes)} indexed chunk(s).")
    except Exception as e:
        print(f"  ℹ️  No existing index or error reading: {type(e).__name__}")
        indexed_hashes = set()

    # Keep only genuinely new chunks
    new_chunks = [c for c in chunks if _chunk_hash(c) not in indexed_hashes]
    skipped = len(chunks) - len(new_chunks)
    if skipped:
        print(f"  ⏭️  Skipping {skipped} already-indexed chunk(s).")

    # --- 6d. Rate-limited upsert ------------------------------------------
    if not new_chunks:
        print("  ✅ All content is up to date — no embedding calls needed.")
    else:
        print(f"  🔄 Syncing {len(new_chunks)} new chunk(s) (rate-limited) …")
        batch_size = 5
        total_added = 0
        
        for i in range(0, len(new_chunks), batch_size):
            batch = new_chunks[i : i + batch_size]
            try:
                vectorstore.add_documents(batch)
                total_added += len(batch)
                progress = min(i + batch_size, len(new_chunks))
                print(f"    [{progress}/{len(new_chunks)}] ✓ Added {len(batch)} chunks")
                
                # Don't sleep after last batch
                if i + batch_size < len(new_chunks):
                    print(f"    ⏳ Waiting 15 seconds before next batch...")
                    time.sleep(15)
                    
            except Exception as e:
                error_str = str(e)
                if "429" in error_str or "rate limit" in error_str.lower():
                    print(f"\n  ⚠️  Rate limit detected (429). Progress saved to disk.")
                    print(f"  ⏰ Added {total_added} chunks. Re-run later to continue.")
                    break
                elif "quota" in error_str.lower():
                    print(f"\n  ⚠️  API quota exceeded.")
                    print(f"  ⏰ Added {total_added} chunks. Wait for quota reset.")
                    break
                else:
                    print(f"  ❌ Unexpected error: {type(e).__name__}: {e}")
                    print(f"  🔧 Added {total_added} chunks. Continuing...")
                    break
        
        print(f"  ✅ Total added: {total_added} new chunk(s).")

    # --- 6e. Create retriever ---------------------------------------------
    retriever = vectorstore.as_retriever(
        search_kwargs={
            "k": 8,
            "score_threshold": 0.3
        }
    )
    
    # --- 6f. RAG chain ----------------------------------------------------
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0,
        max_retries=2
    )

    template = """You are a TSCG (Transdisciplinary System Construction Game) knowledge assistant.
Use ONLY the retrieved context below to answer the question.
If the answer is not present in the context, say so explicitly.

Context:
{context}

Question:
{question}

Answer in the same language as the question:"""

    prompt = ChatPromptTemplate.from_template(template)

    # Create the RAG chain properly
    rag_chain = (
        {
            "context": retriever | RunnableLambda(format_documents),
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    
    # Test the chain
    try:
        print("  🧪 Testing RAG chain...")
        test_query = "What is TSCG?"
        test_result = rag_chain.invoke(test_query)
        if test_result and len(test_result.strip()) > 10:
            print(f"  ✅ RAG chain test successful")
            print(f"  Sample response: {test_result[:100]}...")
        else:
            print(f"  ⚠️  RAG chain test returned minimal response")
    except Exception as e:
        print(f"  ⚠️  RAG chain test failed: {type(e).__name__}: {e}")
    
    return rag_chain, vectorstore
# End of build_tscg_rag


# ---------------------------------------------------------------------------
# 7. Interactive query loop
# ---------------------------------------------------------------------------
def interactive_query(rag_chain, vectorstore=None):
    print("\n" + "="*60)
    print("TSCG RAG System - Interactive Mode")
    print("="*60)
    print("Commands:")
    print("  Type your question (supports French/English)")
    print("  Type 'sources' to see indexed documents")
    print("  Type 'test' for a test query")
    print("  Type 'exit' or 'quit' to end")
    print("="*60)
    
    while True:
        try:
            query = input("\n📝 Question: ").strip()
            
            if not query:
                continue
                
            if query.lower() in ['exit', 'quit', 'q']:
                print("👋 Exiting...")
                break
            
            if query.lower() == 'sources':
                if vectorstore:
                    try:
                        data = vectorstore.get()
                        if data and 'metadatas' in data:
                            sources = set()
                            for meta in data['metadatas']:
                                if meta and 'source' in meta:
                                    sources.add(os.path.basename(meta['source']))
                            print(f"\n📚 Indexed documents: {len(sources)} unique files")
                            if sources:
                                print("Sample files:", ', '.join(list(sources)[:10]))
                        else:
                            print("No documents indexed yet.")
                    except:
                        print("Could not retrieve source list.")
                else:
                    print("Vector store not available.")
                continue
            
            if query.lower() == 'test':
                query = "What are the main components of TSCG?"
            
            print("🤔 Processing...")
            
            start_time = time.time()
            response = rag_chain.invoke(query)
            elapsed_time = time.time() - start_time
            
            print(f"\n📤 Response (in {elapsed_time:.1f}s):")
            print("-"*60)
            print(response)
            print("-"*60)
            
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted by user. Exiting...")
            break
        except Exception as e:
            print(f"\n❌ Error: {type(e).__name__}: {e}")
            print("🔧 Please try again with a different query.")
# End of interactive_query


# ---------------------------------------------------------------------------
# 8. Simple RAG function (alternative approach)
# ---------------------------------------------------------------------------
def simple_rag_query(vectorstore, query, llm=None):
    """Simple RAG query function without complex chain"""
    if llm is None:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0,
            max_retries=2
        )
    
    # Retrieve documents
    retriever = vectorstore.as_retriever(search_kwargs={"k": 8})
    docs = retriever.invoke(query)
    
    # Format context
    context = "\n\n".join([doc.page_content for doc in docs])
    
    # Create prompt
    prompt = f"""You are a TSCG (Transdisciplinary System Construction Game) knowledge assistant.
Use ONLY the retrieved context below to answer the question.
If the answer is not present in the context, say so explicitly.

Context:
{context}

Question:
{query}

Answer in the same language as the question:"""
    
    # Get response
    response = llm.invoke(prompt)
    return response.content if hasattr(response, 'content') else str(response)
# End of simple_rag_query


# ---------------------------------------------------------------------------
# 9. Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("🚀 Starting TSCG RAG System...")
    
    result = build_tscg_rag()
    if result:
        rag_chain, vectorstore = result
        print("\n" + "="*60)
        print("✅ TSCG RAG System Ready!")
        print("="*60)
        
        # Test with simple function first
        print("\n📝 Testing with simple RAG function...")
        
        test_queries = [
            "What is TSCG?",
            "Fais un résumé des concepts sémantiques principaux indexés.",
            "Qu'est-ce que TSCG?",
            "Explique le concept de poclet dans TSCG."
        ]
        
        for i, query in enumerate(test_queries, 1):
            print(f"\nTest {i}: {query}")
            print("🤔 Processing...")
            try:
                # Try simple function first
                response = simple_rag_query(vectorstore, query)
                print(f"\n📤 Response:")
                print("-"*40)
                print(response[:500] + "..." if len(response) > 500 else response)
                print("-"*40)
            except Exception as e:
                print(f"❌ Simple RAG failed: {type(e).__name__}: {e}")
                
                # Try with chain
                try:
                    print("Trying with RAG chain...")
                    response = rag_chain.invoke(query)
                    print(f"\n📤 Response (chain):")
                    print("-"*40)
                    print(response[:500] + "..." if len(response) > 500 else response)
                    print("-"*40)
                except Exception as e2:
                    print(f"❌ Both methods failed: {type(e2).__name__}: {e2}")
        
        # Enter interactive mode
        print("\n" + "="*60)
        choice = input("\nEnter interactive mode? (y/n): ").strip().lower()
        if choice in ['y', 'yes', 'oui']:
            interactive_query(rag_chain, vectorstore)
        else:
            print("\n👋 Exiting...")
    
    else:
        print("\n❌ Failed to build RAG system.")
        print("🔧 Check API key, file permissions, and network connection.")
# End of main block