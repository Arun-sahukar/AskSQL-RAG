import mysql.connector
from mysql.connector import pooling
from contextlib import contextmanager
from typing import List, Dict, Any, Optional
from app.config import get_settings

settings = get_settings()

# Connection pool for better performance
connection_pool: Optional[pooling.MySQLConnectionPool] = None


def init_connection_pool():
    """Initialize MySQL connection pool."""
    global connection_pool
    connection_pool = pooling.MySQLConnectionPool(
        pool_name="asksql_pool",
        pool_size=5,
        pool_reset_session=True,
        host=settings.mysql_host,
        port=settings.mysql_port,
        user=settings.mysql_user,
        password=settings.mysql_password,
        database=settings.mysql_database,
    )


def get_connection():
    """Get a connection from the pool."""
    global connection_pool
    if connection_pool is None:
        init_connection_pool()
    return connection_pool.get_connection()


@contextmanager
def get_db_cursor():
    """Context manager for database cursor."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        yield cursor
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()


def execute_query(sql: str) -> Dict[str, Any]:
    """Execute a SQL query and return results."""
    with get_db_cursor() as cursor:
        cursor.execute(sql)

        # Check if query returns results
        if cursor.description:
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            return {
                "success": True,
                "columns": columns,
                "rows": rows,
                "row_count": len(rows)
            }
        else:
            return {
                "success": True,
                "message": "Query executed successfully",
                "affected_rows": cursor.rowcount
            }


def get_all_tables() -> List[str]:
    """Get all table names from the database."""
    with get_db_cursor() as cursor:
        cursor.execute("SHOW TABLES")
        tables = [list(row.values())[0] for row in cursor.fetchall()]
        return tables


def get_table_schema(table_name: str) -> List[Dict[str, Any]]:
    """Get schema information for a specific table."""
    with get_db_cursor() as cursor:
        cursor.execute(f"DESCRIBE `{table_name}`")
        return cursor.fetchall()


def get_full_schema_info() -> List[Dict[str, Any]]:
    """Get detailed schema info for all tables including column details."""
    tables = get_all_tables()
    schema_info = []

    for table in tables:
        columns = get_table_schema(table)
        column_details = []

        for col in columns:
            column_details.append({
                "name": col["Field"],
                "type": col["Type"],
                "nullable": col["Null"] == "YES",
                "key": col["Key"],
                "default": col["Default"],
            })

        schema_info.append({
            "table_name": table,
            "columns": column_details,
        })

    return schema_info
