import { useState, useEffect } from 'react';
import QueryInput from './components/QueryInput';
import SqlDisplay from './components/SqlDisplay';
import ResultsTable from './components/ResultsTable';
import TableSelector from './components/TableSelector';
import { askQuestion, getTables, indexSchemas } from './services/api';

function App() {
  const [tables, setTables] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isIndexing, setIsIndexing] = useState(false);
  const [error, setError] = useState(null);
  const [queryResult, setQueryResult] = useState(null);

  useEffect(() => {
    fetchTables();
  }, []);

  const fetchTables = async () => {
    try {
      const data = await getTables();
      setTables(data.tables || []);
    } catch (err) {
      console.error('Failed to fetch tables:', err);
    }
  };

  const handleAsk = async (question) => {
    setIsLoading(true);
    setError(null);
    setQueryResult(null);

    try {
      const result = await askQuestion(question);
      setQueryResult(result);
    } catch (err) {
      const errorDetail = err.response?.data?.detail;
      if (typeof errorDetail === 'object') {
        setError(errorDetail.error || 'An error occurred');
        if (errorDetail.sql) {
          setQueryResult({
            sql: errorDetail.sql,
            relevant_tables: errorDetail.relevant_tables || [],
          });
        }
      } else {
        setError(errorDetail || err.message || 'An error occurred');
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleIndexSchemas = async () => {
    setIsIndexing(true);
    try {
      await indexSchemas();
      await fetchTables();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to index schemas');
    } finally {
      setIsIndexing(false);
    }
  };

  return (
    <div className="app">
      <header className="header">
        <h1>AskSQL</h1>
        <p>Ask questions in plain English, get SQL queries and real results</p>
      </header>

      <div className="main-content">
        <div className="query-section">
          <QueryInput onSubmit={handleAsk} isLoading={isLoading} />

          {isLoading && (
            <div className="loading">
              <div className="spinner"></div>
              <span>Generating SQL and fetching results...</span>
            </div>
          )}

          {error && (
            <div className="error">
              <div className="error-title">Error</div>
              <div>{error}</div>
            </div>
          )}

          {queryResult?.sql && (
            <SqlDisplay
              sql={queryResult.sql}
              relevantTables={queryResult.relevant_tables}
            />
          )}

          {queryResult?.results && (
            <ResultsTable results={queryResult.results} />
          )}
        </div>

        <TableSelector
          tables={tables}
          onIndexSchemas={handleIndexSchemas}
          isIndexing={isIndexing}
        />
      </div>
    </div>
  );
}

export default App;
