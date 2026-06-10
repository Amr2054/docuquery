# mini-rag

This is a minimal implementation of the RAG model for question answering

## Requirements

- Python 3.12 or later

## Installation

### Install the required packages

```bash
$ pip install -r requirements.txt
```

### Setup the environment variables

```bash
$ cp .env.example .env
```
Set your environment variables in the `.env` file. Like `OPENAI_API_KEY` value

### Run the FastAPI server
```bash
$ fastapi dev main.py --host 0.0.0.0 --port 5000
```