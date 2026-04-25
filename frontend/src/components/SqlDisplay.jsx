import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';

function SqlDisplay({ sql, relevantTables }) {
  if (!sql) return null;

  return (
    <div className="sql-display">
      <h3>Generated SQL</h3>
      <div className="sql-code">
        <SyntaxHighlighter
          language="sql"
          style={vscDarkPlus}
          customStyle={{
            background: 'transparent',
            fontSize: '0.9rem',
          }}
        >
          {sql}
        </SyntaxHighlighter>
      </div>
      {relevantTables && relevantTables.length > 0 && (
        <div className="relevant-tables">
          {relevantTables.map((table) => (
            <span key={table} className="table-badge">
              {table}
            </span>
          ))}
        </div>
      )}
    </div>
  );
}

export default SqlDisplay;
