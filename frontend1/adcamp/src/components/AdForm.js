import React, { useState } from 'react';
import styled from 'styled-components';  // Correct import

// Define the styled Form component
const Form = styled.form`
  display: flex;
  flex-direction: column;
  gap: 1rem;
`;

const AdForm = ({ onGenerateAd }) => {
  const [formData, setFormData] = useState({
    product: '',
    targetAudience: '',
    adGoal: '',
    topFeature: '',
    callToAction: ''
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onGenerateAd(formData);  // Callback to parent with form data
  };

  return (
    <Form onSubmit={handleSubmit}>  {/* Use the styled Form component here */}
      <label>Product/Service</label>
      <input type="text" name="product" onChange={handleChange} required />

      <label>Target Audience</label>
      <input type="text" name="targetAudience" onChange={handleChange} required />

      <label>Ad Goal</label>
      <input type="text" name="adGoal" onChange={handleChange} required />

      <label>Top Feature/Benefit</label>
      <input type="text" name="topFeature" onChange={handleChange} required />

      <label>Call to Action</label>
      <input type="text" name="callToAction" onChange={handleChange} required />

      <button type="submit">Generate Ad</button>
    </Form>
  );
};

export default AdForm;
