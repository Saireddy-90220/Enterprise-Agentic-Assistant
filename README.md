# 🤖 Nexus AI: Enterprise Agentic Assistant

An autonomous, multi-agent Retrieval-Augmented Generation (RAG) system built for enterprise decision support. Nexus AI leverages advanced LLM orchestration to intelligently route queries across multiple enterprise data sources, synthesizing executive-level insights in real time.

![Nexus AI Interface Demo](https://img.shields.io/badge/UI-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)
![LangGraph](https://img.shields.io/badge/Orchestration-LangGraph-000000?style=for-the-badge)
![Groq](https://img.shields.io/badge/Inference-Groq_Llama_3.3-F55036?style=for-the-badge)

## 🌟 Key Features

* **Intelligent Routing:** Automatically determines the optimal data source for a given query (Vector DB, SQL Database, or Live API) using `llama-3.1-8b-instant`.
* **Multi-Agent Orchestration:** Powered by **LangGraph**, the system utilizes specialized agents:
  * 📚 **Retrieval Agent:** Queries local ChromaDB vector stores for unstructured data (e.g., PDFs, TXTs) using local HuggingFace embeddings (`all-MiniLM-L6-v2`) for absolute data privacy.
  * 📊 **SQL Data Agent:** Translates natural language into raw SQL to execute against structured enterprise relational databases.
  * 🌐 **Live API Agent:** Reaches out to external APIs to fetch real-time intelligence (e.g., stock prices, external market data).
* **Deep Analysis & Synthesis:** Utilizes the massive reasoning capabilities of `llama-3.3-70b-versatile` to deeply analyze retrieved context and output polished, Markdown-formatted executive summaries.
* **Premium UI:** A fully custom-styled, interactive Streamlit frontend showcasing the live thought-process and intermediate steps of the agentic pipeline.

## 🛠️ Technology Stack

* **Backend & Workflow:** LangChain, LangGraph
* **LLM Provider:** Groq (Llama 3.1 8B, Llama 3.3 70B)
* **Embeddings:** HuggingFace `sentence-transformers`
* **Vector Store:** ChromaDB (Local)
* **Frontend:** Streamlit
* **Document Parsing:** PyMuPDF

## 🚀 Getting Started

### Prerequisites
* Python 3.9+ 
* A [Groq API Key](https://console.groq.com/keys)

### Local Environment Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Saireddy-90220/Enterprise-Agentic-Assistant.git
   cd Enterprise-Agentic-Assistant
   ```

2. **Create and activate a virtual environment:**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration:**
   Create a `.env` file in the root directory (or simply paste it directly into the Streamlit sidebar when the app runs):
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

### Running the Application

Start the Streamlit deployment server locally:
```bash
streamlit run app.py
```
The application will be accessible at `http://localhost:8501`.

## 📂 Project Structure

```text
Enterprise-Agentic-Assistant/
├── app.py                  # Main Streamlit frontend application
├── requirements.txt        # Production dependencies
├── data/                   # Directory for raw PDFs and Text files
├── chroma_db/              # Local vector database storage (Generated)
└── src/                    # Core Backend Logic
    ├── agent.py            # LangGraph StateGraph & Node Definitions
    ├── ingestion.py        # PDF/Txt loading, chunking, and embedding
    ├── sql_agent.py        # Structured data querying logic
    ├── api_agent.py        # External REST API fetching logic
    └── config.py           # Path and embedding configurations
```

## 🧠 Example Queries

To witness the multi-agent routing in action, try the following queries:

1. **Vector Document Query:** `"According to the 2024 Acme report, what are the primary risk factors?"`
2. **SQL Structured Query:** `"What was the exact total annual budget allocated to the Engineering department, and what was their revenue for Q1?"`
3. **Live API Query:** `"As an enterprise executive, I need the current, real-time stock price and trading volume for Acme Corp (ACME) immediately."`

## 🛡️ Data Privacy

By default, the system uses **local HuggingFace embeddings** meaning your internal enterprise documents (PDFs/Text files) are vectorized entirely on your local machine and never sent to an external embedding provider. Only the specific, retrieved context chunks are sent to the LLM for synthesis.

---
_Built for advanced enterprise decision automation._