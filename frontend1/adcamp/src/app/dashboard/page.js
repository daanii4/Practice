'use client';

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { adGenerationApi } from '../services/api';
import AdBot from '../../components/AdBot';
import Toast from '../../components/ui/Toast';

export default function Dashboard() {
  const [showProjects, setShowProjects] = useState(false);
  const [showAnalytics, setShowAnalytics] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [toastMessage, setToastMessage] = useState('');
  const [toastType, setToastType] = useState('info');
  const [showToast, setShowToast] = useState(false);

  const handlePromptSubmit = async (promptText) => {
    setIsLoading(true);
    try {
      await adGenerationApi.processPrompt(promptText.trim());
      setToastMessage('Templates generated successfully');
      setToastType('success');
      setShowToast(true);
    } catch (error) {
      console.error('Failed to process prompt:', error);
      setToastMessage('Failed to generate templates');
      setToastType('error');
      setShowToast(true);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="relative min-h-screen bg-gray-900 text-white p-8">
      {isLoading && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
        </div>
      )}

      <Toast
        message={toastMessage}
        type={toastType}
        isVisible={showToast}
        onClose={() => setShowToast(false)}
      />

      <AdBot
        onProjectsClick={() => { setShowProjects(true); setShowAnalytics(false); }}
        onAnalyticsClick={() => { setShowAnalytics(true); setShowProjects(false); }}
        onPromptSubmit={handlePromptSubmit}
        onTemplatesReady={(templates) => {
          console.log('Templates received:', templates);
        }}
      />

      {/* Projects and Analytics Overlays */}
      <AnimatePresence>
        {showProjects && (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50"
            onClick={() => setShowProjects(false)}
          >
            <motion.div
              className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 
                         bg-gray-800 rounded-2xl p-8 w-11/12 max-w-4xl max-h-[80vh] 
                         overflow-auto shadow-2xl"
              onClick={(e) => e.stopPropagation()}
            >
              <h2 className="text-2xl font-bold mb-6">Your Projects</h2>
              {/* Projects Content */}
            </motion.div>
          </motion.div>
        )}

        {showAnalytics && (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50"
            onClick={() => setShowAnalytics(false)}
          >
            <motion.div
              className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 
                         bg-gray-800 rounded-2xl p-8 w-11/12 max-w-4xl max-h-[80vh] 
                         overflow-auto shadow-2xl"
              onClick={(e) => e.stopPropagation()}
            >
              <h2 className="text-2xl font-bold mb-6">Campaign Analytics</h2>
              <p className="text-gray-400">
                Analytics data will be displayed here.
              </p>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
