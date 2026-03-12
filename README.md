# UltimateRAG: Document Intelligence for Text & Tables

UltimateRAG is a production-ready **Retrieval-Augmented Generation (RAG)** system designed to handle multi-format document intelligence. Unlike standard RAG implementations, UltimateRAG features specialized pipelines for both **unstructured text** (PDF, DOCX, TXT, MD) and **structured tabular data** (CSV, XLSX), providing high-accuracy answers and summaries.

##  Key Features

- **Hybrid Ingestion:** Specialized processing for text chunks and tabular DataFrames.
- **Advanced Retrieval:** Multi-stage pipeline featuring embedding-based retrieval and LLM-powered reranking.
- **Table Reasoning:** Native support for querying structured data using specialized reasoning logic.
- **Modern UI:** Minimalistic, interactive React frontend with single-click summarization.
- **Scalable Architecture:** Modular backend built with FastAPI, ChromaDB, and Google Gemini.

##  Tech Stack

- **Backend:** FastAPI, Python, ChromaDB, Sentence-Transformers, Pandas.
- **Frontend:** React (Vite), Axios, Modern CSS.
- **LLM:** Google Gemini (Generative AI).

##  Installation

### 1. Prerequisites

- Python 3.9+
- Node.js & npm

### 2. Backend Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/UltimateRAG.git
cd UltimateRAG

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
# Create a .env file with your GOOGLE_API_KEY
echo "GOOGLE_API_KEY=your_api_key_here" > .env
```

### 3. Frontend Setup

```bash
cd frontend
npm install
```

## 🏃 Launching the Application

### Start the Backend

```bash
# From the root directory
uvicorn backend.main:app --reload
```

### Start the Frontend

```bash
# In a separate terminal
cd frontend
npm run dev
```

Visit `http://localhost:5173` to interact with the system.

##  Project Structure

- `backend/`: FastAPI application, routers, and RAG services.
- `frontend/`: React source code and Vite configuration.
- `storage/`: Local persistence for uploaded files (PDFs, images) and document chunks.
- `chroma_db/`: Vector database for high-performance retrieval.

## 💾 Storage & Data Handling

The system automatically manages several local storage locations:
- **`storage/`**: Stores raw uploaded documents and processed metadata.
- **`chroma_db/`**: Persists vector embeddings for the retriever.
- **`temp_uploads/`**: Temporary buffer for active uploads.

> [!TIP]
> Both `storage/` and `chroma_db/` are excluded from Git to prevent tracking large binary data. Ensure you back up these folders if you need to migrate data.


