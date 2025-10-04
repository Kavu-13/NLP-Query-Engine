import React, { useState } from 'react';
import axios from 'axios';
import { Box, TextField, Button, Typography, CircularProgress } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';

const DatabaseConnector = ({ onSchemaChange }) => {
    const [connectionString, setConnectionString] = useState('sqlite:///company_with_relations.db');
    const [status, setStatus] = useState({ message: '', error: false });
    const [loading, setLoading] = useState(false);

    const handleConnect = async () => {
        setLoading(true);
        setStatus({ message: 'Connecting...', error: false });
        try {
            const response = await axios.post('http://127.0.0.1:8000/api/connect-database', {
                connection_string: connectionString,
            });
            onSchemaChange(response.data.schema);
            setStatus({ message: 'Connected successfully!', error: false });
        } catch (error) {
            setStatus({ message: 'Connection failed. Please check the string and ensure the server is running.', error: true });
        }
        setLoading(false);
    };

    return (
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <TextField
                label="Database Connection String"
                variant="outlined"
                size="small"
                value={connectionString}
                onChange={(e) => setConnectionString(e.target.value)}
                sx={{ flexGrow: 1 }}
                disabled={loading}
            />
            <Button
                variant="contained"
                endIcon={loading ? <CircularProgress size={20} color="inherit" /> : <SendIcon />}
                onClick={handleConnect}
                disabled={loading}
            >
                Connect
            </Button>
            <Typography color={status.error ? 'error' : 'text.secondary'}>{status.message}</Typography>
        </Box>
    );
};

export default DatabaseConnector;