from functools import lru_cache
import os
from llama_index.llms.openai import OpenAI
import redis
from src.generator.query_generator import ChatManager, SQLGenerator


def get_query_generator():
    return SQLGenerator(
        llm=OpenAI(
            model="gpt-3.5-turbo",
            temperature=0,
            api_key=os.environ["OPENAI_API_KEY"],
        )
    )


def get_chat_manager():

    return ChatManager(
        redis_client=redis.Redis(
            host=os.environ["REDIS_HOST"],
            port=os.environ["REDIS_PORT"],
        )
    )
