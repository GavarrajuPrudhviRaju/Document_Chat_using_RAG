from pathlib import Path
from typing import List
import os

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from src.logger import GLOBAL_LOGGER as log
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Ui related code
# Project root
BASE_DIR = Path(__file__).resolve().parent.parent.parent
file_upload_path = os.getenv("File_Upload_Path")
FileUploadPath = Path(file_upload_path) if file_upload_path else BASE_DIR / "data"

# UI folder
UI_DIR = BASE_DIR / "ui"
print("ui directory", UI_DIR)

# Static files
app.mount(
    "/static",
    StaticFiles(directory=UI_DIR / "static"),
    name="static"
)


@app.get("/")
async def getinfo():
    return FileResponse(UI_DIR / "index.html")


@app.post("/chat/index")
async def chat_index(files: List[UploadFile] = File(...),
                     chunk_size=Form(1000),
                     chunk_overlap=Form(200)):
    try:
        log.info("document ingestion started")
        from src.ingestion.document_ingestion import DocumentIngestion
        from src.utils.file_ops import FastAPIFileAdapter

        wrapped = [FastAPIFileAdapter(file) for file in files]
        docingestion = DocumentIngestion()

        docingestion.insertvectordb(
            wrapped, FileUploadPath, int(chunk_size), int(chunk_overlap))
        log.info("Document ingestion completed")
        return {"Response": "Document ingestion completed sucessfully"}
    except Exception as e:
        log.error("Document ingestion failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Indexing failed: {e}")


@app.post("/chat/query")
async def ChatQuery(question=Form(...)):
    try:
        log.info("calling invoke method")
        from src.retrieval.retrieval import ConversationalRAG

        cr = ConversationalRAG()
        # fetching history from database
        chat_history = ""
        answer = cr.invoke(question, chat_history)
        # insert chat hisrtory into database
        log.info("complted invoke method calling")
        log.info("get the response sucessfully")
        return {
            "answer": answer
        }
    except Exception as e:
        log.error(f"chat query failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"query failed: {e}")
