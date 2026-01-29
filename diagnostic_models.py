# uuid: 55667788-9900-aabb-ccdd-eeff11223344
import os
import google.generativeai as genai

def diagnostic_models():
    # Load your key from the .api_key file
    try:
        with open(".api_key", "r", encoding="utf-8") as f:
            api_key = f.read().strip()
            genai.configure(api_key=api_key)
        # End of with
    except FileNotFoundError:
        print("Error: .api_key file not found.")
        return
    # End of except

    print("Checking available models for your API Key...")
    
    try:
        # List all models available for the key
        available_models = genai.list_models()
        
        embedding_models = []
        for m in available_models:
            # We look specifically for models supporting 'embedContent'
            if 'embedContent' in m.supported_generation_methods:
                embedding_models.append(m.name)
            # End of if
        # End of loop

        if embedding_models:
            print("\nModels found for embeddings:")
            for name in embedding_models:
                print(f"-> {name}")
            # End of loop
            print("\nUse one of these strings in GoogleGenerativeAIEmbeddings(model='...')")
        else:
            print("\nNo embedding models found. Check your Google AI Studio project.")
        # End of if/else
        
    except Exception as e:
        print(f"An error occurred during diagnostic: {e}")
    # End of except
# End of diagnostic_models function

if __name__ == "__main__":
    diagnostic_models()
# End of main block