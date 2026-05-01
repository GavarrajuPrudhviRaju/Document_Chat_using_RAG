import sys
import os
from src.utils.config_loader import load_config
from src.logger import GLOBAL_LOGGER as log
from src.exception.custom_exception import CustomException
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings


class Model_Loader:
    def __init__(self):
        load_dotenv()  # for loading env variables
        log.info("loading configs")
        self.config = load_config()
        log.info(self.config)

    def load_embedding(self):
        try:
            embedding_model_name = self.config["embedding_model"]["model_name"]
            log.info("loaded embedding model", model=embedding_model_name)
            return HuggingFaceEmbeddings(model_name=embedding_model_name)
        except Exception as e:
            log.error("Error loading embedding model", str(e))
            raise CustomException("failed to load embedding model", sys)

    def load_llm(self):
        try:
            llm_block = self.config["llm"]
            provider_key = os.getenv("LLM_PROVIDER", "groq")

            if provider_key not in llm_block:
                log.error("LLM provider not found in config",
                          provider=provider_key)
                return ValueError(f"LLM Provider {provider_key} not found in config")

            llm_config = llm_block[provider_key]
            model_name = llm_config.get("model_name")
            temperature = llm_config.get("temprature")
            max_tokens = llm_config.get("max_output_tokens")
            provider = llm_config.get("provider")

            log.info("loading llm", provider=provider_key, model=model_name)

            if provider == "google":
                return ChatGoogleGenerativeAI(model=model_name, google_api_key="", temperature=temperature, max_tokens=max_tokens)
            elif provider == "groq":
                return ChatGroq(model=model_name, api_key=os.getenv("GROQ_API_KEY"), max_tokens=max_tokens, temperature=temperature)
            else:
                return ChatOpenAI(model=model_name, api_key=os.getenv("OPENAPI_API_KEY"), max_tokens=max_tokens, temperature=temperature)
        except Exception as e:
            log.error("Error loading llm", error=str(e))
            raise ValueError("error loading llm")


# for local testing only dont send to production
if __name__ == "__main__":
    loader = Model_Loader()

    # test embedding
    embedding = loader.load_embedding()
    embed_result = embedding.embed_query("Hi how are you")
    print(embed_result)

    # testllm
    llm = loader.load_llm()
    llm_result = llm.invoke(
        "what is the difference between token and embeddings")
    print(f"llm_result: {llm_result.content}")
