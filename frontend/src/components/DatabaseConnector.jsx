import React, { useState } from 'react';
import axios from 'axios';

const DatabaseConnector = ({ onSchemaChange }) => {
    const [connectionString, setConnectionString] = useState('sqlite:///company_with_relations.db');
    const [status, setStatus] = useState('');

    const handleConnect = async () => {
        setStatus('Connecting...');
        try {
            const response = await axios.post('http://127.0.0.1:8000/api/connect-database', {
                connection_string: connectionString,
            });
            onSchemaChange(response.data.schema); // Send schema to parent
            setStatus('Connected successfully!');
        } catch (error) {
            setStatus('Connection failed: ' + error.message);
        }
    };

    return (
        <div>
            <h2>1. Connect to Database</h2>
            <input
                type="text"
                value={connectionString}
                onChange={(e) => setConnectionString(e.target.value)}
                placeholder="Enter database connection string"
                style={{ width: '300px' }}
            />
            <button onClick={handleConnect}>Connect & Analyze</button>
            <p>Status: {status}</p>
        </div>
    );
};

export default DatabaseConnector;