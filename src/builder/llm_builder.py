from llama_index.core.llms.llm import LLM
from llama_index.llms.openai import OpenAI
import os
from llama_index.llms.bedrock import Bedrock


class LLMBuilder:
    @staticmethod
    def get_llm(model_name: str) -> LLM:
        """
        Get LLM model based on the model name

        :param model_name: str
        :return: LLM
        """
        match model_name:
            case "openai":
                return OpenAI(
                    model="gpt-3.5-turbo",
                    temperature=0,
                    api_key=os.environ["OPENAI_API_KEY"],
                )
            case "claude":
                return Bedrock(
                    model="anthropic.claude-3-sonnet-20240229-v1:0", temperature=0
                )
            case _:
                raise ValueError(f"Model {model_name} not found")
