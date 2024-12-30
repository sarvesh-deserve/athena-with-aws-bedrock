from functools import lru_cache
import json
from typing import Any, Dict, List, Optional

import redis
import sqlparse
from llama_index.core.llms.llm import LLM
from pydantic import BaseModel

from src.generator.schema.schema_generator import load_schema, transform_for_llama_index


class QueryRequest(BaseModel):
    question: str
    session_id: str
    schema_info: Optional[Dict] = None  # Database schema information


class ChatManager:
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client

    def get_history(self, session_id: str) -> List[Dict]:
        history = self.redis.get(f"sql_chat:{session_id}")
        return json.loads(history) if history else []

    def add_to_history(
        self, session_id: str, question: str, sql: str, max_history: int = 5
    ):
        history = self.get_history(session_id)
        history.append({"question": question, "sql": sql})
        # Keep only the last max_history items
        history = history[-max_history:]
        self.redis.setex(
            f"sql_chat:{session_id}", 3600, json.dumps(history)  # 1 hour expiry
        )


class PromptManager:

    @staticmethod
    @lru_cache(maxsize=None)
    def get_prompt() -> str:
        with open("src/prompt.txt", "r") as f:
            return f.read()


class SQLGenerator:
    def __init__(self, llm: LLM):
        self.llm = llm

    def generate_sql(
        self,
        question: str,
        chat_history: list[dict[str, Any]] = None,
        tenant_id: str = None,
    ) -> str:

        # This can be moved to vector storage
        # Format schema info for the prompt
        llama_schema = json.dumps(
            transform_for_llama_index(load_schema("src/schema_def.json")), indent=2
        )

        # Format chat history
        history_str = "\n".join(
            [f"Q: {msg['question']}\nSQL: {msg['sql']}" for msg in (chat_history or [])]
        )

        # Generate SQL using the LLM
        prompt = PromptManager.get_prompt().format(
            schema_details=llama_schema, chat_history=history_str, question=question,tenant_id=tenant_id
        )

        response = self.llm.complete(prompt)
        sql = response.text

        # Format the SQL query
        sqlparse.format(sql, reindent=True, keyword_case="upper")

        return sql
