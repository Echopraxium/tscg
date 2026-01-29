# uuid: 99887766-5544-3322-1100-aabbccddeeff
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

def load_api_key():
    try:
        with open(".api_key", "r", encoding="utf-8") as f:
            key = f.read().strip()
            os.environ["GOOGLE_API_KEY"] = key
            return key
        # End of with
    except FileNotFoundError:
        print("Error: .api_key file not found.")
        return None
    # End of except
# End of load_api_key function

def run_query():
    if not load_api_key(): return
    
    # 1. Load the existing database (No re-indexing)
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    db_dir = "./db_vector"
    
    if not os.path.exists(db_dir):
        print("Error: Database directory not found. Please run create_RAG.py first.")
        return
    # End of if check

    vectorstore = Chroma(
        persist_directory=db_dir,
        embedding_function=embeddings
    )

    # 2. Setup Chain
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)
    
    template = """You are the TSCG Assistant. Use the context to answer.
    Context: {context}
    Question: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)
    
    chain = (
        {"context": vectorstore.as_retriever(search_kwargs={"k": 10}), "question": RunnablePassthrough()}
        | prompt | llm | StrOutputParser()
    )

    # 3. Interactive Loop
    print("\n--- TSCG Knowledge Base Ready ---")
    while True:
        user_query = input("\nQuestion (ou 'exit'): ")
        if user_query.lower() in ['exit', 'quit']: break
        
        print("\nGemini is thinking...")
        response = chain.invoke(user_query)
        print(f"\nResponse:\n{response}")
    # End of while loop
# End of run_query function

if __name__ == "__main__":
    run_query()
# End of main block