import React, { useEffect, useState } from 'react';
import styled from 'styled-components';

const TrackerContainer = styled.div`
  margin-top: 2rem;
  padding: 1rem;
  background-color: #fff8e1;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
`;

const ProgressTracker = ({ wsUrl }) => {
  const [status, setStatus] = useState("Connecting...");
  const [steps, setSteps] = useState([]);
  const [error, setError] = useState(''); // State for error messages

  useEffect(() => {
    const socket = new WebSocket(wsUrl);

    socket.onopen = () => {
      setStatus("Connected");
    };

    socket.onmessage = (event) => {
      const message = JSON.parse(event.data);
      setSteps((prevSteps) => [...prevSteps, message]);
    };

    socket.onerror = () => {
      setError("Error connecting to server."); // Set error message here
      setStatus("Error connecting to server.");
    };

    socket.onclose = () => {
      setStatus("Disconnected");
    };

    return () => socket.close();
  }, [wsUrl]);

  return (
    <TrackerContainer>
      <h3>Status: {status}</h3>
      {error && <p className="text-red-500">{error}</p>} {/* Display error if it exists */}
      <ul>
        {steps.map((step, index) => (
          <li key={index}>
            {step.status === 'completed' ? '✅' : step.status === 'error' ? '❌' : '⏳'}
            {step.message}
          </li>
        ))}
      </ul>
    </TrackerContainer>
  );
};

export default ProgressTracker;
