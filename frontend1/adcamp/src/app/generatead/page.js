'use client'; 

import React, { useState } from 'react';
import AdForm from '../../components/AdForm'; // Adjust the import path based on your structure
import ProgressTracker from '../../components/ProgressTracker'; // Adjust the import path based on your structure
import AdPreview from '../../components/AdPreview'; // Adjust the import path based on your structure
import { adGenerationApi } from '../services/api'; // Adjust the import path based on your structure
import styled from 'styled-components';
import { useRouter } from 'next/navigation';

const GenerateAdContainer = styled.div`
  padding: 2rem;
  text-align: center;
`;

const GenerateAd = () => {
  const [adData, setAdData] = useState(null);
  const [progressUrl] = useState("ws://127.0.0.1:8000/ws/progress");
  const router = useRouter(); // Using Next.js router

  const handleGenerateAd = async (formData) => {
    try {
      const result = await adGenerationApi.generateAd(formData);
      setAdData(result.data);
    } catch (error) {
      console.error("Error generating ad:", error);
      alert("Failed to generate ad. Please try again.");
    }
  };

  const handleEditAd = () => {
    if (adData && adData.id) {
      router.push(`/edit-ad/${adData.id}`); // Navigate to the EditAd page with the ad ID
    }
  };

  return (
    <GenerateAdContainer>
      {!adData ? (
        <>
          <h1>Create Your Ad Campaign</h1>
          <AdForm onGenerateAd={handleGenerateAd} />
          <ProgressTracker wsUrl={progressUrl} />
        </>
      ) : (
        <div>
          <h2>Ad Successfully Generated</h2>
          <AdPreview adData={adData} onEdit={handleEditAd} />
          {/* Add button to post to Facebook if needed */}
        </div>
      )}
    </GenerateAdContainer>
  );
};

export default GenerateAd;
