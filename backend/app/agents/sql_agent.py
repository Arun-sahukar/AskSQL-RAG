import re
from typing import Dict, Any, Tuple
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from app.config import get_settings
from app.services.schema_service import get_schema_context_for_llm

settings = get_settings()

# Initialize Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-pro-latest",
    google_api_key=settings.google_api_key,
    temperature=0,
    convert_system_message_to_human=True
)

# SQL Generation prompt template
SQL_GENERATION_PROMPT = """You are an expert SQL query generator. Your task is to convert natural language questions into valid MySQL queries.

IMPORTANT RULES:
1. Only generate SELECT queries - never generate INSERT, UPDATE, DELETE, DROP, or any data-modifying queries
2. Use proper MySQL syntax
3. Always use backticks for table and column names to handle special characters
4. Return ONLY the SQL query, nothing else - no explanations, no markdown
5. If the question cannot be answered with the given schema, respond with: ERROR: <reason>

DATABASE SCHEMA:
{schema_context}

USER QUESTION: {question}

Generate the SQL query:"""


DANGEROUS_PATTERNS = [
    r'\bDROP\b',
    r'\bDELETE\b',
    r'\bTRUNCATE\b',
    r'\bINSERT\b',
    r'\bUPDATE\b',
    r'\bALTER\b',
    r'\bCREATE\b',
    r'\bGRANT\b',
    r'\bREVOKE\b',
    r'\bEXEC\b',
    r'\bEXECUTE\b',
    r';\s*\w',  # Multiple statements
    r'--',      # SQL comments (could hide malicious code)
    r'/\*',     # Block comments
]


def validate_sql(sql: str) -> Tuple[bool, str]:
    """Validate SQL query for safety."""
    sql_upper = sql.upper()

    for pattern in DANGEROUS_PATTERNS:
        if re.search(pattern, sql_upper, re.IGNORECASE):
            return False, f"Dangerous SQL pattern detected: {pattern}"

    # Must start with SELECT
    if not sql_upper.strip().startswith('SELECT'):
        return False, "Only SELECT queries are allowed"

    return True, "Query is safe"


def generate_sql(question: str) -> Dict[str, Any]:
    """Generate SQL from natural language question using Gemini."""
    # Get relevant schema context
    schema_context = get_schema_context_for_llm(question)

    # Create prompt
    prompt = SQL_GENERATION_PROMPT.format(
        schema_context=schema_context,
        question=question
    )

    # Generate SQL using Gemini
    response = llm.invoke([HumanMessage(content=prompt)])
    generated_sql = response.content.strip()

    # Clean up response (remove markdown code blocks if present)
    if generated_sql.startswith("```"):
        lines = generated_sql.split("\n")
        generated_sql = "\n".join(lines[1:-1] if lines[-1] == "```" else lines[1:])
        generated_sql = generated_sql.strip()

    # Check for error response from LLM
    if generated_sql.upper().startswith("ERROR:"):
        return {
            "success": False,
            "error": generated_sql,
            "sql": None
        }

    # Validate the generated SQL
    is_valid, validation_message = validate_sql(generated_sql)
    if not is_valid:
        return {
            "success": False,
            "error": validation_message,
            "sql": generated_sql
        }

    return {
        "success": True,
        "sql": generated_sql,
        "schema_context": schema_context
    }
