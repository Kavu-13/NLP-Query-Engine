import React, { useState, useMemo } from 'react';
import axios from 'axios';

// MUI Imports - Added createTheme
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { CssBaseline, Container, Box, Typography, Divider, Grid, Alert, Paper, IconButton } from '@mui/material';
import Brightness4Icon from '@mui/icons-material/Brightness4'; // Moon icon
import Brightness7Icon from '@mui/icons-material/Brightness7'; // Sun icon

// Component Imports
import DatabaseConnector from './components/DatabaseConnector.jsx';
import DocumentUploader from './components/DocumentUploader.jsx';
import QueryPanel from './components/QueryPanel.jsx';
import ResultsView from './components/ResultsView.jsx';

// --- THEME SETUP ---
const getTheme = (mode) => createTheme({
  palette: {
    mode,
    ...(mode === 'light'
      ? {
        // Palette values for light mode
        primary: {
          main: '#1976d2',
        },
        background: {
          default: '#f4f6f8',
          paper: '#ffffff',
        },
      }
      : {
        // Palette values for dark mode
        primary: {
          main: '#00bcd4',
        },
        background: {
          default: '#121212',
          paper: '#1e1e1e',
        },
        text: {
          primary: '#ffffff',
          secondary: '#b3b3b3',
        },
      }),
  },
  typography: {
    fontFamily: 'Roboto, sans-serif',
  },
});


function App() {
  const [schema, setSchema] = useState(null);
  const [results, setResults] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [themeMode, setThemeMode] = useState('dark');
  const [responseTime, setResponseTime] = useState(0);

  const theme = useMemo(() => getTheme(themeMode), [themeMode]);

  const toggleTheme = () => {
    setThemeMode((prevMode) => (prevMode === 'light' ? 'dark' : 'light'));
  };

  const handleQuery = async (query) => {
    setIsLoading(true);
    setError('');
    setResults(null);

    const startTime = performance.now();

    try {
      const response = await axios.post('http://127.0.0.1:8000/api/query', { query });
      setResults(response.data);
    } catch (error) {
      setError("Query failed. Please ensure the backend server is running and all data is loaded.");
    }
    const endTime = performance.now();
    setResponseTime(Math.round(endTime - startTime));
    setIsLoading(false);
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Typography variant="h3" component="h1" gutterBottom align="center" sx={{ fontWeight: 'bold', flexGrow: 1 }}>
            NLP Query Engine
          </Typography>
          <IconButton sx={{ ml: 1 }} onClick={toggleTheme} color="inherit">
            {theme.palette.mode === 'dark' ? <Brightness7Icon /> : <Brightness4Icon />}
          </IconButton>
        </Box>
        <Divider sx={{ mb: 4 }} />

        <Grid container spacing={4}>
          <Grid item xs={12}>
            <Paper elevation={3} sx={{ p: 3 }}>
              <Typography variant="h5" component="h2" gutterBottom>1. Connect to Database</Typography>
              <DatabaseConnector onSchemaChange={setSchema} />
            </Paper>
          </Grid>

          <Grid item xs={12}>
            <Paper elevation={3} sx={{ p: 3 }}>
              <Typography variant="h5" component="h2" gutterBottom>2. Upload Documents</Typography>
              <DocumentUploader />
            </Paper>
          </Grid>

          <Grid item xs={12}>
            <Paper elevation={3} sx={{ p: 3 }}>
              <Typography variant="h5" component="h2" gutterBottom>3. Ask a Question</Typography>
              <QueryPanel onQuery={handleQuery} isLoading={isLoading} />
            </Paper>
          </Grid>

          <Grid item xs={12}>
            <Paper elevation={3} sx={{ p: 3 }}>
              <Typography variant="h5" component="h2" gutterBottom>Results</Typography>
              {error && <Alert severity="error" sx={{ mt: 2 }}>{error}</Alert>}
              <Box sx={{ mt: 2 }}>
                <ResultsView results={results} responseTime={responseTime} />
              </Box>
            </Paper>
          </Grid>
        </Grid>
      </Container>
    </ThemeProvider>
  );
}

export default App;