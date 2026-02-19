#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
create_RAG.py - TSCG RAG System avec syntaxe simple
Usage:
  python create_RAG.py api          # Utilise Google Gemini API
  python create_RAG.py local        # Utilise SentenceTransformers local
  python create_RAG.py --help       # Affiche l'aide détaillée
"""

import os
import sys
import time
import hashlib
import glob
import argparse
from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document

# ---------------------------------------------------------------------------
# 0. Parser d'arguments avec syntaxe api/local
# ---------------------------------------------------------------------------
def parse_arguments():
    """Parse les arguments de ligne de commande avec syntaxe api/local"""
    parser = argparse.ArgumentParser(
        description="TSCG RAG System - Crée une base de connaissances vectorielle",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXEMPLES:
  python create_RAG.py api           # Utilise Google Gemini API (besoin de clé)
  python create_RAG.py local         # Utilise SentenceTransformers local (gratuit)
  
  python create_RAG.py api --update  # Mise à jour avec API Google
  python create_RAG.py local --test  # Teste avec embeddings locaux
  
  python create_RAG.py api --extensions md txt --chunk-size 2000
  python create_RAG.py local --no-llm  # Uniquement embeddings, pas de LLM
  
  python create_RAG.py --version     # Affiche la version
  python create_RAG.py --help        # Affiche cette aide

CONSEILS:
  • Utilisez 'local' si vous dépassez les quotas Google
  • Utilisez 'api' pour de meilleurs embeddings (quota limité)
  • Placez votre clé API dans ../.api_key ou ./.api_key
        """
    )
    
    # Argument principal (api ou local)
    parser.add_argument(
        "mode",
        choices=["api", "local"],
        help="Mode d'exécution: 'api' pour Google Gemini, 'local' pour SentenceTransformers"
    )
    
    # Options générales
    parser.add_argument(
        "--update", 
        action="store_true",
        help="Mode mise à jour incrémentielle (ajoute seulement les nouveaux fichiers)"
    )
    
    parser.add_argument(
        "--test", 
        action="store_true",
        help="Mode test (vérifie le système sans ajouter de documents)"
    )
    
    parser.add_argument(
        "--extensions", 
        nargs="+",
        default=["md", "jsonld", "txt", "cs", "fs"],
        help="Extensions de fichiers à indexer (défaut: md jsonld txt cs fs)"
    )
    
    parser.add_argument(
        "--chunk-size", 
        type=int,
        default=1500,
        help="Taille des chunks en caractères (défaut: 1500)"
    )
    
    parser.add_argument(
        "--chunk-overlap", 
        type=int,
        default=200,
        help="Chevauchement entre chunks (défaut: 200)"
    )
    
    parser.add_argument(
        "--no-llm", 
        action="store_true",
        help="Désactive le LLM (utilise uniquement les embeddings)"
    )
    
    parser.add_argument(
        "--api-key", 
        type=str,
        metavar="CHEMIN",
        help="Chemin vers le fichier .api_key (défaut: cherche dans ../.api_key ou ./.api_key)"
    )
    
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Lance directement le mode interactif après la création"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="TSCG RAG System v2.0 (Février 2026)"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Affiche plus d'informations de debug"
    )
    
    return parser.parse_args()

# ---------------------------------------------------------------------------
# 1. Chargement de la clé API
# ---------------------------------------------------------------------------
def load_api_key(api_key_path=None, verbose=False):
    """Charge la clé API Gemini depuis le chemin spécifié ou par défaut"""
    possible_paths = []
    
    # Chemin spécifié par l'utilisateur
    if api_key_path:
        possible_paths.append(api_key_path)
    
    # Chemins par défaut
    possible_paths.extend(["../.api_key", "./.api_key"])
    
    for path in possible_paths:
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    key = f.read().strip()
                    os.environ["GOOGLE_API_KEY"] = key
                    if verbose:
                        print(f"✓ Clé API chargée depuis : {path}")
                    else:
                        print(f"✓ Clé API chargée")
                    return key
            except Exception as e:
                if verbose:
                    print(f"⚠️  Erreur lecture {path}: {e}")
                continue
    
    print("⚠️  Fichier .api_key non trouvé. Le LLM ne sera pas disponible.")
    print("   Vous pouvez quand même utiliser les embeddings locaux.")
    return None

# ---------------------------------------------------------------------------
# 2. Gestion des embeddings selon le mode
# ---------------------------------------------------------------------------
def get_embeddings(mode, verbose=False):
    """Retourne le modèle d'embeddings selon le mode choisi"""
    if mode == "local":
        print("🔧 Configuration des embeddings LOCAUX (SentenceTransformers)...")
        try:
            # Essayer d'importer
            from langchain_huggingface import HuggingFaceEmbeddings
            if verbose:
                print("✓ SentenceTransformers trouvé")
        except ImportError:
            print("📦 Installation de sentence-transformers...")
            import subprocess
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "sentence-transformers"])
                from langchain_huggingface import HuggingFaceEmbeddings
                print("✓ SentenceTransformers installé")
            except Exception as e:
                print(f"❌ Échec installation: {e}")
                print("   Exécutez: pip install sentence-transformers")
                return None
        
        return HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
    
    else:  # mode == "api"
        print("🔧 Configuration des embeddings GOOGLE API (Gemini)...")
        try:
            from langchain_google_genai import GoogleGenerativeAIEmbeddings
            return GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
        except Exception as e:
            print(f"❌ Erreur chargement Google embeddings: {e}")
            print("   Utilisez 'python create_RAG.py local' pour les embeddings locaux")
            return None

# ---------------------------------------------------------------------------
# 3. Custom document loader
# ---------------------------------------------------------------------------
class TSCGDocumentLoader:
    def __init__(self, file_path: str):
        self.file_path = file_path
    
    def load(self) -> List[Document]:
        try:
            file_path = os.path.normpath(self.file_path)
            
            encodings = ['utf-8', 'latin-1', 'cp1252']
            
            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding, errors='replace') as f:
                        content = f.read()
                    
                    if content and len(content.strip()) > 0:
                        metadata = {
                            "source": file_path,
                            "filename": os.path.basename(file_path),
                            "size": len(content),
                            "encoding": encoding
                        }
                        return [Document(page_content=content, metadata=metadata)]
                except UnicodeDecodeError:
                    continue
            
            # Fallback binaire
            with open(file_path, 'rb') as f:
                binary_content = f.read()
                try:
                    content = binary_content.decode('utf-8', errors='replace')
                except:
                    content = binary_content.decode('latin-1', errors='replace')
                
                metadata = {
                    "source": file_path,
                    "filename": os.path.basename(file_path),
                    "size": len(content),
                    "encoding": "fallback"
                }
                return [Document(page_content=content, metadata=metadata)]
                
        except Exception as e:
            print(f"  ⚠️  Impossible de charger {self.file_path}: {type(e).__name__}")
            return []

# ---------------------------------------------------------------------------
# 4. Safe directory loader
# ---------------------------------------------------------------------------
def load_documents_from_directory(
    root_dir: str = "..",
    extensions: List[str] = None,
    ignored_patterns: List[str] = None,
    verbose: bool = False
) -> List[Document]:
    
    if extensions is None:
        extensions = ["*.md", "*.jsonld", "*.txt"]
    
    if ignored_patterns is None:
        ignored_patterns = ["obj\\", "bin\\", "_archives\\", ".git\\", ".api_key", "RAG\\"]
    
    all_docs = []
    ignored_patterns = [p.replace('\\', os.path.sep) for p in ignored_patterns]
    
    for ext in extensions:
        pattern = os.path.join(root_dir, "**", ext)
        files = glob.glob(pattern, recursive=True)
        
        if verbose:
            print(f"  Recherche {ext}... {len(files)} fichiers trouvés")
        
        for file_path in files:
            # Ignorer les chemins spécifiés
            skip = False
            for pattern in ignored_patterns:
                if pattern in file_path:
                    skip = True
                    break
            
            if skip:
                if verbose:
                    print(f"  Ignoré: {file_path}")
                continue
            
            try:
                loader = TSCGDocumentLoader(file_path)
                docs = loader.load()
                if docs:
                    all_docs.extend(docs)
                    if verbose:
                        print(f"  ✓ Chargé: {os.path.basename(file_path)}")
            except Exception as e:
                if verbose:
                    print(f"  ⚠️  Erreur chargement {file_path}: {type(e).__name__}")
                continue
    
    return all_docs

# ---------------------------------------------------------------------------
# 5. Utilitaires
# ---------------------------------------------------------------------------
def _chunk_hash(doc: Document) -> str:
    raw = f"{doc.metadata.get('source', '')}::{doc.page_content}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()

def format_documents(docs: List[Document]) -> str:
    return "\n\n".join([doc.page_content for doc in docs])

# ---------------------------------------------------------------------------
# 6. Fonction principale
# ---------------------------------------------------------------------------
def build_tscg_rag(args):
    """Fonction principale avec paramètres"""
    
    print("\n" + "="*60)
    print("🚀 TSCG RAG System")
    print("="*60)
    print(f"Mode: {'GOOGLE API' if args.mode == 'api' else 'LOCAL (SentenceTransformers)'}")
    if args.update:
        print("🔄 Mode: MISE À JOUR (incrémentiel)")
    if args.test:
        print("🧪 Mode: TEST (lecture seule)")
    if args.no_llm:
        print("🤖 LLM: DÉSACTIVÉ")
    print("="*60)
    
    # Charger la clé API (nécessaire pour le LLM, même en mode local)
    api_key = load_api_key(args.api_key, args.verbose)
    
    # Initialiser les embeddings selon le mode
    embeddings = get_embeddings(args.mode, args.verbose)
    if embeddings is None:
        print("❌ Échec initialisation des embeddings.")
        return None
    
    # --- Chargement des documents ------------------------------------------
    if not args.test:
        print("\n📂 Scan des documents...")
        
        # Convertir les extensions en pattern glob
        extensions = [f"*.{ext}" if not ext.startswith("*") else ext for ext in args.extensions]
        
        all_docs = load_documents_from_directory(
            root_dir="..",
            extensions=extensions,
            ignored_patterns=["obj\\", "bin\\", "_archives\\", ".git\\", ".api_key", "RAG\\"],
            verbose=args.verbose
        )
        
        if not all_docs:
            print("  ❌ Aucun document trouvé avec les extensions spécifiées.")
            return None
        
        print(f"  ✓ {len(all_docs)} fichier(s) source chargé(s).")
        
        # Afficher un échantillon
        if len(all_docs) > 0 and args.verbose:
            sample_files = list(set([doc.metadata.get("source", "inconnu") for doc in all_docs[:5]]))
            print(f"  Échantillon: {', '.join([os.path.basename(f) for f in sample_files])}")
        
        # --- Découpage en chunks -------------------------------------------
        print("\n🔪 Découpage des documents...")
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=args.chunk_size, 
            chunk_overlap=args.chunk_overlap,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        chunks = splitter.split_documents(all_docs)
        print(f"  ✓ {len(chunks)} chunk(s) créé(s).")
        
        if args.verbose and chunks:
            avg_size = sum(len(c.page_content) for c in chunks) / len(chunks)
            print(f"  Taille moyenne: {avg_size:.0f} caractères")
    else:
        print("\n⏸️  MODE TEST - Pas de chargement/découpage")
        chunks = []
    
    # --- Base de données vectorielle ---------------------------------------
    print("\n💾 Configuration base de données vectorielle...")
    db_dir = "./db_vector"
    os.makedirs(db_dir, exist_ok=True)
    
    try:
        vectorstore = Chroma(
            embedding_function=embeddings,
            persist_directory=db_dir,
            collection_name="tscg"
        )
        print(f"  ✓ Base de données prête: {db_dir}")
    except Exception as e:
        print(f"❌ Erreur base de données: {e}")
        return None
    
    # --- Vérification des doublons -----------------------------------------
    if not args.test:
        print("\n🔍 Vérification doublons...")
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
            print(f"  ✓ Base contient {len(indexed_hashes)} chunk(s) existant(s).")
        except Exception as e:
            if args.verbose:
                print(f"  ℹ️  Pas d'index existant: {type(e).__name__}")
            indexed_hashes = set()
        
        # --- Ajout des nouveaux chunks -------------------------------------
        new_chunks = [c for c in chunks if _chunk_hash(c) not in indexed_hashes]
        skipped = len(chunks) - len(new_chunks)
        
        if skipped:
            print(f"  ⏭️  {skipped} chunk(s) déjà indexé(s) ignoré(s).")
        
        if not new_chunks:
            print("\n✅ Base à jour - aucun ajout nécessaire.")
        else:
            print(f"\n🔄 Ajout de {len(new_chunks)} nouveau(x) chunk(s)...")
            
            # Taille des lots selon le mode
            batch_size = 50 if args.mode == "local" else 5  # Plus grand si local
            total_added = 0
            
            for i in range(0, len(new_chunks), batch_size):
                batch = new_chunks[i : i + batch_size]
                batch_num = i // batch_size + 1
                total_batches = (len(new_chunks) + batch_size - 1) // batch_size
                
                if args.mode == "api":  # Rate limiting pour Google
                    print(f"    Lot {batch_num}/{total_batches} - Pause 15s pour quota API...")
                    time.sleep(15)
                
                try:
                    vectorstore.add_documents(batch)
                    total_added += len(batch)
                    progress = min(i + batch_size, len(new_chunks))
                    print(f"    [{progress}/{len(new_chunks)}] ✓ Lot {batch_num} ajouté ({len(batch)} chunks)")
                    
                except Exception as e:
                    error_str = str(e)
                    if "429" in error_str or "rate limit" in error_str.lower():
                        print(f"\n⚠️  Limite de quota atteinte. {total_added} chunk(s) ajouté(s).")
                        print("   Relancez plus tard pour continuer.")
                        break
                    elif "quota" in error_str.lower():
                        print(f"\n⚠️  Quota API épuisé. {total_added} chunk(s) ajouté(s).")
                        print("   Attendez 24h ou utilisez 'python create_RAG.py local'")
                        break
                    else:
                        print(f"❌ Erreur lot {batch_num}: {type(e).__name__}")
                        if args.verbose:
                            print(f"   Détails: {e}")
                        break
            
            print(f"\n✅ {total_added} nouveau(x) chunk(s) ajouté(s).")
    
    # --- Configuration du LLM (optionnel) ----------------------------------
    rag_chain = None
    if not args.no_llm and api_key:
        print("\n🤖 Configuration LLM (Gemini)...")
        try:
            llm = ChatGoogleGenerativeAI(
                model="gemini-2.5-flash",
                temperature=0,
                max_retries=2
            )
            
            template = """Vous êtes l'assistant TSCG. Répondez UNIQUEMENT basé sur le contexte.

Contexte:
{context}

Question: {question}

Répondez dans la même langue que la question. Si l'information n'est pas dans le contexte, dites-le."""

            prompt = ChatPromptTemplate.from_template(template)

            rag_chain = (
                {
                    "context": vectorstore.as_retriever(search_kwargs={"k": 8}) | RunnableLambda(format_documents),
                    "question": RunnablePassthrough()
                }
                | prompt
                | llm
                | StrOutputParser()
            )
            
            print("  ✓ Chaîne RAG prête")
            
            # Test simple
            if not args.test:
                print("  🧪 Test de la chaîne RAG...")
                try:
                    test_query = "Qu'est-ce que TSCG?"
                    test_result = rag_chain.invoke(test_query)
                    if test_result and len(test_result.strip()) > 10:
                        print(f"  ✅ Test réussi")
                        if args.verbose:
                            print(f"  Extrait: {test_result[:150]}...")
                    else:
                        print(f"  ⚠️  Réponse minimale du test")
                except Exception as e:
                    print(f"  ⚠️  Test LLM échoué: {type(e).__name__}")
                    if args.verbose:
                        print(f"     Détails: {e}")
        
        except Exception as e:
            print(f"❌ Configuration LLM échouée: {type(e).__name__}")
            if args.verbose:
                print(f"   Détails: {e}")
            print("   Utilisation des embeddings seulement.")
    
    return rag_chain, vectorstore, args

# ---------------------------------------------------------------------------
# 7. Mode interactif
# ---------------------------------------------------------------------------
def interactive_mode(rag_chain, vectorstore, args):
    """Mode interactif pour poser des questions"""
    if rag_chain is None:
        print("\n⚠️  LLM non disponible. Mode interactif impossible.")
        print("   Vérifiez votre clé API ou utilisez sans --no-llm.")
        return
    
    print("\n" + "="*60)
    print("🧠 TSCG RAG - Mode Interactif")
    print("="*60)
    print("Posez des questions sur TSCG en français ou anglais")
    print("Commandes: 'exit'=quitter, 'stats'=statistiques, 'sources'=fichiers")
    print("="*60)
    
    while True:
        try:
            query = input("\n❓ Question: ").strip()
            
            if not query:
                continue
                
            if query.lower() in ['exit', 'quit', 'q']:
                print("\n👋 Au revoir !")
                break
            
            if query.lower() == 'stats':
                try:
                    data = vectorstore.get()
                    count = len(data['documents']) if data['documents'] else 0
                    print(f"\n📊 Statistiques base:")
                    print(f"  Chunks totaux: {count}")
                    print(f"  Mode embeddings: {'GOOGLE API' if args.mode == 'api' else 'LOCAL'}")
                    print(f"  LLM disponible: OUI")
                    
                    if data["metadatas"]:
                        import os
                        from collections import Counter
                        file_types = Counter()
                        for meta in data["metadatas"]:
                            if meta and "source" in meta:
                                ext = os.path.splitext(meta["source"])[1].lower()
                                file_types[ext] += 1
                        
                        print(f"\n  Types de fichiers:")
                        for ext, cnt in file_types.most_common(5):
                            print(f"    {ext}: {cnt} chunks")
                            
                except Exception as e:
                    print(f"⚠️  Impossible statistiques: {e}")
                continue
            
            if query.lower() == 'sources':
                try:
                    data = vectorstore.get()
                    sources = set()
                    for meta in data["metadatas"]:
                        if meta and "source" in meta:
                            sources.add(os.path.basename(meta["source"]))
                    
                    print(f"\n📚 Fichiers sources ({len(sources)}):")
                    for i, source in enumerate(sorted(list(sources))[:15], 1):
                        print(f"  {i:2}. {source}")
                    if len(sources) > 15:
                        print(f"  ... et {len(sources) - 15} autres")
                except Exception as e:
                    print(f"⚠️  Impossible sources: {e}")
                continue
            
            print("🔍 Recherche...")
            try:
                response = rag_chain.invoke(query)
                print(f"\n💡 Réponse:\n{'-'*40}")
                print(response)
                print('-'*40)
            except Exception as e:
                print(f"\n❌ Erreur: {type(e).__name__}")
                if "429" in str(e) or "quota" in str(e).lower():
                    print("   Quota API épuisé. Essayez plus tard.")
                elif "api key" in str(e).lower():
                    print("   Problème clé API. Vérifiez votre fichier .api_key")
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Interrompu. Tapez 'exit' pour quitter.")
        except Exception as e:
            print(f"\n❌ Erreur entrée: {e}")

# ---------------------------------------------------------------------------
# 8. Point d'entrée principal
# ---------------------------------------------------------------------------
def main():
    """Fonction principale"""
    # Parser les arguments
    args = parse_arguments()
    
    # Construction du système RAG
    result = build_tscg_rag(args)
    
    if result is None:
        print("\n❌ Création système RAG échouée.")
        sys.exit(1)
    
    rag_chain, vectorstore, args = result
    
    # Résumé final
    print("\n" + "="*60)
    if rag_chain:
        print("✅ Système TSCG RAG Prêt ! (RAG Complet)")
    else:
        print("✅ Base embeddings TSCG Prête ! (LLM non disponible)")
    print("="*60)
    
    # Statistiques finales
    try:
        data = vectorstore.get()
        total_chunks = len(data["documents"]) if data["documents"] else 0
        
        print(f"\n📊 Statistiques finales:")
        print(f"  Chunks totaux: {total_chunks}")
        print(f"  Mode: {'GOOGLE API' if args.mode == 'api' else 'LOCAL (SentenceTransformers)'}")
        print(f"  LLM: {'DISPONIBLE' if rag_chain else 'NON DISPONIBLE'}")
        print(f"  Base de données: ./db_vector/")
        
        if total_chunks > 0 and args.verbose:
            total_chars = sum(len(doc) for doc in data["documents"])
            avg_size = total_chars / total_chunks
            print(f"  Taille moyenne chunk: {avg_size:.0f} caractères")
            print(f"  Caractères totaux: {total_chars:,}")
    
    except Exception as e:
        print(f"⚠️  Impossible statistiques finales: {e}")
    
    # Mode interactif automatique ou sur demande
    if rag_chain and (args.interactive or not args.test):
        if args.interactive:
            interactive_mode(rag_chain, vectorstore, args)
        else:
            choice = input("\n🎮 Mode interactif ? (o/n): ").strip().lower()
            if choice in ['o', 'oui', 'y', 'yes']:
                interactive_mode(rag_chain, vectorstore, args)
    
    print("\n" + "="*60)
    print("👋 Terminé !")
    print("="*60)

# ---------------------------------------------------------------------------
# 9. Gestion des erreurs
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrompu par l'utilisateur. Au revoir !")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {type(e).__name__}: {e}")
        if "--verbose" in sys.argv:
            import traceback
            traceback.print_exc()
        sys.exit(1)