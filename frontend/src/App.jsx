import React, { useState } from 'react';
import axios from 'axios';
import DatabaseConnector from './components/DatabaseConnector.jsx';
import DocumentUploader from './components/DocumentUploader.jsx';
import QueryPanel from './components/QueryPanel.jsx';
import ResultsView from './components/ResultsView.jsx';
import './App.css';

function App() {
  const [schema, setSchema] = useState(null);
  const [results, setResults] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleQuery = async (query) => {
    setIsLoading(true);
    setResults(null);
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/query', { query });
      setResults(response.data);
    } catch (error) {
      console.error("Query failed:", error);
      setResults({ error: "Failed to fetch results." });
    }
    setIsLoading(false);
  };

  return (
    <div className="App">
      <h1>NLP Query Engine</h1>
      <DatabaseConnector onSchemaChange={setSchema} />
      <hr />
      <DocumentUploader />
      <hr />
      <QueryPanel onQuery={handleQuery} />
      <hr />
      <h2>Results</h2>
      {isLoading && <p>Loading...</p>}
      <ResultsView results={results} />
    </div>
  );
}

export default App;