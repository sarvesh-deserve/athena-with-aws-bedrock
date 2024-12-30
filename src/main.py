"""Main FastAPI application"""

import uuid
from fastapi import Depends, FastAPI

from src.models import ChatRequest, QueryRequest
from src.generator.query.query_generator import ChatManager, SQLGenerator
from src.resolvers import get_chat_manager, get_query_generator
from src.executor.query_executor import QueryExecutor


app = FastAPI()


@app.post("/generate-sql")
async def generate_sql(
    request: ChatRequest,
    chat_manager: ChatManager = Depends(get_chat_manager),
    sql_generator: SQLGenerator = Depends(get_query_generator),
) -> dict:
    """
    Generate SQL from the given question

    :param request: ChatRequest
    :param chat_manager: ChatManager

    :return: str
    """
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
) -> dict:
    """
    Execute SQL query

    :param request: QueryRequest
    :type request: QueryRequest

    :return: Result of the SQL query
    :rtype: dict
    """
    # Execute SQL
    data = QueryExecutor.execute_sql(query=request.query, report_id=str(uuid.uuid4()))

    return {"data": data.to_dict(orient="records")}
