import React from 'react';
import { CheckCircle, X } from 'lucide-react';

const SuccessMessage = ({ message, onClose }) => {
  if (!message) return null;

  return (
    <div className="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg p-4 mb-4">
      <div className="flex items-start">
        <CheckCircle className="w-5 h-5 text-green-500 mt-0.5 mr-3 flex-shrink-0" />
        <div className="flex-1">
          <p className="text-green-800 dark:text-green-200">{message}</p>
        </div>
        <button
          onClick={onClose}
          className="ml-3 text-green-500 hover:text-green-700 dark:hover:text-green-300"
        >
          <X className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
};

export default SuccessMessage;