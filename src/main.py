import uuid
from fastapi import Depends, FastAPI
from pydantic import BaseModel

from src.generator.query.query_generator import ChatManager, SQLGenerator
from src.resolvers import get_chat_manager, get_query_generator
from src.executor.query_executor import QueryExecutor


app = FastAPI()


class ChatRequest(BaseModel):
    question: str
    session_id: str
    tenant_id: str

class QueryRequest(BaseModel):
    query: str
    session_id: str


@app.post("/generate-sql")
async def generate_sql(
    request: ChatRequest,
    chat_manager: ChatManager = Depends(get_chat_manager),
    sql_generator: SQLGenerator = Depends(get_query_generator),
):
    # Get chat history
    history = chat_manager.get_history(request.session_id)

    # Generate SQL
    sql = sql_generator.generate_sql(
        question=request.question, chat_history=history, tenant_id=request.tenant_id
    )

    # Save to history
    chat_manager.add_to_history(
        session_id=request.session_id, question=request.question, sql=sql
    )

    return {"sql": sql, "history": chat_manager.get_history(request.session_id)}


@app.post("/execute-sql")
async def execute_sql(
    request: QueryRequest,
):
    # Execute SQL
    data = QueryExecutor.execute_sql(query=request.query,report_id=str(uuid.uuid4()))

    return {"data": data.to_dict(orient="records")}
