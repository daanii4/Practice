import React from 'react';
import styled from 'styled-components';

const PreviewContainer = styled.div`
  background-color: #ff7043;
  padding: 2rem;
  border-radius: 10px;
  color: white;
  max-width: 600px;
  margin: 2rem auto;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
`;

const AdPreview = ({ adData, onEdit }) => {
  return (
    <PreviewContainer>
      <h2>Ad Preview</h2>
      <p><strong>Product:</strong> {adData.product}</p>
      <p><strong>Target Audience:</strong> {adData.targetAudience}</p>
      <p><strong>Ad Goal:</strong> {adData.adGoal}</p>
      <p><strong>Top Feature:</strong> {adData.topFeature}</p>
      <p><strong>Call to Action:</strong> {adData.callToAction}</p>
      <button onClick={onEdit}>Edit Ad</button>
    </PreviewContainer>
  );
};

export default AdPreview;
