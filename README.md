# Document Chat

FastAPI based RAG application for uploading PDF, DOCX, or TXT files, indexing them in a local Qdrant store, and asking questions over the uploaded content.

## Setup

1. Install dependencies:

```powershell
uv sync
```

2. Create your environment file:

```powershell
Copy-Item .env.example .env
```

3. Add the API key for the provider selected by `LLM_PROVIDER`.

## Run

```powershell
uv run uvicorn src.api.main:app --reload
```

Open `http://127.0.0.1:8000` in your browser.

## Notes

- Supported upload formats: `.pdf`, `.docx`, `.txt`
- The default vector database path is `qdrantdb/`
- Runtime uploads are stored in `data/` unless `File_Upload_Path` is set
