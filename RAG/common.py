# RAG/common.py - Module partagé
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

def load_api_key():
    """Charge la clé API depuis la racine"""
    # ... (même fonction que précédemment)

def get_vectorstore():
    """Retourne le vectorstore chargé"""
    # ... (même fonction que précédemment)

def analyze_database(vectorstore):
    """Analyse la base de données (utilisable par plusieurs scripts)"""
    # ... (logique d'analyse)
    return stats