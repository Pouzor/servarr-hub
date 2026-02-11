import React from 'react';
import Icon from '../../../components/AppIcon';

const StatusIndicator = ({ status, type }) => {
  const getStatusConfig = () => {
    if (type === 'monitoring') {
      switch (status) {
        case 'monitored':
          return {
            icon: 'Eye',
            label: 'Monitored',
            bgColor: 'bg-success/10',
            textColor: 'text-success',
            iconColor: 'text-success'
          };
        case 'unmonitored':
          return {
            icon: 'EyeOff',
            label: 'Unmonitored',
            bgColor: 'bg-muted',
            textColor: 'text-muted-foreground',
            iconColor: 'text-muted-foreground'
          };
        default:
          return {
            icon: 'HelpCircle',
            label: 'Unknown',
            bgColor: 'bg-muted',
            textColor: 'text-muted-foreground',
            iconColor: 'text-muted-foreground'
          };
      }
    }

    if (type === 'availability') {
      switch (status) {
        case 'available':
          return {
            icon: 'CheckCircle2',
            label: 'Available',
            bgColor: 'bg-success/10',
            textColor: 'text-success',
            iconColor: 'text-success'
          };
        case 'downloading':
          return {
            icon: 'Download',
            label: 'Downloading',
            bgColor: 'bg-warning/10',
            textColor: 'text-warning',
            iconColor: 'text-warning'
          };
        case 'missing':
          return {
            icon: 'AlertCircle',
            label: 'Missing',
            bgColor: 'bg-error/10',
            textColor: 'text-error',
            iconColor: 'text-error'
          };
        default:
          return {
            icon: 'HelpCircle',
            label: 'Unknown',
            bgColor: 'bg-muted',
            textColor: 'text-muted-foreground',
            iconColor: 'text-muted-foreground'
          };
      }
    }

    return {
      icon: 'HelpCircle',
      label: 'Unknown',
      bgColor: 'bg-muted',
      textColor: 'text-muted-foreground',
      iconColor: 'text-muted-foreground'
    };
  };

  const config = getStatusConfig();

  return (
    <div className={`inline-flex items-center gap-1.5 px-2 py-1 rounded-md ${config?.bgColor}`}>
      <Icon name={config?.icon} size={12} className={config?.iconColor} />
      <span className={`text-xs font-medium ${config?.textColor}`}>{config?.label}</span>
    </div>
  );
};

export default StatusIndicator;