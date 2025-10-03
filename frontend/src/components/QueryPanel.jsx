import React, { useState } from 'react';

const QueryPanel = ({ onQuery }) => {
    const [query, setQuery] = useState('');

    const handleQuery = () => {
        if (query.trim()) {
            onQuery(query);
        }
    };

    return (
        <div>
            <h2>3. Ask a Question</h2>
            <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="e.g., How many employees are there?"
                style={{ width: '400px' }}
            />
            <button onClick={handleQuery}>Submit Query</button>
        </div>
    );
};

export default QueryPanel;