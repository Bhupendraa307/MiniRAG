import React, { useState, useEffect } from 'react';
import { Activity, AlertCircle } from 'lucide-react';
import { healthCheck } from '../utils/api';

const HealthStatus = () => {
  const [status, setStatus] = useState('checking');
  const [lastCheck, setLastCheck] = useState(null);

  const checkHealth = async () => {
    try {
      await healthCheck();
      setStatus('healthy');
      setLastCheck(new Date().toLocaleTimeString());
    } catch (error) {
      setStatus('error');
      setLastCheck(new Date().toLocaleTimeString());
    }
  };

  useEffect(() => {
    checkHealth();
    const interval = setInterval(checkHealth, 30000); // Check every 30 seconds
    return () => clearInterval(interval);
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

  return (
    <div className="flex items-center space-x-2 text-sm">
      {status === 'healthy' ? (
        <Activity className={`w-4 h-4 ${getStatusColor()}`} />
      ) : (
        <AlertCircle className={`w-4 h-4 ${getStatusColor()}`} />
      )}
      <span className={`${getStatusColor()} font-medium`}>
        {getStatusText()}
      </span>
      {lastCheck && (
        <span className="text-gray-500 dark:text-gray-400 text-xs">
          {lastCheck}
        </span>
      )}
    </div>
  );
};

export default HealthStatus;