from langchain_community.chat_models.ollama import ChatOllama

LOCAL = False

if LOCAL:
    model_params = {
        "temperature": 0.95,
        "top_p": 0.95,
        "max_gen_len": 2048,
    }

    llm = ChatOllama(model="llama3.1", temperature=model_params["temperature"], top_p=model_params["top_p"])
    # llm.invoke() -> response 
    # text -> response.content 
else:
    from azure.ai.inference import ChatCompletionsClient
    from azure.ai.inference.models import SystemMessage
    from azure.ai.inference.models import UserMessage
    from azure.core.credentials import AzureKeyCredential
    import configparser
    config = configparser.ConfigParser()
    config.read("env.ini")
    GITHUB_API_KEY = config["DEFAULT"]["GITHUB_TOKEN"]

    client = ChatCompletionsClient(
        endpoint="https://models.inference.ai.azure.com",
        credential=AzureKeyCredential(GITHUB_API_KEY),
    )

    model_params = {
        "temperature": 0.95,
        "top_p": 0.95,
        "max_gen_len": 2048,
    }

    class LLM:
        def invoke(self, prompt: str):
            response = client.complete(
                messages=[
                    SystemMessage(content=""""""),
                    UserMessage(content=prompt),
                ],
                model="Llama-3.3-70B-Instruct",
                temperature=model_params["temperature"],
                max_tokens=model_params["max_gen_len"],
                top_p=model_params["top_p"],
            )

            return response.choices[0].message
            # response.choices[0].message.content has text

            
    llm = LLM()