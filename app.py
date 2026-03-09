import streamlit as st
import os
from langchain_core.messages import HumanMessage
from src.agent import app_graph
from src.ingestion import ingest_documents
from src.config import GROQ_API_KEY

# Layout and UI Configuration
st.set_page_config(page_title="Enterprise Agentic AI", page_icon="🤖", layout="wide")

st.markdown("""
<style>
    /* Premium Styling */
    .stApp {
        background-color: #0d1117;
        color: #c9d1d9;
    }
    .header-style {
        text-align: center;
        background: -webkit-linear-gradient(#4b6cb7, #182848);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0;
    }
    .subhead-style {
        text-align: center;
        font-size: 1.2rem;
        color: #8b949e;
        margin-top: 0;
        margin-bottom: 2rem;
    }
    .stChatInputContainer {
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='header-style'>Nexus AI: Enterprise Decision Support</h1>", unsafe_allow_html=True)
st.markdown("<p class='subhead-style'>Autonomous Multi-Agent RAG System</p>", unsafe_allow_html=True)


with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("Groq API Key", type="password", value=GROQ_API_KEY)
    if api_key:
        os.environ["GROQ_API_KEY"] = api_key
    
    st.header("📄 Knowledge Base")
    if st.button("Ingest Local Documents"):
        with st.spinner("Processing and Embedding Enterprise Documents..."):
            ingest_documents()
        st.success("Knowledge Base Unified & Vectorized!")
    st.caption("Place PDF/TXT files in the 'data' directory.")


# Chat interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask an enterprise question..."):
    if not os.environ.get("GROQ_API_KEY"):
        st.warning("Please enter your Groq API Key in the sidebar.")
        st.stop()
        
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.status("Agentic RAG Pipeline Active...", expanded=True) as status:
            st.write("🧭 **Router Agent**: Analyzing query intent...")
            # We invoke the graph with streaming to get intermediate states
            inputs = {"messages": [HumanMessage(content=prompt)]}
            
            final_response = ""
            for output in app_graph.stream(inputs):
                for key, value in output.items():
                    if key == "plan":
                        route = value.get("route", "unknown").upper()
                        st.write(f"🔄 **Route Decision**: Redirecting to `{route}` Agent.")
                    elif key == "retrieve":
                        st.write("📚 **Retrieval Agent**: Scanning Vector Database...")
                        st.write("✅ Context Retrieved successfully.")
                    elif key == "sql":
                        st.write("📊 **SQL Data Agent**: Querying Structured Enterprise Data...")
                        st.write("✅ SQL Results Retrieved.")
                    elif key == "api":
                        st.write("🌐 **Live API Agent**: Fetching real-time external data...")
                        st.write("✅ Live Data Retrieved.")
                    elif key == "analyze":
                        st.write("🧠 **Analysis Agent**: Synthesizing insights...")
                    elif key == "generate":
                        st.write("✍️ **Synthesis Agent**: Drafting executive summary...")
                        final_response = value["messages"][-1].content
            
            status.update(label="Response Synthesized!", state="complete", expanded=False)
        
        st.markdown(final_response)
        st.session_state.messages.append({"role": "assistant", "content": final_response})
