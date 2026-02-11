import React, { useState } from 'react';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';
import { Checkbox } from '../../../components/ui/Checkbox';
import { cn } from '../../../utils/cn';

const AlertCard = ({ alert, selected, onSelect, onDismiss }) => {
  const [expanded, setExpanded] = useState(false);

  const severityConfig = {
    error: {
      icon: 'AlertCircle',
      bgColor: 'bg-red-50',
      borderColor: 'border-red-200',
      textColor: 'text-red-700',
      badgeColor: 'bg-red-100 text-red-800',
      iconColor: 'text-red-500'
    },
    warning: {
      icon: 'AlertTriangle',
      bgColor: 'bg-yellow-50',
      borderColor: 'border-yellow-200',
      textColor: 'text-yellow-700',
      badgeColor: 'bg-yellow-100 text-yellow-800',
      iconColor: 'text-yellow-500'
    },
    info: {
      icon: 'Info',
      bgColor: 'bg-blue-50',
      borderColor: 'border-blue-200',
      textColor: 'text-blue-700',
      badgeColor: 'bg-blue-100 text-blue-800',
      iconColor: 'text-blue-500'
    }
  };

  const typeLabels = {
    connection: 'Connection Failure',
    api: 'API Error',
    request: 'Failed Request',
    system: 'System Warning'
  };

  const config = severityConfig?.[alert?.severity] || severityConfig?.info;

  const formatTimestamp = (date) => {
    const now = new Date();
    const diff = now - date;
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(diff / 3600000);
    const days = Math.floor(diff / 86400000);

    if (minutes < 1) return 'Just now';
    if (minutes < 60) return `${minutes} minute${minutes !== 1 ? 's' : ''} ago`;
    if (hours < 24) return `${hours} hour${hours !== 1 ? 's' : ''} ago`;
    return `${days} day${days !== 1 ? 's' : ''} ago`;
  };

  return (
    <div className={cn(
      'bg-white rounded-lg shadow-sm border-2 transition-all',
      config?.borderColor,
      selected && 'ring-2 ring-orange-500 ring-offset-2'
    )}>
      <div className="p-6">
        <div className="flex items-start gap-4">
          {/* Checkbox */}
          <div className="pt-1">
            <Checkbox
              checked={selected}
              onChange={(e) => onSelect(e?.target?.checked)}
            />
          </div>

          {/* Severity Icon */}
          <div className={cn('p-3 rounded-lg', config?.bgColor)}>
            <Icon name={config?.icon} size={24} className={config?.iconColor} />
          </div>

          {/* Alert Content */}
          <div className="flex-1 min-w-0">
            <div className="flex items-start justify-between gap-4 mb-2">
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <span className={cn('px-2 py-1 text-xs font-semibold rounded', config?.badgeColor)}>
                    {alert?.severity?.toUpperCase()}
                  </span>
                  <span className="px-2 py-1 text-xs font-medium bg-gray-100 text-gray-700 rounded">
                    {typeLabels?.[alert?.type]}
                  </span>
                  <span className="px-2 py-1 text-xs font-medium bg-gray-100 text-gray-700 rounded">
                    {alert?.service}
                  </span>
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-1">
                  {alert?.message}
                </h3>
                <p className="text-sm text-gray-600">
                  {formatTimestamp(alert?.timestamp)}
                </p>
              </div>

              {/* Actions */}
              <div className="flex items-center gap-2">
                <Button
                  variant="ghost"
                  size="sm"
                  iconName={expanded ? 'ChevronUp' : 'ChevronDown'}
                  onClick={() => setExpanded(!expanded)}
                >
                  {expanded ? 'Less' : 'More'}
                </Button>
                <Button
                  variant="destructive"
                  size="sm"
                  iconName="X"
                  onClick={onDismiss}
                >
                  Dismiss
                </Button>
              </div>
            </div>

            {/* Details Preview */}
            <p className="text-sm text-gray-700 mb-3">
              {alert?.details}
            </p>

            {/* Expanded Details */}
            {expanded && (
              <div className={cn('mt-4 p-4 rounded-lg', config?.bgColor)}>
                <h4 className="text-sm font-semibold text-gray-900 mb-2">Full Error Log</h4>
                <pre className="text-xs text-gray-700 bg-white p-3 rounded border border-gray-200 overflow-x-auto mb-4">
                  {`[${alert?.timestamp?.toISOString()}] ${alert?.severity?.toUpperCase()}: ${alert?.service}
${alert?.message}

Details:
${alert?.details}

Type: ${alert?.type}
Service: ${alert?.service}
Severity: ${alert?.severity}
Timestamp: ${alert?.timestamp?.toISOString()}`}
                </pre>

                {alert?.suggestions && alert?.suggestions?.length > 0 && (
                  <div>
                    <h4 className="text-sm font-semibold text-gray-900 mb-2">Suggested Remediation Steps</h4>
                    <ul className="space-y-2">
                      {alert?.suggestions?.map((suggestion, index) => (
                        <li key={index} className="flex items-start gap-2 text-sm text-gray-700">
                          <Icon name="CheckCircle" size={16} className="text-green-500 mt-0.5 flex-shrink-0" />
                          <span>{suggestion}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default AlertCard;