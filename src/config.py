import os
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

# Configuration paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
CHROMA_DB_DIR = os.path.join(BASE_DIR, "chroma_db")

# Vector DB configuration
EMBEDDING_MODEL = "all-MiniLM-L6-v2" # Local HuggingFace embedding model
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Get Groq Key (Assuming user will set it)
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

# Ensure directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(CHROMA_DB_DIR, exist_ok=True)
