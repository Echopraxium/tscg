#!/usr/bin/env python3
"""
rag_tool.py - Outil pour interroger la base TSCG RAG
Usage:
  python rag_tool.py api        # Utilise Google embeddings
  python rag_tool.py local      # Utilise SentenceTransformers
  python rag_tool.py --help     # Affiche l'aide
"""

import os
import argparse
from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from collections import Counter

def parse_args():
    parser = argparse.ArgumentParser(
        description="TSCG RAG Query Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXEMPLES:
  python rag_tool.py api        # Interroge avec Google embeddings
  python rag_tool.py local      # Interroge avec embeddings locaux
  python rag_tool.py api --query "Qu'est-ce que TSCG?"
  python rag_tool.py local --stats
  
  python rag_tool.py --help     # Affiche cette aide
        """
    )
    
    parser.add_argument(
        "mode",
        choices=["api", "local"],
        help="Mode: 'api' pour Google, 'local' pour SentenceTransformers"
    )
    
    parser.add_argument(
        "--query", 
        type=str, 
        help="Question à poser (mode non-interactif)"
    )
    
    parser.add_argument(
        "--stats", 
        action="store_true",
        help="Affiche les statistiques de la base"
    )
    
    parser.add_argument(
        "--sources", 
        action="store_true",
        help="Liste les fichiers sources"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Affiche plus d'informations"
    )
    
    return parser.parse_args()

def load_embeddings(mode, verbose=False):
    """Charge les embeddings selon le mode"""
    if mode == "local":
        if verbose:
            print("🔧 Chargement embeddings locaux...")
        try:
            from langchain_huggingface import HuggingFaceEmbeddings
            return HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs={'device': 'cpu'},
                encode_kwargs={'normalize_embeddings': True}
            )
        except ImportError:
            print("❌ Installez: pip install sentence-transformers")
            return None
    else:  # api
        if verbose:
            print("🔧 Chargement embeddings Google...")
        from langchain_google_genai import GoogleGenerativeAIEmbeddings
        return GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

def load_api_key():
    """Charge la clé API"""
    paths = ["../.api_key", "./.api_key"]
    for path in paths:
        if os.path.exists(path):
            with open(path, "r") as f:
                os.environ["GOOGLE_API_KEY"] = f.read().strip()
                return True
    return False

def format_docs(docs):
    return "\n\n".join([doc.page_content for doc in docs])

def show_stats(vectorstore):
    """Affiche les statistiques"""
    try:
        data = vectorstore.get()
        count = len(data['documents']) if data['documents'] else 0
        print(f"\n📊 Base de données:")
        print(f"  Chunks: {count}")
        
        if data["metadatas"]:
            file_types = Counter()
            for meta in data["metadatas"]:
                if meta and "source" in meta:
                    import os
                    ext = os.path.splitext(meta["source"])[1].lower()
                    file_types[ext] += 1
            
            print(f"  Types de fichiers:")
            for ext, cnt in file_types.most_common():
                print(f"    {ext}: {cnt} chunks")
    except Exception as e:
        print(f"❌ Erreur statistiques: {e}")

def show_sources(vectorstore, limit=20):
    """Affiche les sources"""
    try:
        data = vectorstore.get()
        sources = set()
        for meta in data["metadatas"]:
            if meta and "source" in meta:
                sources.add(os.path.basename(meta["source"]))
        
        print(f"\n📚 Fichiers sources ({len(sources)}):")
        for i, source in enumerate(sorted(list(sources))[:limit], 1):
            print(f"  {i:2}. {source}")
        if len(sources) > limit:
            print(f"  ... et {len(sources) - limit} autres")
    except Exception as e:
        print(f"❌ Erreur sources: {e}")

def main():
    args = parse_args()
    
    print("\n" + "="*60)
    print("🔍 TSCG RAG Query Tool")
    print("="*60)
    
    # Vérifier base de données
    if not os.path.exists("./db_vector"):
        print("❌ Base de données non trouvée. Exécutez d'abord:")
        print(f"   python create_RAG.py {args.mode}")
        return
    
    # Charger embeddings
    embeddings = load_embeddings(args.mode, args.verbose)
    if not embeddings:
        return
    
    # Charger base
    try:
        vectorstore = Chroma(
            persist_directory="./db_vector",
            embedding_function=embeddings,
            collection_name="tscg"
        )
        if args.verbose:
            print("✓ Base de données chargée")
    except Exception as e:
        print(f"❌ Erreur chargement base: {e}")
        return
    
    # Commandes simples
    if args.stats:
        show_stats(vectorstore)
        return
    
    if args.sources:
        show_sources(vectorstore)
        return
    
    # Mode non-interactif avec --query
    if args.query:
        # Charger clé API pour LLM
        if not load_api_key():
            print("❌ Clé API non trouvée. Placez .api_key dans le projet.")
            return
        
        try:
            llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
            
            template = """Répondez basé sur le contexte. Contexte: {context} Question: {question} Réponse:"""
            prompt = ChatPromptTemplate.from_template(template)
            
            chain = (
                {"context": vectorstore.as_retriever(search_kwargs={"k": 8}) | RunnableLambda(format_docs),
                 "question": RunnablePassthrough()}
                | prompt | llm | StrOutputParser()
            )
            
            print(f"\n❓ Question: {args.query}")
            print("🔍 Recherche...")
            response = chain.invoke(args.query)
            print(f"\n💡 Réponse:\n{'-'*40}")
            print(response)
            print('-'*40)
            
        except Exception as e:
            print(f"❌ Erreur: {e}")
        return
    
    # Mode interactif
    print("\nCommandes: query, stats, sources, exit")
    print("="*60)
    
    # Vérifier LLM pour mode interactif
    has_llm = load_api_key()
    if not has_llm:
        print("⚠️  LLM non disponible. Commandes disponibles: stats, sources")
    
    while True:
        try:
            cmd = input("\n> ").strip().lower()
            
            if cmd in ['exit', 'quit']:
                break
            
            elif cmd == 'stats':
                show_stats(vectorstore)
            
            elif cmd == 'sources':
                show_sources(vectorstore)
            
            elif cmd == 'query' or (has_llm and not cmd.startswith('!')):
                if not has_llm:
                    print("❌ LLM non disponible. Vérifiez votre .api_key")
                    continue
                
                question = input("Question: ").strip()
                if not question:
                    continue
                
                try:
                    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
                    
                    template = """Répondez basé sur le contexte. Contexte: {context} Question: {question} Réponse:"""
                    prompt = ChatPromptTemplate.from_template(template)
                    
                    chain = (
                        {"context": vectorstore.as_retriever(search_kwargs={"k": 8}) | RunnableLambda(format_docs),
                         "question": RunnablePassthrough()}
                        | prompt | llm | StrOutputParser()
                    )
                    
                    print("🔍 Recherche...")
                    response = chain.invoke(question)
                    print(f"\n{response}")
                    
                except Exception as e:
                    print(f"❌ Erreur: {e}")
            
            else:
                print("Commande inconnue. Essayez: query, stats, sources, exit")
                
        except KeyboardInterrupt:
            print("\n\n👋 Interrompu. Tape