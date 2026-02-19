# uuid: 11223344-5566-7788-9900-aabbccddeeff
import os
import time
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document

# --- Configuration ---
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
# End of load_api_key function

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
    # End of load method
# End of SafeTSCGLoader class

def build_tscg_rag():
    print("Initializing TSCG RAG System (Gemini Flash)...")
    if not load_api_key(): return None

    # 1. Ingestion
    exts = ["**/*.cs", "**/*.fs", "**/*.jsonld", "**/*.md"]
    ignored = ["obj\\", "bin\\", "_archives\\", ".git\\", ".api_key"]
    all_docs = []
    
    print("Scanning local files...")
    for ext in exts:
        loader = DirectoryLoader(".", glob=ext, loader_cls=SafeTSCGLoader, silent_errors=True)
        all_docs.extend([d for d in loader.load() if not any(p in d.metadata["source"] for p in ignored)])
    # End of extension loop

    # 2. Semantic Splitting
    splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
    chunks = splitter.split_documents(all_docs)

    # 3. Vector Store with Recovery Logic
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    db_dir = "./db_vector"

    # Chargement de la base existante sans la supprimer
    vectorstore = Chroma(embedding_function=embeddings, persist_directory=db_dir)
    
    # Récupération de l'état actuel de la base
    print("Checking existing index for recovery...")
    existing_data = vectorstore.get()
    
    # On crée un set des contenus déjà indexés pour une comparaison rapide
    # Note: On utilise le contenu ou un hash si possible, ici on se base sur la source + un échantillon du texte
    indexed_signatures = set()
    if existing_data["documents"]:
        for i in range(len(existing_data["documents"])):
            content_sample = existing_data["documents"][i][:50] # 50 premiers caractères
            source = existing_data["metadatas"][i].get("source", "unknown")
            indexed_signatures.add(f"{source}_{content_sample}")
        # End of for
    # End of if
    
    print(f"Database currently contains {len(indexed_signatures)} chunks.")

    # Filtrage des chunks : on ne garde que ceux qui ne sont pas dans la base
    new_chunks = []
    for c in chunks:
        sig = f"{c.metadata['source']}_{c.page_content[:50]}"
        if sig not in indexed_signatures:
            new_chunks.append(c)
        # End of if
    # End of for
    
    skipped = len(chunks) - len(new_chunks)
    if skipped > 0:
        print(f"Skipping {skipped} chunks already indexed.")
    # End of if

    if not new_chunks:
        print("All repository contents are already indexed and up to date.")
    else:
        print(f"Syncing {len(new_chunks)} remaining chunks (Rate Limited Mode)...")
        batch_size = 5 
        for i in range(0, len(new_chunks), batch_size):
            batch = new_chunks[i:i + batch_size]
            try:
                vectorstore.add_documents(batch)
                print(f"Progress (Current Session): {i + len(batch)}/{len(new_chunks)}")
                time.sleep(15) 
            except Exception as e:
                if "429" in str(e):
                    print("\nQuota reached for today. Progress has been saved.")
                    print("Please run the script again in 24 hours.")
                    return None
                else:
                    print(f"Unexpected Error: {e}")
                    break
                # End of if/else
            # End of try/except
        # End of batch loop
    # End of if/else new_chunks

    # 4. Chain Generation
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)
    template = """Use the following context to answer:
    Context: {context}
    Question: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)
    
    rag_chain = (
        {"context": vectorstore.as_retriever(search_kwargs={"k": 8}), "question": RunnablePassthrough()}
        | prompt | llm | StrOutputParser()
    )
    return rag_chain
# End of build_tscg_rag function

if __name__ == "__main__":
    chain = build_tscg_rag()
    if chain:
        print("\n--- TSCG RAG Ready ---")
        query = "Fais un résumé des concepts sémantiques principaux indexés."
        print(chain.invoke(query))
    # End of if
# End of main block