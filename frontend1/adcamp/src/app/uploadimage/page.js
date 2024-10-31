'use client';

import React, { useState, Suspense } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import axios from 'axios';

const UploadImageContent = () => {
    const router = useRouter();
    const searchParams = useSearchParams();
    const prompt = searchParams.get('prompt') || '';
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [selectedFile, setSelectedFile] = useState(null);

    const handleFileSelect = (e) => {
        const file = e.target.files[0];
        if (file) {
            setSelectedFile(file);
            setError('');
        }
    };

    const handleImageUpload = async () => {
        if (!selectedFile) {
            setError('Please select an image to upload.');
            return;
        }

        const formData = new FormData();
        formData.append('file', selectedFile);

        try {
            setLoading(true);
            setError('');
            const token = localStorage.getItem('token');
            await axios.post('http://localhost:8000/media-assets/upload/', formData, {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'multipart/form-data'
                }
            });

            router.push(`/promptsummary?prompt=${encodeURIComponent(prompt)}&imageFile=${encodeURIComponent(selectedFile.name)}`);
        } catch (err) {
            console.error('Error uploading image:', err);
            setError('Error uploading image: ' + (err.response?.data?.detail || err.message));
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="p-4 max-w-md mx-auto">
            <h2 className="text-2xl font-bold mb-4">Upload Image</h2>
            <p className="mb-4">{prompt}</p>
            <input
                type="file"
                onChange={handleFileSelect}
                accept="image/*"
                className="mb-4"
            />
            <button 
                onClick={handleImageUpload}
                disabled={loading || !selectedFile}
                className="w-full bg-blue-500 text-white py-2 px-4 rounded disabled:bg-gray-300 mb-4"
            >
                {loading ? 'Uploading...' : 'Upload Image'}
            </button>
            {loading && <p className="text-blue-500">Uploading...</p>}
            {error && <p className="text-red-500">{error}</p>}
        </div>
    );
};

const UploadImage = () => {
    return (
        <Suspense fallback={<div>Loading...</div>}>
            <UploadImageContent />
        </Suspense>
    );
};

export default UploadImage;