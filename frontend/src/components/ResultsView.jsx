import React from 'react';

const ResultsView = ({ results }) => {
    if (!results) return null;

    // Handle document search results
    if (Array.isArray(results.answer) && results.answer.length > 0 && results.answer[0].source) {
        return (
            <div>
                <h3>Document Results</h3>
                {results.answer.map((item, index) => (
                    <div key={index} style={{ border: '1px solid grey', padding: '10px', margin: '10px' }}>
                        <p><strong>Source:</strong> {item.source}</p>
                        <p>{item.content}</p>
                    </div>
                ))}
            </div>
        );
    }

    // Handle SQL results
    if (Array.isArray(results.answer)) {
        return (
            <div>
                <h3>Database Results</h3>
                <p><strong>Generated SQL:</strong> <code>{results.generated_sql}</code></p>
                {results.answer.length > 0 ? (
                    <table border="1" cellPadding="5">
                        <thead>
                            <tr>{Object.keys(results.answer[0]).map(key => <th key={key}>{key}</th>)}</tr>
                        </thead>
                        <tbody>
                            {results.answer.map((row, i) => <tr key={i}>{Object.values(row).map((val, j) => <td key={j}>{String(val)}</td>)}</tr>)}
                        </tbody>
                    </table>
                ) : <p>Query returned no results.</p>}
            </div>
        );
    }

    return <div><pre>{JSON.stringify(results, null, 2)}</pre></div>;
};

export default ResultsView;