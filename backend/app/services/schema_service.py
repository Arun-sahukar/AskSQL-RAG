from typing import List, Dict, Any
from app.database import get_full_schema_info, get_all_tables, get_table_schema
from app.vector_store import index_all_schemas, search_relevant_tables, get_indexed_tables


def refresh_schema_index() -> Dict[str, Any]:
    """Refresh the vector store with current database schema."""
    # Get all schema info from MySQL
    schema_info = get_full_schema_info()

    # Index into Chroma
    tables_indexed = index_all_schemas(schema_info)

    return {
        "success": True,
        "message": f"Successfully indexed {tables_indexed} tables",
        "tables_indexed": tables_indexed
    }


def get_relevant_tables_for_query(question: str, n_results: int = 3) -> List[Dict[str, Any]]:
    """Find tables most relevant to the user's natural language question."""
    return search_relevant_tables(question, n_results)


def get_all_table_info() -> List[Dict[str, Any]]:
    """Get information about all tables in the database."""
    tables = get_all_tables()
    table_info = []

    for table in tables:
        columns = get_table_schema(table)
        table_info.append({
            "table_name": table,
            "columns": [
                {
                    "name": col["Field"],
                    "type": col["Type"],
                    "nullable": col["Null"] == "YES",
                    "key": col["Key"],
                    "default": col["Default"]
                }
                for col in columns
            ]
        })

    return table_info


def get_schema_context_for_llm(question: str) -> str:
    """Get formatted schema context for the LLM prompt."""
    relevant_tables = get_relevant_tables_for_query(question)

    if not relevant_tables:
        # Fallback: get all tables if no relevant ones found
        all_tables = get_all_table_info()
        context = "Available tables:\n"
        for table in all_tables[:5]:  # Limit to first 5 tables
            context += f"\nTable: {table['table_name']}\n"
            context += "Columns: " + ", ".join([c["name"] for c in table["columns"]]) + "\n"
        return context

    context = "Relevant tables for your query:\n"
    for table in relevant_tables:
        context += f"\n{table['schema']}\n"

    return context
