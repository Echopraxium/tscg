#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
update_RAG.py - Mise à jour incrémentielle de la base TSCG RAG
Usage: python update_RAG.py
"""

import os
import sys
import time

# Ajouter le dossier courant au path pour les imports
sys.path.append('.')

try:
    from create_RAG import load_documents_from_directory, _chunk_hash
    from langchain_chroma import Chroma
    from langchain_google_genai import GoogleGenerativeAIEmbeddings
    from langchain_core.documents import Document
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're running from the RAG/ directory and all dependencies are installed.")
    sys.exit(1)

# ---------------------------------------------------------------------------
# 1. Configuration
# ---------------------------------------------------------------------------
def load_api_key():
    """Charge la clé API depuis la racine du projet"""
    try:
        # Essayer d'abord depuis la racine du projet (../.api_key)
        root_key = "../.api_key"
        if os.path.exists(root_key):
            with open(root_key, "r", encoding="utf-8") as f:
                key = f.read().strip()
                os.environ["GOOGLE_API_KEY"] = key
                print("✓ API key loaded from project root")
                return True
        
        # Sinon depuis le dossier courant
        with open(".api_key", "r", encoding="utf-8") as f:
            key = f.read().strip()
            os.environ["GOOGLE_API_KEY"] = key
            print("✓ API key loaded from current directory")
            return True
            
    except FileNotFoundError:
        print("❌ Error: .api_key file not found.")
        print("   Place it in either:")
        print("   - Project root (../.api_key)")
        print("   - RAG folder (./.api_key)")
        return False

# ---------------------------------------------------------------------------
# 2. Fonction de mise à jour
# ---------------------------------------------------------------------------
def update_vector_store():
    """Mise à jour incrémentielle de la base de données"""
    print("\n" + "="*60)
    print("🔄 TSCG RAG - Incremental Update")
    print("="*60)
    
    # Charger la clé API
    if not load_api_key():
        return
    
    # Charger les nouveaux documents
    print("\n📂 Scanning for new or modified files...")
    new_docs = load_documents_from_directory(
        root_dir="..",  # Scanner depuis la racine
        extensions=["*.md", "*.jsonld", "*.txt", "*.cs", "*.fs"],
        ignored_patterns=["obj\\", "bin\\", "_archives\\", ".git\\", ".api_key", "RAG\\"]
    )
    
    if not new_docs:
        print("❌ No documents found.")
        return
    
    print(f"✓ Found {len(new_docs)} raw documents.")
    
    # Charger la base de données existante
    db_dir = "./db_vector"
    if not os.path.exists(db_dir):
        print(f"❌ Database directory '{db_dir}' not found.")
        print("   Please run 'python create_RAG.py' first.")
        return
    
    print("📦 Loading existing vector database...")
    try:
        embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
        vectorstore = Chroma(
            persist_directory=db_dir,
            embedding_function=embeddings,
            collection_name="tscg"
        )
    except Exception as e:
        print(f"❌ Error loading vector store: {e}")
        return
    
    # Vérifier les doublons
    print("🔍 Checking for duplicates...")
    try:
        existing = vectorstore.get()
        existing_hashes = set()
        
        if existing["documents"]:
            for doc_text, meta in zip(existing["documents"], existing["metadatas"]):
                dummy = Document(page_content=doc_text, metadata=meta if meta else {})
                existing_hashes.add(_chunk_hash(dummy))
            print(f"✓ Database contains {len(existing_hashes)} existing chunks.")
    except Exception as e:
        print(f"⚠️  Could not read existing data: {e}")
        existing_hashes = set()
    
    # Filtrer les nouveaux documents
    new_chunks = [doc for doc in new_docs if _chunk_hash(doc) not in existing_hashes]
    
    if not new_chunks:
        print("\n✅ No new chunks to add. Database is up to date.")
        return
    
    print(f"\n🆕 Found {len(new_chunks)} new chunks to add.")
    
    # Ajouter par lots
    try:
        batch_size = 5
        total_batches = (len(new_chunks) + batch_size - 1) // batch_size
        
        print(f"\n📤 Adding {len(new_chunks)} chunks in {total_batches} batches...")
        print("   (Rate limited to avoid API quotas)")
        
        for i in range(0, len(new_chunks), batch_size):
            batch = new_chunks[i:i + batch_size]
            batch_num = i // batch_size + 1
            
            print(f"\n   Batch {batch_num}/{total_batches} ({len(batch)} chunks)...")
            vectorstore.add_documents(batch)
            print(f"   ✓ Added batch {batch_num}")
            
            # Pause entre les lots (sauf après le dernier)
            if i + batch_size < len(new_chunks):
                print(f"   ⏳ Waiting 10 seconds before next batch...")
                time.sleep(10)
        
        print(f"\n🎉 Successfully added {len(new_chunks)} new chunks!")
        
        # Afficher un résumé
        try:
            final_data = vectorstore.get()
            final_count = len(final_data["documents"]) if final_data["documents"] else 0
            print(f"\n📊 Database now contains {final_count} total chunks.")
        except:
            pass
        
    except Exception as e:
        print(f"\n❌ Error adding documents: {type(e).__name__}: {e}")
        
        # Vérifier si c'est une erreur de quota/rate limit
        error_str = str(e).lower()
        if "429" in str(e) or "rate limit" in error_str or "quota" in error_str:
            print("\n⚠️  Rate limit or quota exceeded.")
            print("   Progress has been saved. You can run this script again later.")
    
    print("\n" + "="*60)

# ---------------------------------------------------------------------------
# 3. Point d'entrée
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    try:
        update_vector_store()
        input("\nPress Enter to exit...")
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user. Exiting...")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        input("\nPress Enter to exit...")