// src/app/promptsummary/page.js
'use client';

import React, { Suspense } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import Image from 'next/image';

// Create a separate component that uses useSearchParams
const PromptSummaryContent = () => {
    const searchParams = useSearchParams();
    const prompt = searchParams.get('prompt') || '';
    const imageFile = searchParams.get('imageFile') || '';

    const router = useRouter();

    const handleEdit = () => {
        router.push(`/upload?prompt=${encodeURIComponent(prompt)}`);
    };

    if (!prompt) {
        return <p>No prompt provided.</p>;
    }

    return (
        <div className="p-4">
            <h2 className="text-2xl font-bold mb-4">Summary</h2>
            <h3 className="text-xl font-semibold mb-2">Your Prompt:</h3>
            <p className="mb-4">{prompt}</p>
            <h3 className="text-xl font-semibold mb-2">Uploaded Image:</h3>
            {imageFile && (
                <Image 
                    src={`/api/placeholder/300/300`} 
                    alt="Uploaded Brand" 
                    width={300}
                    height={300}
                    className="mb-4 max-w-full h-auto"
                />
            )}
            <button 
                onClick={handleEdit}
                className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
            >
                Edit Prompt
            </button>
        </div>
    );
};

// Main component wrapped in Suspense
const PromptSummary = () => {
    return (
        <Suspense fallback={<p>Loading...</p>}>
            <PromptSummaryContent />
        </Suspense>
    );
};

export default PromptSummary;