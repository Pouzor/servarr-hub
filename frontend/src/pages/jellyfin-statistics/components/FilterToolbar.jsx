import React from 'react';
import Select from '../../../components/ui/Select';
import Button from '../../../components/ui/Button';
import Icon from '../../../components/AppIcon';

const FilterToolbar = ({ 
  filters, 
  onFilterChange, 
  onApplyFilters, 
  onResetFilters,
  onExport 
}) => {
  const contentTypeOptions = [
    { value: 'all', label: 'All Content' },
    { value: 'movies', label: 'Movies' },
    { value: 'tv', label: 'TV Shows' },
    { value: 'music', label: 'Music' },
    { value: 'audiobooks', label: 'Audiobooks' }
  ];

  const dateRangeOptions = [
    { value: 'today', label: 'Today' },
    { value: 'yesterday', label: 'Yesterday' },
    { value: 'last7days', label: 'Last 7 Days' },
    { value: 'last30days', label: 'Last 30 Days' },
    { value: 'last90days', label: 'Last 90 Days' },
    { value: 'thisMonth', label: 'This Month' },
    { value: 'lastMonth', label: 'Last Month' },
    { value: 'thisYear', label: 'This Year' },
    { value: 'custom', label: 'Custom Range' }
  ];

  const userOptions = [
    { value: 'all', label: 'All Users' },
    { value: 'john_admin', label: 'John Admin' },
    { value: 'sarah_user', label: 'Sarah User' },
    { value: 'mike_family', label: 'Mike Family' },
    { value: 'emma_guest', label: 'Emma Guest' },
    { value: 'david_power', label: 'David Power' }
  ];

  const deviceTypeOptions = [
    { value: 'all', label: 'All Devices' },
    { value: 'web', label: 'Web Browser' },
    { value: 'mobile', label: 'Mobile App' },
    { value: 'tv', label: 'Smart TV' },
    { value: 'roku', label: 'Roku' },
    { value: 'firetv', label: 'Fire TV' }
  ];

  return (
    <div className="bg-card border border-border rounded-lg p-4 md:p-6 mb-6 md:mb-8">
      <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4 mb-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center">
            <Icon name="Filter" size={20} color="var(--color-primary)" />
          </div>
          <div>
            <h2 className="text-lg md:text-xl font-semibold text-foreground">Advanced Filters</h2>
            <p className="text-xs md:text-sm text-muted-foreground">Refine your analytics view</p>
          </div>
        </div>
        
        <div className="flex flex-wrap gap-2">
          <Button
            variant="outline"
            size="sm"
            onClick={onResetFilters}
            iconName="RotateCcw"
            iconSize={16}
          >
            Reset
          </Button>
          <Button
            variant="default"
            size="sm"
            onClick={onApplyFilters}
            iconName="Search"
            iconSize={16}
          >
            Apply Filters
          </Button>
          <Button
            variant="secondary"
            size="sm"
            onClick={onExport}
            iconName="Download"
            iconSize={16}
          >
            Export
          </Button>
        </div>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Select
          label="Content Type"
          options={contentTypeOptions}
          value={filters?.contentType}
          onChange={(value) => onFilterChange('contentType', value)}
          placeholder="Select content type"
        />

        <Select
          label="Date Range"
          options={dateRangeOptions}
          value={filters?.dateRange}
          onChange={(value) => onFilterChange('dateRange', value)}
          placeholder="Select date range"
        />

        <Select
          label="User"
          options={userOptions}
          value={filters?.user}
          onChange={(value) => onFilterChange('user', value)}
          searchable
          placeholder="Select user"
        />

        <Select
          label="Device Type"
          options={deviceTypeOptions}
          value={filters?.deviceType}
          onChange={(value) => onFilterChange('deviceType', value)}
          placeholder="Select device"
        />
      </div>
      {filters?.dateRange === 'custom' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4 pt-4 border-t border-border">
          <div>
            <label className="block text-sm font-medium text-foreground mb-2">Start Date</label>
            <input
              type="date"
              value={filters?.customStartDate || ''}
              onChange={(e) => onFilterChange('customStartDate', e?.target?.value)}
              className="w-full px-3 py-2 bg-background border border-input rounded-lg text-foreground focus:outline-none focus:ring-2 focus:ring-ring"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-foreground mb-2">End Date</label>
            <input
              type="date"
              value={filters?.customEndDate || ''}
              onChange={(e) => onFilterChange('customEndDate', e?.target?.value)}
              className="w-full px-3 py-2 bg-background border border-input rounded-lg text-foreground focus:outline-none focus:ring-2 focus:ring-ring"
            />
          </div>
        </div>
      )}
    </div>
  );
};

export default FilterToolbar;