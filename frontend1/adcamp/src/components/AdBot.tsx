import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { adGenerationApi } from '../app/services/api';
import { useToast } from './ui/Toast';
import { PencilIcon } from '@heroicons/react/24/solid';

interface AdBotProps {
  onProjectsClick: () => void;
  onAnalyticsClick: () => void;
  onPromptSubmit: (promptText: string) => void;
  onTemplatesReady: (templates: PromptResponse) => void;
}

interface Message {
  text: string;
  isUser: boolean;
  error?: boolean;
}

interface PromptResponse {
  awareness: string;
  leads: string;
  sales: string;
  retention: string;
  social: string;
}

// Update the ToastHook interface to match the actual implementation
interface ToastHook {
  toast: (message: string, type?: 'success' | 'error' | 'info') => void;
  ToastComponent: React.JSX.Element;
}

const AdBot: React.FC<AdBotProps> = ({ 
  onProjectsClick, 
  onAnalyticsClick, 
  onPromptSubmit,
  onTemplatesReady 
}) => {
  const { toast } = useToast() as ToastHook;
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [showPopup, setShowPopup] = useState(false);
  const [templates, setTemplates] = useState<PromptResponse | null>(null);
  const [editingTemplate, setEditingTemplate] = useState<{
    type: keyof PromptResponse;
    text: string;
  } | null>(null);

  const botVariants = {
    float: {
      y: [0, -5, 0],
      transition: {
        duration: 4,
        repeat: Infinity,
        ease: "easeInOut"
      }
    }
  };

  const buttonVariants = {
    hover: { scale: 1.05, transition: { duration: 0.3 } },
    tap: { scale: 0.95 },
    float: {
      y: [0, -3, 0],
      transition: {
        duration: 4,
        repeat: Infinity,
        ease: "easeInOut"
      }
    }
  };

  const handleSendMessage = async () => {
    if (!inputMessage.trim()) return;
    
    setMessages(prev => [...prev, { text: inputMessage, isUser: true }]);
    setInputMessage('');
    setLoading(true);

    try {
      const response = await adGenerationApi.processPrompt(inputMessage.trim());
      console.log('Received response:', response);

      const { awareness, leads, sales, retention, social } = response;

      setTemplates({ awareness, leads, sales, retention, social });
      onTemplatesReady({ awareness, leads, sales, retention, social });

      setMessages(prev => [...prev, {
        text: "✨ Templates generated successfully! Click the button below to view them.",
        isUser: false
      }]);

      toast("Templates Ready: Click to view optimized ad templates", "success");
      onPromptSubmit(inputMessage.trim());
      setShowPopup(true);

    } catch (err) {
      console.error("Error processing prompt:", err);
      setMessages(prev => [...prev, { 
        text: err instanceof Error 
          ? err.message 
          : "There was an error processing your prompt.", 
        isUser: false,
        error: true
      }]);
      
      toast("Failed to process prompt. Please try again.", "error");
    } finally {
      setLoading(false);
    }
  };

  const handleTemplateSelect = (type: keyof PromptResponse) => {
    if (templates) {
      setMessages(prev => [...prev, {
        text: `Selected ${type} template: ${templates[type]}`,
        isUser: false
      }]);
      setShowPopup(false);
    }
  };

  const handleTemplateEdit = (type: keyof PromptResponse) => {
    if (templates) {
      setEditingTemplate({
        type,
        text: templates[type]
      });
    }
  };

  const handleSaveEdit = () => {
    if (editingTemplate && templates) {
      setTemplates({
        ...templates,
        [editingTemplate.type]: editingTemplate.text
      });
      setEditingTemplate(null);
    }
  };

  return (
    <>
      <motion.div
        initial={{ opacity: 0, y: 50 }}
        animate={{ opacity: 1, y: 0 }}
        className="fixed inset-0 flex items-center justify-center z-50"
      >
        <div className="flex items-center space-x-8">
          {/* Projects Button */}
          <motion.button
            variants={buttonVariants}
            whileHover="hover"
            whileTap="tap"
            animate="float"
            onClick={onProjectsClick}
            className="px-8 py-4 bg-gradient-to-r from-purple-500 to-purple-600 text-white text-lg font-bold rounded-full shadow-lg hover:shadow-xl transition-all duration-200"
          >
            Projects
          </motion.button>

          <motion.div
            animate={botVariants.float}
            className="w-96 text-center"
          >
            {/* Holographic Title */}
            <motion.div className="relative mb-4">
              <h2 className="text-xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-cyan-300 filter blur-[0.5px]">
                Let&apos;s save some time
              </h2>
            </motion.div>

            {/* Bot Head */}
            <motion.div 
              className="bg-gradient-to-b from-gray-100 to-gray-200 dark:from-gray-700 dark:to-gray-800 rounded-full p-6 shadow-lg"
            >
              {/* Bot Face */}
              <div className="flex justify-center space-x-4">
                <div className="w-5 h-5 rounded-full bg-blue-400" />
                <div className="w-5 h-5 rounded-full bg-blue-400" />
              </div>
            </motion.div>

            {/* Bot Body with Chatbox */}
            <motion.div 
              className="bg-gray-100 dark:bg-gray-900 rounded-3xl p-6 mt-4 shadow-xl border border-gray-200 dark:border-gray-700"
            >
              <div className="h-64 overflow-y-auto mb-4 text-left">
                {messages.map((message, index) => (
                  <div key={index} className={`mb-2 ${message.isUser ? 'text-right' : 'text-left'}`}>
                    <span className={`inline-block p-2 rounded-lg ${
                      message.isUser 
                        ? 'bg-blue-500 text-white' 
                        : message.error
                          ? 'bg-red-100 text-red-700 dark:bg-red-900 dark:text-red-200'
                          : 'bg-white text-black dark:bg-gray-800 dark:text-white'
                    }`}>
                      {message.text}
                    </span>
                  </div>
                ))}
                {loading && <p>Optimizing your prompt...</p>}
              </div>
              <div className="flex">
                <input
                  type="text"
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                  placeholder="Type your ad idea here..."
                  className="flex-grow p-2 border rounded-l-lg focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white dark:bg-gray-800 dark:border-gray-600 dark:text-white text-black"
                />
                <button
                  onClick={handleSendMessage}
                  disabled={loading}
                  className="px-4 py-2 bg-blue-500 text-white rounded-r-lg hover:bg-blue-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Send
                </button>
              </div>
            </motion.div>
          </motion.div>

          {/* Analytics Button */}
          <motion.button
            variants={buttonVariants}
            whileHover="hover"
            whileTap="tap"
            animate="float"
            onClick={onAnalyticsClick}
            className="px-8 py-4 bg-gradient-to-r from-green-500 to-green-600 text-white text-lg font-bold rounded-full shadow-lg hover:shadow-xl transition-all duration-200"
          >
            Analytics
          </motion.button>
        </div>
      </motion.div>

      <AnimatePresence>
        {showPopup && templates && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
          >
            <motion.div
              initial={{ scale: 0.9 }}
              animate={{ scale: 1 }}
              exit={{ scale: 0.9 }}
              className="bg-gray-900 dark:bg-gray-700 text-white rounded-lg p-6 max-w-2xl w-full max-h-[80vh] overflow-y-auto"
            >
              <h2 className="text-2xl font-bold mb-4">Select a Template</h2>
              {Object.entries(templates).map(([type, text]) => (
                <div key={type} className="mb-4 relative">
                  <h3 className="text-lg font-semibold capitalize">{type}</h3>
                  {editingTemplate?.type === type ? (
                    <div className="flex gap-2">
                      <textarea
                        value={editingTemplate.text}
                        onChange={(e) => setEditingTemplate({
                          ...editingTemplate,
                          text: e.target.value
                        })}
                        className="w-full p-2 text-gray-900 rounded"
                        rows={3}
                      />
                      <button
                        onClick={handleSaveEdit}
                        className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
                      >
                        Save
                      </button>
                    </div>
                  ) : (
                    <>
                      <p className="mb-2">{text}</p>
                      <button
                        onClick={() => handleTemplateSelect(type as keyof PromptResponse)}
                        className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
                      >
                        Select
                      </button>
                      <button
                        onClick={() => handleTemplateEdit(type as keyof PromptResponse)}
                        className="absolute bottom-2 right-2 p-1 bg-gray-600 rounded-full hover:bg-gray-700 transition"
                      >
                        <PencilIcon className="h-5 w-5 text-white" />
                      </button>
                    </>
                  )}
                </div>
              ))}
              <button
                onClick={() => setShowPopup(false)}
                className="mt-4 px-4 py-2 bg-gray-300 text-gray-800 rounded hover:bg-gray-400"
              >
                Close
              </button>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
};

export default AdBot;
