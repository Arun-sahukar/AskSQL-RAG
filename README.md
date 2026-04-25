# AskSQL

Ask questions in plain English, get SQL queries and real results from your database.

## Features

- **Natural Language to SQL**: Ask questions like "Show me all customers from New York"
- **RAG-Powered**: Uses Chroma vector database to find relevant tables
- **Safe Queries**: Only SELECT queries allowed, dangerous operations blocked
- **Real Results**: Executes queries on MySQL and returns actual data

## Tech Stack

- **Backend**: Python, FastAPI, LangChain
- **LLM**: Google Gemini AI
- **Vector DB**: Chroma
- **Database**: MySQL
- **Frontend**: React, Vite

## Setup

### Prerequisites

- Python 3.10+
- Node.js 18+
- MySQL 8.0+
- Google Gemini API key

### 1. Clone and Setup Database

```bash
# Create the sample database
mysql -u root -p < scripts/setup_sample_db.sql
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your credentials
```

Edit `.env` file:
```
GOOGLE_API_KEY=your_gemini_api_key
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_mysql_password
MYSQL_DATABASE=asksql_demo
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install
```

### 4. Run the Application

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### 5. Index Database Schemas

Open http://localhost:5173 and click "Re-index Schemas" to index your database tables.

## Usage

1. Type a question in plain English
2. AskSQL finds relevant tables using RAG
3. Gemini AI generates the SQL query
4. Query executes on MySQL
5. Results display in the browser

### Example Questions

- "Show me all customers from New York"
- "What are the top 5 products by price?"
- "How many orders were placed in January 2024?"
- "List all products in the Electronics category"
- "What is the total revenue from delivered orders?"

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/ask` | POST | Convert question to SQL and execute |
| `/api/tables` | GET | List all database tables |
| `/api/index` | POST | Re-index table schemas |
| `/api/health` | GET | Health check |

## How It Works

```
User Question
     |
     v
┌─────────────────┐
│ 1. Retrieve     │ ← Chroma finds relevant tables
│    Tables (RAG) │
└────────┬────────┘
         |
         v
┌─────────────────┐
│ 2. Generate SQL │ ← Gemini creates SQL with schema context
│    (Gemini AI)  │
└────────┬────────┘
         |
         v
┌─────────────────┐
│ 3. Validate &   │ ← Check for dangerous operations
│    Execute      │
└────────┬────────┘
         |
         v
┌─────────────────┐
│ 4. Return       │ ← Format and display results
│    Results      │
└─────────────────┘
```

## License

MIT
