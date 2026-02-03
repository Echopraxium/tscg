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

python create_rag.py