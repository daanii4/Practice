// services/api.js
import axios from 'axios';

// Create an axios instance with default config
const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

console.log('API URL:', process.env.NEXT_PUBLIC_API_URL);

// Add request interceptor for handling tokens, etc.
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor for handling errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Handle different error cases
    if (error.response) {
      // Server responded with error status
      console.error('Server Error:', error.response.data);
    } else if (error.request) {
      // Request made but no response received
      console.error('Network Error:', error.request);
    } else {
      // Error in request setup
      console.error('Request Error:', error.message);
    }
    return Promise.reject(error);
  }
);

// Add TypeScript interface
/**
 * @typedef {Object} ProcessPromptResponse
 * @property {Object} data
 * @property {string[]} data.variations
 */

// API endpoints
export const adGenerationApi = {
  processPrompt: async (prompt) => {
    try {
      const response = await api.post(`/ad-generation/process_prompt/?prompt=${encodeURIComponent(prompt)}`);

      console.log('API Response:', response);
      
      if (!response || !response.data) {
        throw new Error('Invalid response from server');
      }
      
      return response.data;
    } catch (error) {
      console.error('API Error:', error);
      if (error.response?.data?.detail) {
        throw new Error(error.response.data.detail);
      }
      throw error;
    }
  },
  
  sendOptimizedPrompt: (promptData) =>
    api.post('/ad-generation/optimizedprompt', promptData),
    
  getAnalytics: (projectId) =>
    api.get(`/analytics/${projectId}/`),

  fetchAdDetails: (adId) =>
    api.get(`/ads/${adId}`).then(response => response.data),
    
  saveAdChanges: (adId, adData) =>
    api.put(`/ads/${adId}`, adData).then(response => response.data),
};

export const { 
  fetchAdDetails, 
  saveAdChanges,
  processPrompt,
  sendOptimizedPrompt,
  getAnalytics 
} = adGenerationApi;

export default api;
