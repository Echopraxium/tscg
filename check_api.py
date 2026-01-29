import os
import google.generativeai as genai

# Chargez votre clé
with open(".api_key", "r") as f:
    os.environ["GOOGLE_API_KEY"] = f.read().strip()

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

print("Modèles disponibles pour votre clé :")
for m in genai.list_models():
    if 'embedContent' in m.supported_generation_methods:
        print(f"-> {m.name}")