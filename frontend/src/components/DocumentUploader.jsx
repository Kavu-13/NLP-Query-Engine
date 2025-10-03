import React, { useState } from 'react';
import axios from 'axios';

const DocumentUploader = () => {
    const [files, setFiles] = useState([]);
    const [status, setStatus] = useState('');

    const handleFileChange = (e) => {
        setFiles(e.target.files);
    };

    const handleUpload = async () => {
        if (files.length === 0) {
            setStatus('Please select files to upload.');
            return;
        }
        setStatus('Uploading...');
        const formData = new FormData();
        for (let i = 0; i < files.length; i++) {
            formData.append('files', files[i]);
        }

        try {
            const response = await axios.post('http://127.0.0.1:8000/api/upload-documents', formData, {
                headers: { 'Content-Type': 'multipart/form-data' },
            });
            setStatus(`Successfully indexed: ${response.data.indexed_files.join(', ')}`);
        } catch (error) {
            setStatus('Upload failed: ' + error.message);
        }
    };

    return (
        <div>
            <h2>2. Upload Documents</h2>
            <input type="file" multiple onChange={handleFileChange} />
            <button onClick={handleUpload}>Upload & Index</button>
            <p>Status: {status}</p>
        </div>
    );
};

export default DocumentUploader;