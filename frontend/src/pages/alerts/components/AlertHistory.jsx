import React, { useState } from 'react';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';
import Input from '../../../components/ui/Input';
import { cn } from '../../../utils/cn';

const AlertHistory = ({ alerts, onRestore }) => {
  const [searchTerm, setSearchTerm] = useState('');

  const filteredAlerts = alerts?.filter(alert => {
    if (!searchTerm) return true;
    const search = searchTerm?.toLowerCase();
    return (alert?.message?.toLowerCase()?.includes(search) ||
    alert?.service?.toLowerCase()?.includes(search) ||
    alert?.type?.toLowerCase()?.includes(search) || alert?.details?.toLowerCase()?.includes(search));
  });

  const severityConfig = {
    error: {
      icon: 'AlertCircle',
      badgeColor: 'bg-red-100 text-red-800',
      iconColor: 'text-red-500'
    },
    warning: {
      icon: 'AlertTriangle',
      badgeColor: 'bg-yellow-100 text-yellow-800',
      iconColor: 'text-yellow-500'
    },
    info: {
      icon: 'Info',
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

  const formatTimestamp = (date) => {
    return new Date(date)?.toLocaleString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200">
      <div className="p-6 border-b border-gray-200">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-xl font-semibold text-gray-900">Alert History</h2>
            <p className="text-sm text-gray-600 mt-1">
              {alerts?.length} dismissed alert{alerts?.length !== 1 ? 's' : ''}
            </p>
          </div>
        </div>

        <div className="relative">
          <Icon name="Search" size={18} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
          <Input
            placeholder="Search dismissed alerts..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e?.target?.value)}
            className="pl-10"
          />
        </div>
      </div>
      <div className="divide-y divide-gray-200">
        {filteredAlerts?.length === 0 ? (
          <div className="p-12 text-center">
            <Icon name="Archive" size={48} className="mx-auto mb-4 text-gray-400" />
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              {searchTerm ? 'No Results Found' : 'No Dismissed Alerts'}
            </h3>
            <p className="text-gray-600">
              {searchTerm ? 'Try adjusting your search terms' : 'Dismissed alerts will appear here'}
            </p>
          </div>
        ) : (
          filteredAlerts?.map((alert) => {
            const config = severityConfig?.[alert?.severity] || severityConfig?.info;
            
            return (
              <div key={alert?.id} className="p-6 hover:bg-gray-50 transition-colors">
                <div className="flex items-start gap-4">
                  <div className="p-2 rounded-lg bg-gray-100">
                    <Icon name={config?.icon} size={20} className={config?.iconColor} />
                  </div>

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
                        <h3 className="text-base font-semibold text-gray-900 mb-1">
                          {alert?.message}
                        </h3>
                        <p className="text-sm text-gray-600 mb-1">
                          {alert?.details}
                        </p>
                        <div className="flex items-center gap-4 text-xs text-gray-500">
                          <span>Occurred: {formatTimestamp(alert?.timestamp)}</span>
                          {alert?.dismissedAt && (
                            <span>Dismissed: {formatTimestamp(alert?.dismissedAt)}</span>
                          )}
                        </div>
                      </div>

                      <Button
                        variant="outline"
                        size="sm"
                        iconName="RotateCcw"
                        onClick={() => onRestore(alert)}
                      >
                        Restore
                      </Button>
                    </div>
                  </div>
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
};

export default AlertHistory;