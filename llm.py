from langchain_community.chat_models.ollama import ChatOllama

model_params = {
    "temperature": 0.95,
    "top_p": 0.95,
    "max_gen_len": 2048,
}

llm = ChatOllama(model="llama3.1", temperature=model_params["temperature"], top_p=model_params["top_p"])