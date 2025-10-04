import React, { useState } from 'react';
import { Box, TextField, Button } from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';

const QueryPanel = ({ onQuery, isLoading }) => {
  const [query, setQuery] = useState('');

  const handleQuery = () => {
    if (query.trim()) {
      onQuery(query);
    }
  };

  return (
    <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
      <TextField
        label="Ask a Question"
        variant="outlined"
        size="small"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="e.g., How many employees are there?"
        fullWidth
        disabled={isLoading}
      />
      <Button
        variant="contained"
        onClick={handleQuery}
        disabled={isLoading}
        endIcon={<SearchIcon />}
      >
        Submit
      </Button>
    </Box>
  );
};

export default QueryPanel;