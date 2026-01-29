# uuid: 12345-check-env
import sys
import importlib.util

modules = ["langchain", "langchain_community", "langchain_openai", "chromadb"]

print(f"Python version: {sys.version}")
print("-" * 30)

for mod in modules:
    spec = importlib.util.find_spec(mod)
    status = "OK" if spec is not None else "MISSING"
    print(f"{mod.ljust(20)}: {status}")

# Test spécifique pour le sous-module chains
try:
    from langchain.chains import RetrievalQA
    print("langchain.chains     : OK")
except ImportError as e:
    print(f"langchain.chains     : FAILED ({e})")