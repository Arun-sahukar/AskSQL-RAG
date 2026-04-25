import { useState } from 'react';

function TableSelector({ tables, onIndexSchemas, isIndexing }) {
  const [expandedTable, setExpandedTable] = useState(null);

  const toggleTable = (tableName) => {
    setExpandedTable(expandedTable === tableName ? null : tableName);
  };

  return (
    <div className="sidebar">
      <div className="table-selector">
        <h3>Available Tables</h3>
        <button
          className="index-btn"
          onClick={onIndexSchemas}
          disabled={isIndexing}
          style={{ marginBottom: '1rem' }}
        >
          {isIndexing ? 'Indexing...' : 'Re-index Schemas'}
        </button>
        {tables.length === 0 ? (
          <div className="empty-state">
            <p>No tables found</p>
            <p style={{ fontSize: '0.8rem', marginTop: '0.5rem' }}>
              Click "Re-index Schemas" after setting up your database
            </p>
          </div>
        ) : (
          <div className="table-list">
            {tables.map((table) => (
              <div
                key={table.table_name}
                className={`table-item ${expandedTable === table.table_name ? 'expanded' : ''}`}
                onClick={() => toggleTable(table.table_name)}
              >
                <div className="table-name">{table.table_name}</div>
                {expandedTable === table.table_name && (
                  <div className="column-list">
                    {table.columns.map((col) => (
                      <div key={col.name} className="column-item">
                        {col.name}
                        <span className="column-type"> ({col.type})</span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default TableSelector;
