import { useState } from 'react';

function QueryInput({ onSubmit, isLoading }) {
  const [question, setQuestion] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (question.trim() && !isLoading) {
      onSubmit(question);
    }
  };

  return (
    <div className="query-input-container">
      <form className="query-form" onSubmit={handleSubmit}>
        <input
          type="text"
          className="query-input"
          placeholder="Ask a question about your data... (e.g., 'Show me all customers from New York')"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          disabled={isLoading}
        />
        <button
          type="submit"
          className="submit-btn"
          disabled={isLoading || !question.trim()}
        >
          {isLoading ? 'Thinking...' : 'Ask'}
        </button>
      </form>
    </div>
  );
}

export default QueryInput;
