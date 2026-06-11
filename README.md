# Medical AI Assistant — RAG Q&A System

A retrieval-augmented generation (RAG) system for healthcare documents built with FastAPI, MongoDB, Qdrant vector database, and Cohere embeddings. Includes a vanilla JavaScript frontend served directly from FastAPI.

## Please Visit The Link

[mini-rag-project-onuw.onrender.com](https://mini-rag-project-onuw.onrender.com)

## Features

- **RAG Query Interface**: Chat-based interface to ask questions about indexed Medical documents
- **Batch Embedding**: Efficient Cohere embeddings with batch processing (reduces API calls)
- **Vector Search**: Qdrant vector database for semantic search
- **MongoDB Storage**: Document and project metadata storage
- **Single-Page Frontend**: Vanilla HTML/CSS/JS served by FastAPI  
- **Project Selector**: Switch between different RAG projects at runtime

## Project Structure

```
Medical AI Assistant/
├── docker/
│   ├── docker-compose.yaml       # MongoDB 
│   └── mongoDB/                  # MongoDB data volume
├── src/
│   ├── main.py                   # FastAPI app entry point
│   ├── requirements.txt           # Python dependencies
│   ├── .env                       # Configuration (API keys, DB settings)
│   ├── static/
│   │   └── index.html            # Chat frontend (single file)
│   ├── routes/
│   │   ├── base.py               # Base routes
│   │   ├── data.py               # File upload/processing routes
│   │   └── nlp.py                # RAG and search routes
│   ├── controllers/
│   │   ├── NLPController.py      # RAG logic
│   │   ├── DataController.py     # Data processing
│   │   └── ProcessController.py  # File processing
│   ├── stores/
│   │   ├── llm/                  # LLM providers (Cohere, OpenAI, Gemini)
│   │   └── vectordb/             # Vector DB (Qdrant)
│   └── models/                   # Data models and schemas
```

## Prerequisites

- **MongoDB Atlas** account and cluster for remote MongoDB
- **Qdrant Cloud** account and API key for remote vector search
- **Python 3.9+** with venv or conda
- **Studio 3T** (optional) — [download](https://studio3t.com/download/)
- **API Keys**:
  - Gemini API Key (generation) — [get here](https://aistudio.google.com/)
  - Cohere API Key (embeddings) — [get here](https://cohere.com/api)
  - OpenAI API Key (optional) — [get here](https://platform.openai.com/)

## Quick Start

### 1. Configure MongoDB Atlas and Qdrant Cloud

For remote deployment, skip local Docker setup and connect using your MongoDB Atlas cluster string and Qdrant Cloud endpoint.

### 2. Connect to MongoDB with Studio 3T

1. **Open Studio 3T** → **New Connection**
2. **Server**: copy your Atlas cluster host from Atlas connection string
3. **Port**: default MongoDB Atlas port (`27017` or as provided)
4. **Username**: Atlas database user
5. **Password**: Atlas user password
6. **Authentication Database**: `admin` or your Atlas auth DB
7. **Database**: `mini-rag`
8. Click "Test Connection" → "Save"

### 3. Set Up Python Environment

```bash
cd src

# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Edit `src/.env`:
```
MONGODB_URL=mongodb+srv://<username>:<password>@<cluster-host>/mini-rag?retryWrites=true&w=majority
MONGODB_DATABASE=mini-rag

VECTORDB_BACKEND=QDRANT
# For Qdrant Cloud, set the remote URL and API key below.
VECTOR_DB_URL=https://<your-cloud-instance>.eu-central-1-0.aws.cloud.qdrant.io
VECTOR_DB_API_KEY=your_qdrant_cloud_api_key
VECTOR_DB_DISTANCE_METHOD=cosine

GENERATION_BACKEND=GEMINI
EMBEDDING_BACKEND=COHERE

GEMINI_API_KEY=your_gemini_api_key_here
GENERATION_MODEL_ID=gemini-3.1-flash-lite

COHERE_API_KEY=your_cohere_api_key_here
EMBEDDING_MODEL_ID=embed-multilingual-light-v3.0
EMBEDDING_MODEL_SIZE=384

OPENAI_API_KEY=
OPENAI_API_URL=

default_input_max_char=1024
default_output_max_char=200
temperature=0.1

PRIMARY_LANGUAGE=en
DEFAULT_LANGUAGE=ar
```

Replace API keys with your actual keys.

### 5. Run the FastAPI Server

```bash
cd src
uvicorn main:app --reload 
```

Server starts at `http://127.0.0.1`

## Using the Chat Interface

1. **Open browser** → `http://127.0.0.1`
2. **Set project ID** (default `1`):
   - Enter a project ID in the "Project" field
   - Click "Set"
3. **Ask a question**:
   - Type your question in the chat input
   - Click "Send" or press Enter
   - The backend queries the RAG endpoint and displays the answer

### URL Parameters

You can also pass project ID via URL:
```
http://127.0.0.1/?project=1
```

## API Endpoints

### RAG Chat
**POST** `/api/v1/nlp/rag/answer/{project_id}`
- Query the RAG system
- **Body**: `{"text": "your question", "limit": 5}`
- **Response**: `{"signal": "RAG_ANSWER_SUCCESS", "answer": "...", "full_prompt": "...", "chat_history": [...]}`

### Index Documents
**POST** `/api/v1/nlp/index/push/{project_id}`
- Index all project chunks into Qdrant vector database
- **Body**: `{"do_reset": 0}` (set to 1 to clear existing index)
- **Response**: `{"signal": "IS_INSERTED", "Inserted Item Count": N}`

### Semantic Search
**POST** `/api/v1/nlp/index/search/{project_id}`
- Search indexed documents
- **Body**: `{"text": "search query", "limit": 5}`
- **Response**: `{"signal": "RESPONSE_RETRIEVED", "Result": [...]}`

### Upload & Process Files
**POST** `/api/v1/data/upload/{project_id}`
- Upload a document file (PDF, TXT, etc.)
- Processes and chunks it automatically
- Returns file metadata and chunk count

### Get Project Info
**GET** `/api/v1/nlp/index/info/{project_id}`
- Get collection info for a project
- **Response**: `{"signal": "COLLECTION_INFO", "Collection_Info": {...}}`

## MongoDB Collections

### `projects`
```json
{
  "_id": ObjectId,
  "project_id": "1",
  "created_at": ISODate,
  "updated_at": ISODate
}
```

### `files`
```json
{
  "_id": ObjectId,
  "project_id": "1",
  "file_name": "document.pdf",
  "file_type": "pdf",
  "file_size": 12345,
  "file_path": "/path/to/file",
  "chunks_count": 10,
  "created_at": ISODate
}
```

### `chunks`
```json
{
  "_id": ObjectId,
  "project_id": "1",
  "file_id": ObjectId,
  "chunk_text": "Lorem ipsum...",
  "chunk_metadata": {"page": 1, "section": "intro"},
  "created_at": ISODate
}
```




