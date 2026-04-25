from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    question: str
    sql: str
    results: Dict[str, Any]
    relevant_tables: List[str]


class TableInfo(BaseModel):
    table_name: str
    columns: List[Dict[str, Any]]


class TablesResponse(BaseModel):
    tables: List[TableInfo]


class IndexResponse(BaseModel):
    success: bool
    message: str
    tables_indexed: int


class HealthResponse(BaseModel):
    status: str
    database: str
    vector_store: str


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
