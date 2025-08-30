import React, { useState } from 'react';
import ThemeToggle from './components/ThemeToggle';
import FileUpload from './components/FileUpload';
import QueryInterface from './components/QueryInterface';
import ErrorMessage from './components/ErrorMessage';
import SuccessMessage from './components/SuccessMessage';
import { Brain } from 'lucide-react';

function App() {
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleUploadSuccess = (result) => {
    setSuccess(`Document "${result.filename}" uploaded successfully!`);
    setError('');
  };

  const handleError = (errorMessage) => {
    setError(errorMessage);
    setSuccess('');
  };

  const clearMessages = () => {
    setError('');
    setSuccess('');
  };

  return (
    <div className="min-h-screen bg-gray-100 dark:bg-gray-900 transition-colors">
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center space-x-3">
            <Brain className="w-8 h-8 text-blue-600" />
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
              Mini RAG
            </h1>
          </div>
          <ThemeToggle />
        </div>

        {/* Messages */}
        <ErrorMessage message={error} onClose={clearMessages} />
        <SuccessMessage message={success} onClose={clearMessages} />

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <FileUpload 
            onUploadSuccess={handleUploadSuccess}
            onError={handleError}
          />
          <QueryInterface 
            onError={handleError}
          />
        </div>

        {/* Footer */}
        <footer className="mt-12 text-center text-gray-500 dark:text-gray-400">
          <p>Mini RAG - Retrieval-Augmented Generation with Vector Search</p>
        </footer>
      </div>
    </div>
  );
}

export default App;