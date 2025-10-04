import React, { useState } from 'react';
import axios from 'axios';
import { Box, Button, Typography, CircularProgress } from '@mui/material';
import UploadFileIcon from '@mui/icons-material/UploadFile';

const DocumentUploader = () => {
    const [files, setFiles] = useState([]);
    const [status, setStatus] = useState({ message: '', error: false });
    const [loading, setLoading] = useState(false);

    const handleFileChange = (e) => {
        setFiles(e.target.files);
        setStatus({ message: `${e.target.files.length} file(s) selected`, error: false });
    };

    const handleUpload = async () => {
        if (files.length === 0) {
            setStatus({ message: 'Please select files to upload.', error: true });
            return;
        }
        setLoading(true);
        setStatus({ message: 'Uploading...', error: false });
        const formData = new FormData();
        for (let i = 0; i < files.length; i++) {
            formData.append('files', files[i]);
        }

        try {
            const response = await axios.post('http://127.0.0.1:8000/api/upload-documents', formData);
            setStatus({ message: `Success: Indexed ${response.data.indexed_files.join(', ')}`, error: false });
        } catch (error) {
            setStatus({ message: 'Upload failed. Please try again.', error: true });
        }
        setLoading(false);
    };

    return (
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <Button
                variant="outlined"
                component="label"
                endIcon={<UploadFileIcon />}
                disabled={loading}
            >
                Choose Files
                <input type="file" multiple hidden onChange={handleFileChange} />
            </Button>
            <Button
                variant="contained"
                onClick={handleUpload}
                disabled={loading || files.length === 0}
                endIcon={loading ? <CircularProgress size={20} color="inherit" /> : null}
            >
                Upload & Index
            </Button>
            <Typography color={status.error ? 'error' : 'text.secondary'}>{status.message}</Typography>
        </Box>
    );
};

export default DocumentUploader;