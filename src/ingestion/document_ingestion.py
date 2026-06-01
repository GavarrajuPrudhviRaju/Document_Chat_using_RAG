from src.utils.file_ops import save_upload_files, load_documents
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.logger import GLOBAL_LOGGER as log
from src.utils.model_loader import Model_Loader
from src.utils.config_loader import load_config
from langchain_qdrant import QdrantVectorStore
from src.exception.custom_exception import CustomException


class DocumentIngestion():
    def __init__(self):
        self.model_loader = Model_Loader()
        self.config = load_config()

    def splitchunks(self, docs, chunksize=1000, chunkoverlap=200):
        try:
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunksize, chunk_overlap=chunkoverlap)
            chunks = splitter.split_documents(docs)
            log.info("Document split completed")
            return chunks
        except Exception as e:
            log.error("failed chunking")
            raise CustomException("error converting chunks", e)

    def _storevectordb(self, chunks) -> QdrantVectorStore:
        try:
            embed_model = self.model_loader.load_embedding()
            vectorstore = QdrantVectorStore.from_documents(
                documents=chunks,
                embedding=embed_model,
                path="qdrantdb",
                collection_name="document_chat"

            )
            return vectorstore
        except Exception as e:
            log.error("failed storing vectordb", error=str(e))
            raise CustomException("error storing data into vectordb", e)

    def insertvectordb(self, uploadfiles, targetpath, chunksize, chunkoverlap):
        try:
            # load documents
            paths = save_upload_files(uploadfiles, targetpath)
            docs = load_documents(paths)
            # split chunks
            chunks = self.splitchunks(docs, chunksize, chunkoverlap)
            # convert embeddings and store into vectordb
            self._storevectordb(chunks)

            # topk=self.config["retriever"]["top_k"]
            # return Retriever
            # return vectorstore.as_retriever(search_args={"k":topk})
        except Exception as e:
            log.error("failed storing vectordb", error=str(e))
            raise CustomException("Error storing vectordb", e)


# def add(a, b):
#     log.info("started add method")
#     try:
#         a = 9/0
#     except Exception as e:
#         log.error(e)
#         # log.error(str(CustomException(e, sys)))
#         # three scenarios we are handling
#         # customobj=CustomException("Division failed")
#         # customobj=CustomException("Division failed", sys)
#         # customobj=CustomException("Division failed", e)
#         # print(customobj) # it will call __str__ method
#         raise CustomException("Division failed", sys)


# if __name__ == "__main__":
#     try:
#         add(2, 3)
#     except CustomException as e:
#         log.error(str(e))
