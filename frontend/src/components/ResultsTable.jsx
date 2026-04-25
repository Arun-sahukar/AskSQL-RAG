function ResultsTable({ results }) {
  if (!results) return null;

  const { columns, rows, row_count } = results;

  if (!columns || !rows) {
    return (
      <div className="results-section">
        <div className="empty-state">
          <p>Query executed successfully</p>
          {results.affected_rows !== undefined && (
            <p>Affected rows: {results.affected_rows}</p>
          )}
        </div>
      </div>
    );
  }

  if (rows.length === 0) {
    return (
      <div className="results-section">
        <div className="results-header">
          <h3>Results</h3>
        </div>
        <div className="empty-state">
          <p>No results found</p>
        </div>
      </div>
    );
  }

  return (
    <div className="results-section">
      <div className="results-header">
        <h3>Results</h3>
        <span className="row-count">{row_count} row{row_count !== 1 ? 's' : ''}</span>
      </div>
      <div className="results-table-wrapper">
        <table className="results-table">
          <thead>
            <tr>
              {columns.map((col) => (
                <th key={col}>{col}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((row, idx) => (
              <tr key={idx}>
                {columns.map((col) => (
                  <td key={col}>
                    {row[col] === null ? (
                      <span style={{ color: '#71717a', fontStyle: 'italic' }}>null</span>
                    ) : (
                      String(row[col])
                    )}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default ResultsTable;
