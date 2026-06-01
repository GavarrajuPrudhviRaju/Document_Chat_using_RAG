from pathlib import Path
import re
import sys
from typing import Iterable, List
import uuid

from fastapi import UploadFile
from src.logger import GLOBAL_LOGGER as log
from src.exception.custom_exception import CustomException
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader

SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt"}


def save_upload_files(uploadfiles: Iterable, targetdir: Path):
    try:
        if targetdir is None:
            raise ValueError("Upload target directory is not configured")

        # convert string to path
        targetdir = Path(targetdir)
        targetdir.mkdir(parents=True, exist_ok=True)
        saved: List[Path] = []
        for uf in uploadfiles:
            name = getattr(uf, "name", "file1.pdf")  # pythontutorial.pdf
            ext = Path(name).suffix.lower()
            if ext not in SUPPORTED_EXTENSIONS:
                log.warning("unsupported file", filename=name)
                continue

            safe_name = re.sub(r'[^a-zA-Z0-9_\-]', '_',
                               Path(name).stem).lower()
            filename = f"{safe_name}_{uuid.uuid4().hex[:6]}{ext}"

            out = targetdir/filename

            with open(out, "wb") as f:
                if hasattr(uf, "read"):
                    f.write(uf.read())
                else:
                    f.write(uf.getbuffer())

            saved.append(out)

        if not saved:
            raise ValueError(
                f"No supported files uploaded. Supported extensions: {', '.join(sorted(SUPPORTED_EXTENSIONS))}"
            )

        return saved

    except Exception as e:
        log.error("failed to save upload files",
                  error=str(e), dir=str(targetdir))
        raise CustomException("failed to save upload files", e)


def load_documents(paths: Iterable[Path]):
    """Load docs using appropriate loader based on extension"""
    docs: List[any] = []
    try:
        for p in paths:
            ext = p.suffix.lower()
            if ext == ".pdf":
                loader = PyPDFLoader(str(p))
            elif ext == ".docx":
                loader = Docx2txtLoader(str(p))
            elif ext == ".txt":
                loader = TextLoader(str(p))
            else:
                log.warning("unsupported extension", path=str(p))
                continue
            docs.extend(loader.load())
        log.info("Documents successfully loaded", count=len(docs))
        return docs
    except Exception as e:
        log.error("failed loading documents", error=str(e))
        raise CustomException("Error loading documents", e)


class FastAPIFileAdapter:
    def __init__(self, uf: UploadFile):
        self.uf = uf
        self.name = uf.filename

    def getbuffer(self):
        self.uf.file.seek(0)
        return self.uf.file.read()


if __name__ == "__main__":
    try:
        save_upload_files()
    except CustomException as e:
        log.error("custom exception", error=str(e))
