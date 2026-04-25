from typing import Dict, Any, List
from app.agents.sql_agent import generate_sql
from app.database import execute_query
from app.services.schema_service import get_relevant_tables_for_query


def process_question(question: str) -> Dict[str, Any]:
    """
    Process a natural language question:
    1. Retrieve relevant tables (RAG)
    2. Generate SQL using Gemini
    3. Execute query on MySQL
    4. Return formatted results
    """
    # Step 1: Get relevant tables for context
    relevant_tables = get_relevant_tables_for_query(question)
    table_names = [t["table_name"] for t in relevant_tables]

    # Step 2: Generate SQL using LLM
    generation_result = generate_sql(question)

    if not generation_result["success"]:
        return {
            "success": False,
            "question": question,
            "error": generation_result["error"],
            "sql": generation_result.get("sql"),
            "relevant_tables": table_names,
            "results": None
        }

    sql = generation_result["sql"]

    # Step 3: Execute the query
    try:
        results = execute_query(sql)
    except Exception as e:
        return {
            "success": False,
            "question": question,
            "error": f"Query execution failed: {str(e)}",
            "sql": sql,
            "relevant_tables": table_names,
            "results": None
        }

    # Step 4: Return formatted response
    return {
        "success": True,
        "question": question,
        "sql": sql,
        "relevant_tables": table_names,
        "results": results
    }
