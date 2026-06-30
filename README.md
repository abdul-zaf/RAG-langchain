# RAG Langchain

A Retrieval-Augmented Generation (RAG) pipeline built with LangChain, FAISS, and Ollama, with a Streamlit frontend.

## Features

- Query a programming languages textbook using natural language
- FAISS vector store for fast semantic search
- Local LLM inference via Ollama (llama3.2)
- Streamlit web UI with suggested questions and retrieved passage viewer

## Run locally

```bash
pip install -r requirements.txt
python -m streamlit run frontend.py
```

Requires [Ollama](https://ollama.com) running locally with `llama3.2` pulled.

## Run with Docker

```bash
docker compose up --build
```

Open http://localhost:8501 in your browser.
