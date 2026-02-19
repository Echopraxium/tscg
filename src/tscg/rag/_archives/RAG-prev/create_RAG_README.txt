pip install langchain langchain-community langchain-openai chromadb
pip install -U langchain langchain-community langchain-openai chromadb
# Force la mise à jour et réinstalle le coeur de langchain
pip install --force-reinstall langchain langchain-openai langchain-community

# Désinstallation des composants potentiellement conflictuels
pip uninstall langchain langchain-core langchain-community langchain-openai -y

# Réinstallation propre et complète
pip install langchain langchain-community langchain-openai chromadb unstructured

pip install -U langchain-google-genai
pip install -U langchain-chroma
pip install -U google-generativeai
pip install -U langchain-google-genai google-generativeai

pip install --upgrade langchain-chroma chromadb langchain-google-genai

pip install sentence-transformers
pip install --upgrade numpy pandas --force-reinstall
pip install google-cloud-aiplatform chromadb sentence-transformers

python create_rag.py

  python create_RAG.py api          # Utilise Google Gemini API
  python create_RAG.py local        # Utilise SentenceTransformers local
  python create_RAG.py --help       # Affiche l'aide détaillée

  python rag_tool.py api        # Utilise Google embeddings
  python rag_tool.py local      # Utilise SentenceTransformers
  python rag_tool.py --help     # Affiche l'aide