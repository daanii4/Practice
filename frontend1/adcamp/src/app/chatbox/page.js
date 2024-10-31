'use client';

import React, { useState, Suspense } from 'react';
import { useRouter } from 'next/navigation';

const ChatboxContent = () => {
    const [userPrompt, setUserPrompt] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const router = useRouter();

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (userPrompt.trim()) {
            setLoading(true);
            // Navigate to the image upload page with the userPrompt passed as query parameters
            router.push(`/upload-image?prompt=${encodeURIComponent(userPrompt.trim())}`);
            setLoading(false); // Reset loading state after navigation
        } else {
            setError('Please enter a prompt before submitting.');
        }
    };

    return (
        <div className="p-4 max-w-md mx-auto">
            <h2 className="text-2xl font-bold mb-4">Ad Prompt Chatbox</h2>
            <form onSubmit={handleSubmit} className="space-y-4">
                <textarea
                    id="userPrompt"
                    name="userPrompt"
                    value={userPrompt}
                    onChange={(e) => setUserPrompt(e.target.value)}
                    placeholder="Type your prompt here..."
                    required
                    disabled={loading}
                    className="w-full p-2 border border-gray-300 rounded"
                    rows="4"
                />
                <button 
                    type="submit" 
                    disabled={loading || !userPrompt.trim()}
                    className="w-full bg-blue-500 text-white py-2 px-4 rounded disabled:bg-gray-300"
                >
                    {loading ? 'Processing...' : 'Submit'}
                </button>
            </form>
            {error && <p className="text-red-500 mt-2">{error}</p>}
        </div>
    );
};

const Chatbox = () => {
    return (
        <Suspense fallback={<div>Loading...</div>}>
            <ChatboxContent />
        </Suspense>
    );
};

export default Chatbox;