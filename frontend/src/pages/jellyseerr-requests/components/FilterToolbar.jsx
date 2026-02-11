import React from 'react';
import Select from '../../../components/ui/Select';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';

const FilterToolbar = ({ searchQuery, onSearchChange, filters, onFilterChange, totalResults, uniqueUsers }) => {
  const statusOptions = [
    { label: 'All Status', value: 'all' },
    { label: 'Pending', value: 'pending' },
    { label: 'Approved', value: 'approved' },
    { label: 'Processing', value: 'processing' },
    { label: 'Declined', value: 'declined' },
    { label: 'Available', value: 'available' }
  ];

  const typeOptions = [
    { label: 'All Types', value: 'all' },
    { label: 'Movies', value: 'movie' },
    { label: 'TV Shows', value: 'tv' }
  ];

  const userOptions = uniqueUsers?.map(user => ({
    label: user === 'all' ? 'All Users' : user,
    value: user
  }));

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
            placeholder="Search requests by title..."
            value={searchQuery}
            onChange={(e) => onSearchChange(e?.target?.value)}
            className="w-full h-10 pl-10 pr-4 rounded-md border border-input bg-background text-foreground text-sm placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
          />
        </div>
      </div>

      {/* Filters Row */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mb-4">
        <Select
          options={statusOptions}
          value={filters?.status}
          onChange={(value) => onFilterChange('status', value)}
          placeholder="Status"
        />
        
        <Select
          options={typeOptions}
          value={filters?.type}
          onChange={(value) => onFilterChange('type', value)}
          placeholder="Request Type"
        />
        
        <Select
          options={userOptions}
          value={filters?.user}
          onChange={(value) => onFilterChange('user', value)}
          placeholder="Requested By"
        />
      </div>

      {/* Results Count */}
      <div className="flex items-center justify-between text-sm">
        <p className="text-muted-foreground">
          Showing <span className="font-semibold text-foreground">{totalResults}</span> {totalResults === 1 ? 'request' : 'requests'}
        </p>
        
        {(searchQuery || filters?.status !== 'all' || filters?.type !== 'all' || filters?.user !== 'all') && (
          <Button
            variant="ghost"
            size="sm"
            iconName="X"
            onClick={() => {
              onSearchChange('');
              onFilterChange('status', 'all');
              onFilterChange('type', 'all');
              onFilterChange('user', 'all');
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