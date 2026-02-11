import React, { useState, useMemo } from 'react';
import Header from '../../components/navigation/Header';
import Icon from '../../components/AppIcon';
import FilterToolbar from './components/FilterToolbar';
import MonitoringTable from './components/MonitoringTable';
import Button from '../../components/ui/Button';

const Monitoring = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [filters, setFilters] = useState({
    service: 'all',
    status: 'all',
    quality: 'all'
  });
  const [selectedItems, setSelectedItems] = useState([]);

  // Mock data for monitored media
  const mockMonitoringData = [
    {
      id: '1',
      title: 'Breaking Bad',
      service: 'sonarr',
      monitoringStatus: 'monitored',
      availabilityStatus: 'available',
      qualityProfile: 'HD-1080p',
      lastUpdated: '2026-02-09T14:30:00',
      seasons: [
        { number: 1, episodes: 7, monitored: 7, available: 7 },
        { number: 2, episodes: 13, monitored: 13, available: 13 },
        { number: 3, episodes: 13, monitored: 13, available: 13 },
        { number: 4, episodes: 13, monitored: 13, available: 13 },
        { number: 5, episodes: 16, monitored: 16, available: 16 }
      ],
      filePath: '/media/tv/Breaking Bad',
      downloadHistory: [
        { date: '2026-02-01', action: 'Downloaded S05E16', quality: '1080p' },
        { date: '2026-01-25', action: 'Downloaded S05E15', quality: '1080p' }
      ]
    },
    {
      id: '2',
      title: 'The Dark Knight',
      service: 'radarr',
      monitoringStatus: 'monitored',
      availabilityStatus: 'available',
      qualityProfile: '4K',
      lastUpdated: '2026-02-08T10:15:00',
      year: 2008,
      filePath: '/media/movies/The Dark Knight (2008)',
      fileSize: '45.2 GB',
      downloadHistory: [
        { date: '2026-02-08', action: 'Downloaded', quality: '4K' }
      ]
    },
    {
      id: '3',
      title: 'Stranger Things',
      service: 'sonarr',
      monitoringStatus: 'monitored',
      availabilityStatus: 'missing',
      qualityProfile: 'HD-1080p',
      lastUpdated: '2026-02-09T18:45:00',
      seasons: [
        { number: 1, episodes: 8, monitored: 8, available: 8 },
        { number: 2, episodes: 9, monitored: 9, available: 9 },
        { number: 3, episodes: 8, monitored: 8, available: 8 },
        { number: 4, episodes: 9, monitored: 9, available: 7 },
        { number: 5, episodes: 8, monitored: 8, available: 0 }
      ],
      filePath: '/media/tv/Stranger Things',
      downloadHistory: [
        { date: '2026-02-05', action: 'Searching for S05E01-08', quality: '1080p' }
      ]
    },
    {
      id: '4',
      title: 'Inception',
      service: 'radarr',
      monitoringStatus: 'monitored',
      availabilityStatus: 'downloading',
      qualityProfile: 'HD-1080p',
      lastUpdated: '2026-02-10T00:10:00',
      year: 2010,
      filePath: '/media/movies/Inception (2010)',
      downloadProgress: 67,
      downloadHistory: [
        { date: '2026-02-10', action: 'Downloading (67%)', quality: '1080p' }
      ]
    },
    {
      id: '5',
      title: 'The Office',
      service: 'sonarr',
      monitoringStatus: 'unmonitored',
      availabilityStatus: 'available',
      qualityProfile: 'SD',
      lastUpdated: '2026-01-15T09:20:00',
      seasons: [
        { number: 1, episodes: 6, monitored: 0, available: 6 },
        { number: 2, episodes: 22, monitored: 0, available: 22 },
        { number: 3, episodes: 25, monitored: 0, available: 25 }
      ],
      filePath: '/media/tv/The Office',
      downloadHistory: []
    },
    {
      id: '6',
      title: 'Interstellar',
      service: 'radarr',
      monitoringStatus: 'monitored',
      availabilityStatus: 'available',
      qualityProfile: '4K',
      lastUpdated: '2026-02-07T16:30:00',
      year: 2014,
      filePath: '/media/movies/Interstellar (2014)',
      fileSize: '52.8 GB',
      downloadHistory: [
        { date: '2026-02-07', action: 'Downloaded', quality: '4K' }
      ]
    },
    {
      id: '7',
      title: 'Game of Thrones',
      service: 'sonarr',
      monitoringStatus: 'monitored',
      availabilityStatus: 'available',
      qualityProfile: '4K',
      lastUpdated: '2026-02-06T12:00:00',
      seasons: [
        { number: 1, episodes: 10, monitored: 10, available: 10 },
        { number: 2, episodes: 10, monitored: 10, available: 10 },
        { number: 3, episodes: 10, monitored: 10, available: 10 },
        { number: 4, episodes: 10, monitored: 10, available: 10 },
        { number: 5, episodes: 10, monitored: 10, available: 10 },
        { number: 6, episodes: 10, monitored: 10, available: 10 },
        { number: 7, episodes: 7, monitored: 7, available: 7 },
        { number: 8, episodes: 6, monitored: 6, available: 6 }
      ],
      filePath: '/media/tv/Game of Thrones',
      downloadHistory: [
        { date: '2026-02-06', action: 'Downloaded S08E06', quality: '4K' }
      ]
    },
    {
      id: '8',
      title: 'The Matrix',
      service: 'radarr',
      monitoringStatus: 'monitored',
      availabilityStatus: 'missing',
      qualityProfile: '4K',
      lastUpdated: '2026-02-09T08:15:00',
      year: 1999,
      filePath: '/media/movies/The Matrix (1999)',
      downloadHistory: [
        { date: '2026-02-09', action: 'Searching', quality: '4K' }
      ]
    }
  ];

  // Filter logic
  const filteredData = useMemo(() => {
    let result = [...mockMonitoringData];

    // Search filter
    if (searchQuery) {
      result = result?.filter((item) =>
        item?.title?.toLowerCase()?.includes(searchQuery?.toLowerCase())
      );
    }

    // Service filter
    if (filters?.service !== 'all') {
      result = result?.filter((item) => item?.service === filters?.service);
    }

    // Status filter
    if (filters?.status !== 'all') {
      result = result?.filter((item) => item?.availabilityStatus === filters?.status);
    }

    // Quality filter
    if (filters?.quality !== 'all') {
      result = result?.filter((item) => item?.qualityProfile?.includes(filters?.quality));
    }

    return result;
  }, [searchQuery, filters, mockMonitoringData]);

  const handleFilterChange = (key, value) => {
    setFilters((prev) => ({ ...prev, [key]: value }));
  };

  const handleSelectAll = (checked) => {
    if (checked) {
      setSelectedItems(filteredData?.map((item) => item?.id));
    } else {
      setSelectedItems([]);
    }
  };

  const handleSelectItem = (id, checked) => {
    if (checked) {
      setSelectedItems((prev) => [...prev, id]);
    } else {
      setSelectedItems((prev) => prev?.filter((itemId) => itemId !== id));
    }
  };

  const handleBulkAction = (action) => {
    console.log(`Bulk action: ${action} on items:`, selectedItems);
    // Implement bulk action logic here
  };

  return (
    <div className="min-h-screen bg-background">
      <Header />
      <div className="container mx-auto px-4 py-6 md:py-8">
        {/* Page Header */}
        <div className="mb-6 md:mb-8">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center">
              <Icon name="Monitor" size={20} color="var(--color-primary)" />
            </div>
            <div>
              <h1 className="text-2xl md:text-3xl font-bold text-foreground">Media Monitoring</h1>
              <p className="text-sm text-muted-foreground">Comprehensive oversight of all Sonarr and Radarr monitored content</p>
            </div>
          </div>
        </div>

        {/* Filter Toolbar */}
        <FilterToolbar
          searchQuery={searchQuery}
          onSearchChange={setSearchQuery}
          filters={filters}
          onFilterChange={handleFilterChange}
          totalResults={filteredData?.length}
        />

        {/* Bulk Actions */}
        {selectedItems?.length > 0 && (
          <div className="bg-primary/10 border border-primary/30 rounded-lg p-4 mb-6 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Icon name="CheckSquare" size={18} className="text-primary" />
              <span className="text-sm font-medium text-foreground">
                {selectedItems?.length} {selectedItems?.length === 1 ? 'item' : 'items'} selected
              </span>
            </div>
            <div className="flex gap-2">
              <Button
                variant="outline"
                size="sm"
                iconName="Play"
                onClick={() => handleBulkAction('monitor')}
              >
                Monitor
              </Button>
              <Button
                variant="outline"
                size="sm"
                iconName="Pause"
                onClick={() => handleBulkAction('unmonitor')}
              >
                Unmonitor
              </Button>
              <Button
                variant="outline"
                size="sm"
                iconName="RefreshCw"
                onClick={() => handleBulkAction('refresh')}
              >
                Refresh
              </Button>
              <Button
                variant="outline"
                size="sm"
                iconName="Search"
                onClick={() => handleBulkAction('search')}
              >
                Search
              </Button>
            </div>
          </div>
        )}

        {/* Monitoring Table */}
        <MonitoringTable
          data={filteredData}
          selectedItems={selectedItems}
          onSelectAll={handleSelectAll}
          onSelectItem={handleSelectItem}
        />
      </div>
    </div>
  );
};

export default Monitoring;