import chromadb
from chromadb.config import Settings as ChromaSettings
from typing import List, Dict, Any
from app.config import get_settings

settings = get_settings()

# Initialize Chroma client with persistence
chroma_client = chromadb.PersistentClient(
    path=settings.chroma_persist_dir
)

# Collection for table schemas
COLLECTION_NAME = "table_schemas"


def get_or_create_collection():
    """Get or create the schema collection."""
    return chroma_client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"description": "Database table schemas for SQL generation"}
    )


def clear_collection():
    """Clear all documents from the collection."""
    try:
        chroma_client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass
    return get_or_create_collection()


def index_table_schema(table_info: Dict[str, Any]) -> None:
    """Index a single table schema into the vector store."""
    collection = get_or_create_collection()

    table_name = table_info["table_name"]
    columns = table_info["columns"]

    # Create a rich text representation of the table schema
    column_descriptions = []
    for col in columns:
        col_desc = f"{col['name']} ({col['type']})"
        if col.get("key") == "PRI":
            col_desc += " PRIMARY KEY"
        if not col.get("nullable", True):
            col_desc += " NOT NULL"
        column_descriptions.append(col_desc)

    schema_text = f"""
Table: {table_name}
Columns: {', '.join([c['name'] for c in columns])}
Schema Details:
{chr(10).join(['- ' + desc for desc in column_descriptions])}
"""

    # Add to collection
    collection.add(
        documents=[schema_text],
        metadatas=[{
            "table_name": table_name,
            "column_count": len(columns),
            "columns": ",".join([c["name"] for c in columns])
        }],
        ids=[f"table_{table_name}"]
    )


def index_all_schemas(schema_info: List[Dict[str, Any]]) -> int:
    """Index all table schemas into the vector store."""
    collection = clear_collection()

    for table_info in schema_info:
        index_table_schema(table_info)

    return len(schema_info)


def search_relevant_tables(query: str, n_results: int = 3) -> List[Dict[str, Any]]:
    """Search for tables relevant to the user's query."""
    collection = get_or_create_collection()

    results = collection.query(
        query_texts=[query],
        n_results=n_results,
        include=["documents", "metadatas"]
    )

    relevant_tables = []
    if results["documents"] and results["documents"][0]:
        for i, doc in enumerate(results["documents"][0]):
            metadata = results["metadatas"][0][i] if results["metadatas"] else {}
            relevant_tables.append({
                "table_name": metadata.get("table_name", "unknown"),
                "schema": doc,
                "columns": metadata.get("columns", "").split(",")
            })

    return relevant_tables


def get_indexed_tables() -> List[str]:
    """Get list of all indexed table names."""
    collection = get_or_create_collection()
    results = collection.get(include=["metadatas"])

    tables = []
    if results["metadatas"]:
        for metadata in results["metadatas"]:
            if "table_name" in metadata:
                tables.append(metadata["table_name"])

    return tables
