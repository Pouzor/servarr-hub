import React from 'react';
import Select from '../../../components/ui/Select';
import Button from '../../../components/ui/Button';

const FilterToolbar = ({ filters, onFilterChange }) => {
  const dateRangeOptions = [
    { label: 'All Time', value: 'all' },
    { label: 'Last Hour', value: '1h' },
    { label: 'Last 24 Hours', value: '24h' },
    { label: 'Last 7 Days', value: '7d' },
    { label: 'Last 30 Days', value: '30d' }
  ];

  const serviceOptions = [
    { label: 'All Services', value: 'all' },
    { label: 'Radarr', value: 'Radarr' },
    { label: 'Sonarr', value: 'Sonarr' },
    { label: 'Jellyfin', value: 'Jellyfin' },
    { label: 'Jellyseerr', value: 'Jellyseerr' }
  ];

  const severityOptions = [
    { label: 'All Severities', value: 'all' },
    { label: 'Error', value: 'error' },
    { label: 'Warning', value: 'warning' },
    { label: 'Info', value: 'info' }
  ];

  const handleReset = () => {
    onFilterChange({
      dateRange: 'all',
      service: 'all',
      severity: 'all',
      status: 'active'
    });
  };

  const hasActiveFilters = filters?.dateRange !== 'all' || filters?.service !== 'all' || filters?.severity !== 'all';

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 mb-6">
      <div className="flex flex-wrap items-end gap-4">
        <div className="flex-1 min-w-[200px]">
          <Select
            label="Date Range"
            options={dateRangeOptions}
            value={filters?.dateRange}
            onChange={(value) => onFilterChange({ ...filters, dateRange: value })}
          />
        </div>

        <div className="flex-1 min-w-[200px]">
          <Select
            label="Service"
            options={serviceOptions}
            value={filters?.service}
            onChange={(value) => onFilterChange({ ...filters, service: value })}
          />
        </div>

        <div className="flex-1 min-w-[200px]">
          <Select
            label="Severity"
            options={severityOptions}
            value={filters?.severity}
            onChange={(value) => onFilterChange({ ...filters, severity: value })}
          />
        </div>

        {hasActiveFilters && (
          <Button
            variant="outline"
            iconName="RotateCcw"
            onClick={handleReset}
          >
            Reset Filters
          </Button>
        )}
      </div>
    </div>
  );
};

export default FilterToolbar;