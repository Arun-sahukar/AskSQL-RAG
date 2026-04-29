from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.models.schemas import (
    QueryRequest, QueryResponse, TablesResponse, TableInfo,
    IndexResponse, HealthResponse, ErrorResponse
)
from app.services.query_service import process_question
from app.services.schema_service import refresh_schema_index, get_all_table_info
from app.database import get_all_tables
from app.vector_store import get_indexed_tables

app = FastAPI(
    title="AskSQL API",
    description="Convert natural language to SQL queries using RAG and Gemini AI",
    version="1.0.0"
)

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "https://asksql-frontend.onrender.com",
        "https://*.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Check health of database and vector store connections."""
    db_status = "healthy"
    vector_status = "healthy"

    try:
        tables = get_all_tables()
        db_status = f"healthy ({len(tables)} tables)"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"

    try:
        indexed = get_indexed_tables()
        vector_status = f"healthy ({len(indexed)} tables indexed)"
    except Exception as e:
        vector_status = f"unhealthy: {str(e)}"

    return HealthResponse(
        status="ok",
        database=db_status,
        vector_store=vector_status
    )


@app.post("/api/ask")
async def ask_question(request: QueryRequest):
    """
    Main endpoint: Convert natural language question to SQL and execute.

    Flow:
    1. Retrieve relevant tables from Chroma (RAG)
    2. Generate SQL using Gemini AI
    3. Execute query on MySQL
    4. Return results
    """
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    result = process_question(request.question)

    if not result["success"]:
        raise HTTPException(
            status_code=400,
            detail={
                "error": result["error"],
                "sql": result.get("sql"),
                "relevant_tables": result.get("relevant_tables", [])
            }
        )

    return {
        "question": result["question"],
        "sql": result["sql"],
        "results": result["results"],
        "relevant_tables": result["relevant_tables"]
    }


@app.get("/api/tables", response_model=TablesResponse)
async def get_tables():
    """Get all available tables and their schemas."""
    try:
        tables = get_all_table_info()
        return TablesResponse(
            tables=[TableInfo(**table) for table in tables]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/index", response_model=IndexResponse)
async def index_schemas():
    """Re-index all table schemas into the vector store."""
    try:
        result = refresh_schema_index()
        return IndexResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    """Root endpoint with API info."""
    return {
        "name": "AskSQL API",
        "version": "1.0.0",
        "description": "Ask questions in plain English, get SQL queries and results",
        "endpoints": {
            "POST /api/ask": "Ask a question",
            "GET /api/tables": "List all tables",
            "POST /api/index": "Re-index schemas",
            "GET /api/health": "Health check"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
