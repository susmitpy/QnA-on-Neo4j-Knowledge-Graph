from abc import ABC, abstractmethod


class LLM(ABC):
    @abstractmethod
    def invoke(self, prompt: str) -> str:
        """
        Invokes the LLM model with the given prompt and returns the response.

        Args:
            prompt (str): The prompt to be used for the LLM model.

        Returns:
            str: The text response from the LLM model.

        """
        pass
