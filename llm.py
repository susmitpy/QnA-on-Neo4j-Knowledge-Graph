from typing import Type

from llms.azure_ai_inference import AzureAIInferenceLLM
from llms.base import LLM
from llms.ollama import OllamaLLM

llms_with_params: list[tuple[Type[LLM], dict]] = [
    (OllamaLLM, {}),
    (AzureAIInferenceLLM, {"model": "llama3.3 70"}),
    (AzureAIInferenceLLM, {"model": "llama3.1 8"}),
]

llm_index_to_use = 1

llm_with_param = llms_with_params[llm_index_to_use]

llm = llm_with_param[0](**llm_with_param[1])