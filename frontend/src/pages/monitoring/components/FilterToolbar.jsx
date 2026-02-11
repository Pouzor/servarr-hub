import React from 'react';
import Select from '../../../components/ui/Select';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';

const FilterToolbar = ({ searchQuery, onSearchChange, filters, onFilterChange, totalResults }) => {
  const serviceOptions = [
    { label: 'All Services', value: 'all' },
    { label: 'Sonarr (TV Shows)', value: 'sonarr' },
    { label: 'Radarr (Movies)', value: 'radarr' }
  ];

  const statusOptions = [
    { label: 'All Status', value: 'all' },
    { label: 'Monitored', value: 'monitored' },
    { label: 'Unmonitored', value: 'unmonitored' },
    { label: 'Available', value: 'available' },
    { label: 'Missing', value: 'missing' },
    { label: 'Downloading', value: 'downloading' }
  ];

  const qualityOptions = [
    { label: 'All Qualities', value: 'all' },
    { label: '4K', value: '4K' },
    { label: '1080p', value: '1080p' },
    { label: '720p', value: '720p' },
    { label: 'SD', value: 'SD' }
  ];

  return (
    <div className="bg-card border border-border rounded-lg p-4 md:p-6 mb-6">
      {/* Search Bar */}
      <div className="mb-4">
        <div className="relative">
          <Icon 
            name="Search" 
            size={18} 
            className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground" 
          />
          <input
            type="text"
            placeholder="Search media by title..."
            value={searchQuery}
            onChange={(e) => onSearchChange(e?.target?.value)}
            className="w-full h-10 pl-10 pr-4 rounded-md border border-input bg-background text-foreground text-sm placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
          />
        </div>
      </div>

      {/* Filters Row */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mb-4">
        <Select
          options={serviceOptions}
          value={filters?.service}
          onChange={(value) => onFilterChange('service', value)}
          placeholder="Service"
        />
        
        <Select
          options={statusOptions}
          value={filters?.status}
          onChange={(value) => onFilterChange('status', value)}
          placeholder="Status"
        />
        
        <Select
          options={qualityOptions}
          value={filters?.quality}
          onChange={(value) => onFilterChange('quality', value)}
          placeholder="Quality Profile"
        />
      </div>

      {/* Results Count */}
      <div className="flex items-center justify-between text-sm">
        <p className="text-muted-foreground">
          Showing <span className="font-semibold text-foreground">{totalResults}</span> {totalResults === 1 ? 'item' : 'items'}
        </p>
        
        {(searchQuery || filters?.service !== 'all' || filters?.status !== 'all' || filters?.quality !== 'all') && (
          <Button
            variant="ghost"
            size="sm"
            iconName="X"
            onClick={() => {
              onSearchChange('');
              onFilterChange('service', 'all');
              onFilterChange('status', 'all');
              onFilterChange('quality', 'all');
            }}
          >
            Clear Filters
          </Button>
        )}
      </div>
    </div>
  );
};

export default FilterToolbar;