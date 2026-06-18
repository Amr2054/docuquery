# DocuQuery — Document Intelligence API

> Upload documents, ask questions, get answers. A production-ready RAG backend built with FastAPI, Qdrant, and MongoDB.

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white)
![Qdrant](https://img.shields.io/badge/Qdrant-DC244C?style=for-the-badge&logo=qdrant&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)
![Cohere](https://img.shields.io/badge/Cohere-39594E?style=for-the-badge&logo=cohere&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=for-the-badge&logo=pydantic&logoColor=white)

---

## What is DocuQuery?

DocuQuery is a backend API that lets you build document question-answering into any application. You upload files (PDFs or text), the system processes and indexes them semantically, and then you query them in natural language to get grounded, accurate answers — all scoped to isolated projects per tenant or use case.

Under the hood it implements a full **Retrieval-Augmented Generation (RAG)** pipeline:

```
Upload → Chunk → Embed → Index → Retrieve → Generate Answer
```

---

## Features

- **Document ingestion** — upload `.pdf` and `.txt` files with automatic validation and unique file management
- **Smart chunking** — configurable chunk size and overlap using LangChain's `RecursiveCharacterTextSplitter`
- **Semantic search** — embed and index chunks into Qdrant vector DB; search by meaning, not just keywords
- **RAG answer generation** — retrieve the most relevant chunks and feed them to an LLM to generate a grounded answer
- **Multi-provider LLM support** — plug in OpenAI or Cohere for both generation and embeddings, switchable via config
- **OpenAI-compatible endpoint** — works with any OpenAI-compatible API URL, including local model servers
- **Multi-language prompts** — built-in prompt templates in English and Arabic; extensible to other languages
- **Project isolation** — every upload, chunk, and vector collection is scoped to a `project_id`
- **Async throughout** — built on FastAPI with async MongoDB (Motor) for non-blocking I/O
- **Docker-ready** — MongoDB service included in `docker-compose.yml`

---

## Tech Stack

| Layer | Technology |
|---|---|
| API framework | FastAPI |
| Database | MongoDB (via Motor async driver) |
| Vector store | Qdrant (local file-based) |
| LLM / Embeddings | OpenAI, Cohere |
| Document parsing | PyMuPDF (PDF), LangChain TextLoader (TXT) |
| Text splitting | LangChain RecursiveCharacterTextSplitter |
| Config management | Pydantic Settings |
| Containerization | Docker Compose |

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                    FastAPI App                       │
│                                                      │
│  /api/v1/data/upload        → DataController         │
│  /api/v1/data/process       → ProcessController      │
│  /api/v1/nlp/index/push     → NLPController          │
│  /api/v1/nlp/index/search   → NLPController          │
│  /api/v1/nlp/index/answer   → NLPController          │
└──────────┬──────────────────────────┬────────────────┘
           │                          │
    ┌──────▼──────┐           ┌───────▼───────┐
    │   MongoDB   │           │     Qdrant    │
    │  Projects   │           │ Vector Store  │
    │  Assets     │           │ (per-project  │
    │  Chunks     │           │  collections) │
    └─────────────┘           └───────────────┘
           │
    ┌──────▼──────────────────────────┐
    │         LLM Providers           │
    │  OpenAI  |  Cohere              │
    │  (generation + embeddings)      │
    └─────────────────────────────────┘
```

---

## API Reference

All endpoints are prefixed with `/api/v1`.

### Data Endpoints

#### `POST /data/upload/{project_id}`
Upload a file to a project. Creates the project automatically if it doesn't exist.

**Form Data:**
| Field | Type | Description |
|---|---|---|
| `file` | File | `.pdf` or `.txt`, max 10 MB |

**Response:**
```json
{
  "signal": "file_uploaded_successfully",
  "file_id": "<asset_id>"
}
```

---

#### `POST /data/process/{project_id}`
Process uploaded files into text chunks and store them in MongoDB.

**Request Body:**
```json
{
  "file_id": "optional_specific_file_id",
  "chunk_size": 100,
  "overlap_size": 20,
  "do_reset": 0
}
```

| Field          | Type   | Default | Description                                                      |
|----------------|--------|---------|------------------------------------------------------------------|
| `file_id`      | string | `null`  | Target a specific file; omit to process all files in the project |
| `chunk_size`   | int    | `100`   | Characters per chunk                                             |
| `overlap_size` | int    | `20`    | Overlapping characters between chunks                            |
| `do_reset`     | int    | `0`     | Set to `1` to delete existing chunks before processing           |

**Response:**
```json
{
  "signal": "processing_success",
  "inserted_chunks": 142,
  "processed_files": 3
}
```

---

### NLP Endpoints

#### `POST /nlp/index/push/{project_id}`
Embed all MongoDB chunks and push them into the Qdrant vector store.

**Request Body:**
```json
{
  "do_reset": 0
}
```

| Field | Type | Default | Description |
|---|---|---|---|
| `do_reset` | int | `0` | Set to `1` to wipe and rebuild the vector collection |

**Response:**
```json
{
  "signal": "insert_into_vectordb_success",
  "inserted_items_count": 142
}
```

---

#### `GET /nlp/index/info/{project_id}`
Get metadata about a project's Qdrant vector collection (vector count, distance method, config).

**Response:**
```json
{
  "signal": "vectordb_collection_retrieved",
  "collection_info": { ... }
}
```

---

#### `POST /nlp/index/search/{project_id}`
Run a semantic similarity search against the project's vector index.

**Request Body:**
```json
{
  "text": "What are the payment terms?",
  "limit": 5
}
```

**Response:**
```json
{
  "signal": "vectordb_search_success",
  "results": [
    { "text": "...", "score": 0.91 },
    { "text": "...", "score": 0.87 }
  ]
}
```

---

#### `POST /nlp/index/answer/{project_id}`
The full RAG endpoint — retrieves relevant chunks and generates a natural language answer.

**Request Body:**
```json
{
  "text": "What are the payment terms?",
  "limit": 5
}
```

**Response:**
```json
{
  "signal": "rag_answer_success",
  "answer": "Payment is due within 30 days of invoice date...",
  "full_prompt": "...",
  "chat_history": [...]
}
```

---

## Setup & Installation

### Prerequisites

- Python 3.12+
- Docker & Docker Compose
- An OpenAI API key and/or a Cohere API key

---

### 1. Clone the repository

```bash
git clone https://github.com/Amr2054/docuquery.git
cd docuquery
```

### 2. Start MongoDB with Docker

```bash
cd docker
cp .env.example .env
# Fill in MONGO_INITDB_ROOT_USERNAME and MONGO_INITDB_ROOT_PASSWORD
docker compose up -d
cd ..
```

### 3. Install Python dependencies

```bash
cd src
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Open `.env` and fill in your values

### 5. Run the server

```bash
fastapi dev main.py --host 0.0.0.0 --port 5000
```

The API will be live at `http://localhost:5000`. Interactive docs at `http://localhost:5000/docs`.

---

## Typical Workflow

Here's the standard sequence to go from a raw document to a question-answered result:

```
1. POST /data/upload/{project_id}         → upload your file
2. POST /data/process/{project_id}        → chunk the file and store in MongoDB
3. POST /nlp/index/push/{project_id}      → embed chunks and push to Qdrant
4. POST /nlp/index/answer/{project_id}    → ask a question, get an answer
```

You only need to repeat step 1–3 when you add new documents. Step 4 can be called repeatedly for different questions.

---

## Project Structure

```
.
├── docker/
│   ├── docker-compose.yml        # MongoDB service
│   └── .env.example
└── src/
    ├── main.py                   # App entry point, startup/shutdown lifecycle
    ├── requirements.txt
    ├── .env.example
    ├── routes/
    │   ├── base.py               # Health/info endpoint
    │   ├── data.py               # Upload & process routes
    │   ├── nlp.py                # Indexing, search, and answer routes
    │   └── schemes/              # Pydantic request models
    ├── controllers/
    │   ├── BaseController.py     # Shared utilities
    │   ├── DataController.py     # File validation & path management
    │   ├── ProcessController.py  # File loading & chunking
    │   ├── NLPController.py      # Vector DB ops & RAG logic
    │   └── ProjectController.py  # Project directory management
    ├── models/
    │   ├── db_schemes/           # MongoDB Pydantic models (Project, Asset, Chunk)
    │   └── enums/                # Enums for asset types, processing, responses
    ├── stores/
    │   ├── llm/
    │   │   ├── providers/        # OpenAI and Cohere implementations
    │   │   ├── templates/
    │   │   │   └── locales/
    │   │   │       ├── en/       # English RAG prompts
    │   │   │       └── ar/       # Arabic RAG prompts
    │   │   └── LLMProviderFactory.py
    │   └── vectordb/
    │       ├── providers/        # Qdrant implementation
    │       └── VectorDBProviderFactory.py
    └── assets/                   # Uploaded files (per project subdirectory)
```

---

## Adding a New LLM Provider

The LLM layer is built around a provider interface. To add a new provider (e.g., Google Gemini):

1. Create `src/stores/llm/providers/GeminiProvider.py` implementing `LLMInterface`
2. Add the provider enum to `LLMEnums.py`
3. Register it in `LLMProviderFactory.py`
4. Set `GENERATION_BACKEND=GEMINI` in your `.env`

---

## Adding a New Language

Prompt templates are locale-based. To add a new language (e.g., French):

1. Create `src/stores/llm/templates/locales/fr/`
2. Add `__init__.py` and `rag.py` with `system_prompt`, `document_prompt`, and `footer_prompt` templates matching the existing structure
3. Set `PRIMARY_LANG="fr"` in `.env`

---

## License

Apache 2.0 — see [LICENSE](./LICENSE) for details.