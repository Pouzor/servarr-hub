import React from 'react';

import Select from '../../../components/ui/Select';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';

const FilterToolbar = ({ searchQuery, onSearchChange, filters, onFilterChange, totalResults }) => {
  const contentTypeOptions = [
    { label: 'All Content', value: 'all' },
    { label: 'Movies', value: 'movie' },
    { label: 'TV Shows', value: 'tv' }
  ];

  const qualityOptions = [
    { label: 'All Qualities', value: 'all' },
    { label: '4K', value: '4K' },
    { label: '1080p', value: '1080p' },
    { label: '720p', value: '720p' }
  ];

  const sortOptions = [
    { label: 'Added Date', value: 'added_date' },
    { label: 'Ratio', value: 'ratio' },
    { label: 'File Size', value: 'size' },
    { label: 'Title', value: 'title' }
  ];

  const orderOptions = [
    { label: 'Descending', value: 'desc' },
    { label: 'Ascending', value: 'asc' }
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
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-4">
        <Select
          options={contentTypeOptions}
          value={filters?.contentType}
          onChange={(value) => onFilterChange('contentType', value)}
          placeholder="Content Type"
        />
        
        <Select
          options={qualityOptions}
          value={filters?.quality}
          onChange={(value) => onFilterChange('quality', value)}
          placeholder="Quality"
        />
        
        <Select
          options={sortOptions}
          value={filters?.sortBy}
          onChange={(value) => onFilterChange('sortBy', value)}
          placeholder="Sort By"
        />
        
        <Select
          options={orderOptions}
          value={filters?.order}
          onChange={(value) => onFilterChange('order', value)}
          placeholder="Order"
        />
      </div>

      {/* Results Count */}
      <div className="flex items-center justify-between text-sm">
        <p className="text-muted-foreground">
          Showing <span className="font-semibold text-foreground">{totalResults}</span> {totalResults === 1 ? 'item' : 'items'}
        </p>
        
        {(searchQuery || filters?.contentType !== 'all' || filters?.quality !== 'all') && (
          <Button
            variant="ghost"
            size="sm"
            iconName="X"
            onClick={() => {
              onSearchChange('');
              onFilterChange('contentType', 'all');
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