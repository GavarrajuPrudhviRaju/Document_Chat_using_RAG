import sys
from operator import itemgetter

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_qdrant import QdrantVectorStore
from src.utils.model_loader import Model_Loader
from src.logger import GLOBAL_LOGGER as log
from src.exception.custom_exception import CustomException
from src.utils.config_loader import load_config
from src.prompts.prompts import PROMT_REGISTRY


class ConversationalRAG:
    def __init__(self):
        try:
            # build retirvel
            self.model_loader = Model_Loader()
            self.embed_model = self.model_loader.load_embedding()
            self.config = load_config()
            self.llm = self._load_llm()
            self.retrievar = self._load_qdrant_retrievar()
            log.info("retrievar created successfully")

        # buld prompt
            log.info("building lcel chain")
            self.chain = None
            if self.retrievar is not None:
                self._build_lcel_chain()
                log.info("completed lcel chain")
        except Exception as e:
            log.error("retrieval initialization failed", error=str(e))
            raise CustomException("retrieval initialization failed", sys)

    def _load_qdrant_retrievar(self):
        try:
            vectorstore = QdrantVectorStore.from_existing_collection(
                embedding=self.embed_model,
                path="qdrantdb",
                collection_name="document_chat"
            )
            topk = self.config["retriever"]["top_k"]
            retrievar = vectorstore.as_retriever(search_args={"k": topk})
            return retrievar
        except Exception as e:
            log.error("retrievar created failed", error=str(e))
            raise CustomException("retrievar created failed", sys)

    def _load_llm(self):
        try:
            llm = self.model_loader.load_llm()
            if not llm:
                raise ValueError("LLM could not be found")
            log.info("LLM loaded successfully")
            return llm
        except Exception as e:
            log.error("failed top load LLM", error=str(e))
            raise CustomException("LLM loading faild in ConersationalRAG", sys)

    def _build_lcel_chain(self):
        try:
            # 1. Rewrite user question with chathistory contecxt
            context_question_prompt: ChatPromptTemplate = PROMT_REGISTRY["contextualize_question"]
            question_rewriter = (
                {"input": itemgetter(
                    "input"), "chat_history": itemgetter("chat_history")}
                | context_question_prompt
                | self.llm
                | StrOutputParser()
            )

            retrievedocs = question_rewriter | self.retrievar | self._format_docs

            # 2. Anserr using retrieved context + question rewriter
            context_qa_prompt: ChatPromptTemplate = PROMT_REGISTRY["context_qa"]
            self.chain = (
                {"context": retrievedocs, "input": itemgetter("input")}
                | context_qa_prompt
                | self.llm
                | StrOutputParser()
            )

            log.info("LCEL graph build successfully]")
        except Exception as e:
            log.error(
                "failed to build LCEL chain in ConverstaionalRAG", error=str(e))
            raise CustomException(
                "failed to build LCEL chain in ConverstaionalRAG")

    def _format_docs(self, docs):
        context = " ".join([doc.page_content for doc in docs])
        return context

    def invoke(self, user_input, chat_history):
        try:
            if self.chain is None:
                raise ValueError("Rag chain not initialized", sys)

            chat_history = chat_history or []
            payload = {"input": user_input, "chat_history": chat_history}
            answer = self.chain.invoke(payload)
            if not answer:
                log.warning("No answer generated", user_input=user_input)
                return "no answer generated"

            log.info("chain invoked successfullya nd generated answer",
                     user_input=user_input, answer=str(answer[:100]))
            return answer
        except Exception as e:
            log.error("failed to invoke ConversationalRAG", error=str(e))
            raise CustomException("ailed to invoke ConversationalRAG", sys)


# import sys

# from langchain_core.output_parsers import StrOutputParser
# from langchain_qdrant import QdrantVectorStore
# from src.utils.model_loader import Model_Loader
# from src.logger import GLOBAL_LOGGER as log
# from src.exception.custom_exception import CustomException
# from src.utils.config_loader import load_config
# from src.prompts.prompts import PROMT_REGISTRY


# class ConversationalRAG:
#     def __init__(self):
#         # build retrival
#         # self.model_loader=ModelLoader()
#         self.embed_model = Model_Loader().load_embedding()
#         self.config = load_config()
#         self.llm = self._load_llm()
#         self.retrievar = self._load_qdrant_retrieval()

#         # build prompt
#         self.chain = None
#         if self.retrievar is not None:
#             self.chain = self._build_lcel_chain()

#     def _load_qdrant_retrievar(self):
#         vectorstore = QdrantVectorStore.from_existing_collection(
#             embedding=self.embed_model,
#             path="qdrantdb",
#             collection_name="document_chat"
#         )
#     topk = self.config["retriever"]["top_k"]
#     retrievar = vectorstore.as_retriever(search_args={"k": topk})
#     return retrievar


# def _load_llm(self):
#     try:
#         llm = Model_Loader().load_llm
#         if not llm:
#             raise ValueError("LLM could not be found")
#         log.info("LLM loaded successfully")
#         return llm
#     except Exception as e:
#         log.error("failed top load LLM", error=str(e))
#         raise CustomException("LLM loading failed in ConversationalRAG", sys)

#     def _build_lcel_chain(self, payload):
#         try:
#             # 1. rewrite user question with chat history context
#             context_question_prompt = PROMT_REGISTRY["contextualize_question"]
#             question_rewriter = (
#                 {"input": payload.input, "chat_history": payload.chat_history}
#                 context_question_prompt
#                 self._llm
#                 StrOutputParser
#             )


# retrievedocs = question_rewriter | self.retrievar | self._format_docs


# # 2. Answer using retrieved context + question rewriter
# context_qa_prompt = PROMT_REGISTRY["context_qa"]
# self.chain = (
#     {"context": retrievedocs, "input": payload.input}
#     context_qa_prompt
#     self.llm
#     StrOutputParser
# )

# log.info("LCEL graph build successfully")

# except Exception as e:
#     log.error("failed to build LCEL chain in ConversationalRAG", error=str(e))
#     raise CustomException("failed to build LCEL chain in ConversationalRAG")


# def _format_docs(self, docs):
#     context = " ".join([doc.page_content for doc in docs])
#     return context_qa_prompt


# def invoke(self, user_input, chat_history):
#     try:
#         if self.chain is None:
#             raise CustomException("Rag chain not initialized", sys)

#         chat_history = chat_history or []
#         payload = {"input": user_input, "chat_history": chat_history}
#         answer = self.chain.invoke(payload)
#         if not answer:
#             log.warning("No answer generated", user_input=user_input)
#             return "no answer generated"

#         log.info("chain invoked successfully nd generated answer",
#                  user_input=user_input, answer=str(answer["100"]))
#         return answer
#     except Exception as e:
#         log.error("failed to invoke ConversationalRAG", error=str(e))
#         raise CustomException("ailed to invoke ConversationalRAG", sys)
