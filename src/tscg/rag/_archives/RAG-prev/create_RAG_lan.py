#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
create_RAG_lan.py - Crée la base RAG pour lan_sentences
Usage:
  python create_RAG_lan.py local        # Mode local (embedding local)
  python create_RAG_lan.py api          # Mode API (Google Vertex AI)
  python create_RAG_lan.py --help       # Aide
"""

import os
import json
import argparse
import datetime
from typing import List, Dict, Optional
from pathlib import Path
import time

# ============================================================================
# CONFIGURATION API GOOGLE VERTEX AI
# ============================================================================
GOOGLE_MODEL = "textembedding-gecko@003"
GOOGLE_PROJECT = None  # À configurer
GOOGLE_LOCATION = "us-central1"

# ============================================================================
# FONCTIONS UTILITAIRES
# ============================================================================

def load_documents(input_dir: str) -> List[Dict]:
    """Charge les documents depuis le répertoire"""
    documents = []
    
    for file_path in Path(input_dir).glob("*.txt"):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Découper en paragraphes/chunks significatifs
        paragraphs = []
        current_para = []
        current_length = 0
        
        for line in content.split('\n'):
            line = line.strip()
            if not line:
                continue
                
            # Découper les lignes trop longues
            if len(line) > 1000:
                # Découper par phrases si possible
                sentences = line.split('. ')
                for sentence in sentences:
                    if sentence:
                        if current_length + len(sentence) > 1000 and current_para:
                            # Sauvegarder le paragraphe courant
                            paragraphs.append(' '.join(current_para))
                            current_para = [sentence]
                            current_length = len(sentence)
                        else:
                            current_para.append(sentence)
                            current_length += len(sentence)
            else:
                if current_length + len(line) > 1000 and current_para:
                    paragraphs.append(' '.join(current_para))
                    current_para = [line]
                    current_length = len(line)
                else:
                    current_para.append(line)
                    current_length += len(line)
        
        # Ajouter le dernier paragraphe
        if current_para:
            paragraphs.append(' '.join(current_para))
        
        # Ajouter chaque paragraphe comme un chunk
        for i, para in enumerate(paragraphs):
            if len(para) < 30:  # Ignorer les chunks trop courts
                continue
                
            documents.append({
                "text": para,
                "metadata": {
                    "filename": file_path.name,
                    "file_id": str(file_path),
                    "chunk_id": len(documents),
                    "para_id": i,
                    "char_length": len(para),
                    "word_count": len(para.split())
                }
            })
        
        print(f"✓ {file_path.name}: {len(paragraphs)} paragraphes")
    
    return documents

def get_google_embedding(text: str, project_id: str, location: str = "us-central1") -> List[float]:
    """Obtient les embeddings via Google Vertex AI"""
    try:
        from google.cloud import aiplatform
        from google.oauth2 import service_account
        
        # Initialiser Vertex AI
        aiplatform.init(project=project_id, location=location)
        
        # Créer l'embedding
        result = aiplatform.TextEmbedding(
            model=GOOGLE_MODEL
        ).embed([text])
        
        return result[0].values
        
    except Exception as e:
        print(f"❌ Erreur API Google: {e}")
        raise

def get_local_embedding(text: str, model) -> List[float]:
    """Obtient les embeddings via modèle local"""
    try:
        embedding = model.encode(text)
        return embedding.tolist()
    except Exception as e:
        print(f"❌ Erreur embedding local: {e}")
        raise

# ============================================================================
# FONCTIONS PRINCIPALES
# ============================================================================

def create_database_local(input_dir: str = "./lan_sentences", db_path: str = "./db_lan"):
    """Crée la base avec embeddings locaux"""
    try:
        import chromadb
        from chromadb.config import Settings
        from sentence_transformers import SentenceTransformer
        
        # Configuration
        model_name = "all-MiniLM-L6-v2"
        
        # Vérifier les fichiers
        if not os.path.exists(input_dir):
            print(f"❌ Répertoire '{input_dir}' non trouvé")
            print(f"   Créez le répertoire et placez-y vos fichiers .txt")
            return False
        
        txt_files = list(Path(input_dir).glob("*.txt"))
        if not txt_files:
            print(f"❌ Aucun fichier .txt trouvé dans '{input_dir}'")
            return False
        
        print(f"📁 Répertoire source: {input_dir}")
        print(f"📄 Fichiers trouvés: {len(txt_files)}")
        
        # Charger le modèle
        print(f"🔧 Chargement du modèle {model_name}...")
        model = SentenceTransformer(model_name)
        
        # Initialiser ChromaDB
        print("🗄️  Initialisation de ChromaDB...")
        client = chromadb.PersistentClient(
            path=db_path,
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Créer/obtenir la collection
        collection = client.get_or_create_collection(
            name="tscg_lan",
            metadata={"hnsw:space": "cosine"}
        )
        
        # Charger les documents
        print("📖 Chargement des documents...")
        documents = load_documents(input_dir)
        
        if not documents:
            print("❌ Aucun document valide trouvé")
            return False
        
        # Traiter par batch pour éviter la mémoire
        batch_size = 50
        total_chunks = len(documents)
        
        print(f"\n🔨 Création des embeddings ({total_chunks} chunks)...")
        
        for i in range(0, total_chunks, batch_size):
            batch = documents[i:i+batch_size]
            batch_texts = [doc["text"] for doc in batch]
            batch_metadatas = [doc["metadata"] for doc in batch]
            
            # Créer les embeddings
            print(f"  Batch {i//batch_size + 1}/{(total_chunks+batch_size-1)//batch_size}...")
            embeddings = model.encode(batch_texts)
            
            # Ajouter à la collection
            collection.add(
                embeddings=embeddings.tolist(),
                documents=batch_texts,
                metadatas=batch_metadatas,
                ids=[f"chunk_{j}" for j in range(i, min(i+batch_size, total_chunks))]
            )
            
            time.sleep(0.1)  # Petite pause
            
        # Sauvegarder les métadonnées
        metadata = {
            "mode": "local",
            "model": model_name,
            "input_dir": input_dir,
            "documents": len(txt_files),
            "chunks": total_chunks,
            "created_at": datetime.datetime.now().isoformat(),
            "embedding_dim": len(embeddings[0]) if embeddings else 384
        }
        
        os.makedirs(db_path, exist_ok=True)
        with open(f"{db_path}/metadata.json", "w", encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Base créée avec succès!")
        print(f"📊 {metadata['documents']} documents → {metadata['chunks']} chunks")
        print(f"🎯 Dimension embeddings: {metadata['embedding_dim']}")
        print(f"📁 Base sauvegardée dans: {db_path}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Bibliothèque manquante: {e}")
        print("   Installez avec: pip install sentence-transformers chromadb")
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

def create_database_api(input_dir: str = "./lan_sentences", db_path: str = "./db_lan", 
                       project_id: Optional[str] = None):
    """Crée la base avec embeddings Google Vertex AI"""
    try:
        import chromadb
        from chromadb.config import Settings
        
        # Vérifier les fichiers
        if not os.path.exists(input_dir):
            print(f"❌ Répertoire '{input_dir}' non trouvé")
            return False
        
        txt_files = list(Path(input_dir).glob("*.txt"))
        if not txt_files:
            print(f"❌ Aucun fichier .txt trouvé dans '{input_dir}'")
            return False
        
        # Demander le project_id si non fourni
        if not project_id:
            project_id = input("🔑 Entrez votre Google Cloud Project ID: ").strip()
            if not project_id:
                print("❌ Project ID requis pour l'API Google")
                return False
        
        print(f"📁 Répertoire source: {input_dir}")
        print(f"📄 Fichiers trouvés: {len(txt_files)}")
        print(f"☁️  Mode API: Google Vertex AI ({GOOGLE_MODEL})")
        print(f"🏢 Project ID: {project_id}")
        
        # Vérifier les credentials Google
        print("🔐 Vérification des credentials...")
        try:
            from google.cloud import aiplatform
            from google.auth import default
            
            # Tester l'authentification
            credentials, project = default()
            if project != project_id:
                print(f"⚠️  Attention: Project ID différent ({project} vs {project_id})")
            
            # Initialiser Vertex AI
            aiplatform.init(project=project_id, location=GOOGLE_LOCATION)
            print("✓ Authentification Google réussie")
            
        except Exception as auth_error:
            print(f"❌ Erreur d'authentification Google: {auth_error}")
            print("\n🔧 Configuration requise:")
            print("   1. Activer l'API Vertex AI")
            print("   2. Configurer les credentials:")
            print("      gcloud auth application-default login")
            print("      ou définir GOOGLE_APPLICATION_CREDENTIALS")
            return False
        
        # Initialiser ChromaDB
        print("🗄️  Initialisation de ChromaDB...")
        client = chromadb.PersistentClient(
            path=db_path,
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Créer/obtenir la collection
        collection = client.get_or_create_collection(
            name="tscg_lan",
            metadata={"hnsw:space": "cosine"}
        )
        
        # Charger les documents
        print("📖 Chargement des documents...")
        documents = load_documents(input_dir)
        
        if not documents:
            print("❌ Aucun document valide trouvé")
            return False
        
        # Traiter par batch
        batch_size = 5  # Plus petit pour l'API (limites de quota)
        total_chunks = len(documents)
        
        print(f"\n☁️  Création des embeddings via API ({total_chunks} chunks)...")
        print("   (Cela peut prendre du temps selon le nombre de chunks)")
        
        for i in range(0, total_chunks, batch_size):
            batch = documents[i:i+batch_size]
            batch_texts = [doc["text"] for doc in batch]
            batch_metadatas = [doc["metadata"] for doc in batch]
            
            # Créer les embeddings via API
            print(f"  Batch {i//batch_size + 1}/{(total_chunks+batch_size-1)//batch_size}...")
            
            try:
                from google.cloud import aiplatform
                embeddings = []
                
                for text in batch_texts:
                    embedding = get_google_embedding(text, project_id, GOOGLE_LOCATION)
                    embeddings.append(embedding)
                    time.sleep(0.1)  # Respecter les limites de quota
                
                # Ajouter à la collection
                collection.add(
                    embeddings=embeddings,
                    documents=batch_texts,
                    metadatas=batch_metadatas,
                    ids=[f"chunk_{j}" for j in range(i, min(i+batch_size, total_chunks))]
                )
                
                print(f"    ✓ {len(batch_texts)} chunks traités")
                time.sleep(0.5)  # Pause entre les batchs
                
            except Exception as batch_error:
                print(f"    ❌ Erreur sur le batch: {batch_error}")
                print("    ⏳ Pause de 10 secondes avant réessai...")
                time.sleep(10)
                
                # Réessayer avec un batch plus petit
                try:
                    for j, text in enumerate(batch_texts):
                        embedding = get_google_embedding(text, project_id, GOOGLE_LOCATION)
                        collection.add(
                            embeddings=[embedding],
                            documents=[text],
                            metadatas=[batch_metadatas[j]],
                            ids=[f"chunk_{i+j}"]
                        )
                        time.sleep(0.2)
                    print(f"    ✓ Batch récupéré")
                except:
                    print(f"    ❌ Impossible de récupérer le batch, continuation...")
        
        # Sauvegarder les métadonnées
        metadata = {
            "mode": "api",
            "model": GOOGLE_MODEL,
            "project_id": project_id,
            "location": GOOGLE_LOCATION,
            "input_dir": input_dir,
            "documents": len(txt_files),
            "chunks": total_chunks,
            "created_at": datetime.datetime.now().isoformat(),
            "embedding_dim": len(embeddings[0]) if embeddings else 768
        }
        
        os.makedirs(db_path, exist_ok=True)
        with open(f"{db_path}/metadata.json", "w", encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Base créée avec succès via API Google!")
        print(f"📊 {metadata['documents']} documents → {metadata['chunks']} chunks")
        print(f"🎯 Dimension embeddings: {metadata['embedding_dim']}")
        print(f"📁 Base sauvegardée dans: {db_path}")
        print(f"\n💡 Note: Les embeddings ont été générés via Vertex AI")
        print("   Vérifiez votre consommation sur Google Cloud Console")
        
        return True
        
    except ImportError as e:
        print(f"❌ Bibliothèque manquante: {e}")
        print("   Installez avec: pip install google-cloud-aiplatform chromadb")
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

# ============================================================================
# MAIN
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Crée la base RAG lan_sentences",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  %(prog)s local                 # Mode local (recommandé pour débuter)
  %(prog)s api                   # Mode API Google (nécessite compte Google Cloud)
  %(prog)s api --project my-project  # Spécifie le project ID
  %(prog)s local --dir ./docs    # Spécifie un répertoire source différent
  %(prog)s local --db ./my_db    # Spécifie un répertoire de base différent
  
Configuration API Google:
  1. Activer Vertex AI API: https://console.cloud.google.com/vertex-ai
  2. Configurer l'authentification:
     - gcloud auth application-default login
     - ou définir GOOGLE_APPLICATION_CREDENTIALS
  3. Vérifier les quotas et limites
        """
    )
    
    parser.add_argument("mode", choices=["local", "api"], help="Mode d'embedding")
    parser.add_argument("--dir", default="./lan_sentences", help="Répertoire source des documents")
    parser.add_argument("--db", default="./db_lan", help="Répertoire de la base de données")
    parser.add_argument("--project", help="Google Cloud Project ID (pour mode API)")
    
    args = parser.parse_args()
    
    print("\n" + "="*60)
    print("🏗️  TSCG RAG - Construction de la base lan_sentences")
    print("="*60)
    
    # Vérifier le répertoire source
    if not os.path.exists(args.dir):
        print(f"\n📁 Création du répertoire source: {args.dir}")
        os.makedirs(args.dir, exist_ok=True)
        print("   Placez vos fichiers .txt dans ce répertoire et relancez le script")
        return
    
    if args.mode == "local":
        print(f"\n🤖 Mode: LOCAL (sentence-transformers)")
        print(f"📁 Source: {args.dir}")
        print(f"🗄️  Destination: {args.db}")
        print("-" * 60)
        
        success = create_database_local(args.dir, args.db)
        
        if success:
            print("\n🎉 Installation locale terminée!")
            print("   Pour interroger la base: python query_lan.py")
        else:
            print("\n❌ Échec de la création de la base")
            print("   Vérifiez les messages d'erreur ci-dessus")
    
    else:  # mode API
        print(f"\n☁️  Mode: API GOOGLE VERTEX AI")
        print(f"📁 Source: {args.dir}")
        print(f"🗄️  Destination: {args.db}")
        print(f"🔧 Modèle: {GOOGLE_MODEL}")
        print("-" * 60)
        
        success = create_database_api(args.dir, args.db, args.project)
        
        if success:
            print("\n🎉 Base API créée avec succès!")
            print("   Pour interroger la base: python query_lan.py")
        else:
            print("\n❌ Échec de la création de la base API")
            print("   Vérifiez:")
            print("   1. L'authentification Google Cloud")
            print("   2. L'activation de Vertex AI API")
            print("   3. Les quotas et limites de l'API")

if __name__ == "__main__":
    main()