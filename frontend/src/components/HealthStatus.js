import React, { useState, useEffect } from 'react';
import { Activity, AlertCircle, RefreshCw } from 'lucide-react';
import { healthCheck } from '../utils/api';

const HealthStatus = () => {
  const [status, setStatus] = useState('checking');
  const [lastCheck, setLastCheck] = useState(null);
  const [isChecking, setIsChecking] = useState(false);

  const checkHealth = async () => {
    setIsChecking(true);
    setStatus('checking');
    try {
      await healthCheck();
      setStatus('healthy');
      setLastCheck(new Date().toLocaleTimeString());
    } catch (error) {
      setStatus('error');
      setLastCheck(new Date().toLocaleTimeString());
    } finally {
      setIsChecking(false);
    }
  };

  useEffect(() => {
    checkHealth();
  }, []);

  const getStatusColor = () => {
    switch (status) {
      case 'healthy': return 'text-green-500';
      case 'error': return 'text-red-500';
      default: return 'text-yellow-500';
    }
  };

  const getStatusText = () => {
    switch (status) {
      case 'healthy': return 'API Online';
      case 'error': return 'API Offline';
      default: return 'Checking...';
    }
  };

  const getIcon = () => {
    if (isChecking) {
      return <RefreshCw className={`w-4 h-4 ${getStatusColor()} animate-spin`} />;
    }
    return status === 'healthy' ? (
      <Activity className={`w-4 h-4 ${getStatusColor()}`} />
    ) : (
      <AlertCircle className={`w-4 h-4 ${getStatusColor()}`} />
    );
  };

  return (
    <button
      onClick={checkHealth}
      disabled={isChecking}
      className="flex items-center space-x-2 text-sm hover:bg-gray-100 dark:hover:bg-gray-700 px-2 py-1 rounded-md transition-colors"
      title="Click to check API health"
    >
      {getIcon()}
      <span className={`${getStatusColor()} font-medium`}>
        {getStatusText()}
      </span>
      {lastCheck && (
        <span className="text-gray-500 dark:text-gray-400 text-xs">
          {lastCheck}
        </span>
      )}
    </button>
  );
};

export default HealthStatus;