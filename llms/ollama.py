from langchain_community.chat_models.ollama import ChatOllama

from llms.base import LLM

model_params = {
    "temperature": 0.2,
    "top_p": 0.9,
    "max_gen_len": 2048,
}


class OllamaLLM(LLM):
    def invoke(self, prompt: str) -> str:
        llm = ChatOllama(
            model="llama3.1",
            temperature=model_params["temperature"],
            top_p=model_params["top_p"],
        )
        return llm.invoke(prompt).content
