"""
Resolvers for FastAPI
"""

import os
from fastapi import Request
import redis
from src.builder.llm_builder import LLMBuilder
from src.generator.query.query_generator import ChatManager, SQLGenerator


async def get_query_generator(request: Request) -> SQLGenerator:
    """
    Get SQL generator

    :param request: Request
    :type request: Request

    :return: SQLGenerator
    :rtype: SQLGenerator
    """
    body = await request.json()
    model_name = body.get("llm")
    return SQLGenerator(llm=LLMBuilder.get_llm(model_name=model_name))


def get_chat_manager() -> ChatManager:
    """
    Get chat manager

    :return: ChatManager
    :rtype: ChatManager
    """
    return ChatManager(
        redis_client=redis.Redis(
            host=os.environ["REDIS_HOST"],
            port=os.environ["REDIS_PORT"],
        )
    )
