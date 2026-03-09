import os
from langchain_core.messages import HumanMessage
from src.agent import app_graph
from src.ingestion import ingest_documents
from dotenv import load_dotenv

load_dotenv()

def run_test_query():
    print("========================================")
    print("  ENTERPRISE AGENTIC AI - CLI TEST  ")
    print("========================================")
    
    if not os.environ.get("GROQ_API_KEY"):
        print("\n[!] Error: GROQ_API_KEY is not set in .env")
        print("Please add it before running tests.")
        return

    # Ingest if the ChromaDB doesn't exist yet
    if not os.path.exists("chroma_db"):
        print("\n[*] Initializing Knowledge Base...")
        ingest_documents()
    else:
        print("\n[*] Knowledge Base already exists.")

    print("\n[?] Enter an enterprise query (e.g., 'What are the strategic initiatives for 2025?'):")
    query = input("> ")

    print("\n[*] Initializing Agentic Workflow...")
    inputs = {"messages": [HumanMessage(content=query)]}
    
    final_message = ""
    for output in app_graph.stream(inputs):
        for key, value in output.items():
            print(f"[*] Step executed: {key}")
            if key == "generate":
                final_message = value["messages"][-1].content
    
    print("\n========================================")
    print("             FINAL RESPONSE             ")
    print("========================================")
    print(final_message)
    print("\n========================================")

if __name__ == "__main__":
    run_test_query()
