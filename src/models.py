from enum import Enum
from pydantic import BaseModel


class LLM(Enum):
    openai = "openai"
    claude = "claude"


class ChatRequest(BaseModel):  # noqa: F821
    question: str
    session_id: str
    tenant_id: str
    llm: LLM


class QueryRequest(BaseModel):
    query: str
    session_id: str
