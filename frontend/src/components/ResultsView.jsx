import React from 'react';

import { Box, Typography, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Card, CardContent, Grid } from '@mui/material';

// SqlResult component with error handling
const SqlResult = ({ data, sql }) => {
  if (!Array.isArray(data) || data.length === 0) {
    return <Typography color="text.secondary">Query returned no database results.</Typography>;
  }
  return (
    <Box>
      <Typography variant="h6" gutterBottom>Database Results</Typography>
      <Typography variant="body2" sx={{ mb: 1, fontFamily: 'monospace' }}>
        <strong>Generated SQL:</strong> {sql}
      </Typography>
      <TableContainer component={Paper}>
        <Table size="small">
          <TableHead>
            <TableRow>{Object.keys(data[0]).map(key => <TableCell key={key}><strong>{key}</strong></TableCell>)}</TableRow>
          </TableHead>
          <TableBody>
            {data.map((row, i) => <TableRow key={i}>{Object.values(row).map((val, j) => <TableCell key={j}>{String(val)}</TableCell>)}</TableRow>)}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
};

// DocResult component with error handling
const DocResult = ({ data }) => {
  if (!Array.isArray(data) || data.length === 0) {
    return <Typography color="text.secondary">Query returned no document results.</Typography>;
  }
  return (
    <Box>
      <Typography variant="h6" gutterBottom>Document Results</Typography>
      {data.map((item, index) => (
        <Card key={index} sx={{ mb: 2 }}>
          <CardContent>
            <Typography variant="body2">{item.content}</Typography>
          </CardContent>
        </Card>
      ))}
    </Box>
  );
};


const ResultsView = ({ results, responseTime }) => {
  if (!results) return <Typography color="text.secondary">Results will be displayed here.</Typography>;
  if (results.error) return <Typography color="error">{results.error}</Typography>;

  const { answer, type, generated_sql, cached } = results;

  return (
    <Box sx={{ mt: 2 }}>
      <Typography variant="caption" color="text.secondary" sx={{ mr: 2 }}>
        {cached ? 'Cache Hit' : 'Cache Miss'}
      </Typography>
      {responseTime > 0 && <Typography variant="caption" color="text.secondary">Query took {responseTime} ms</Typography>}

      {type === 'DOCUMENT' && <DocResult data={answer} />}

      {type === 'SQL' && <SqlResult data={answer} sql={generated_sql} />}

      {type === 'HYBRID' && (
        <Grid container spacing={4}>
          <Grid item xs={12} md={6}>
            <SqlResult data={answer.sql_results} sql={generated_sql} />
          </Grid>
          <Grid item xs={12} md={6}>
            <DocResult data={answer.doc_results} />
          </Grid>
        </Grid>
      )}
    </Box>
  );
};

export default ResultsView;
