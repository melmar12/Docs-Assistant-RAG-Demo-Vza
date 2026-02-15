# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

RAG (Retrieval Augmented Generation) Internal Docs Assistant — a tool for querying internal documentation using retrieval-augmented generation.

## Repository Structure

- `backend/` — FastAPI server and RAG pipeline (ingestion, embedding, retrieval, generation)
  - `backend/app/main.py` — FastAPI application entrypoint
- `frontend/` — User interface for interacting with the assistant

## Backend Development

```bash
# Activate the virtual environment
source backend/.venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt

# Run the dev server (from repo root)
uvicorn backend.app.main:app --reload
```

The API runs at http://localhost:8000. Docs at http://localhost:8000/docs.
