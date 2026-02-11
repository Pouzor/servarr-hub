import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import Header from '../../components/navigation/Header';
import Icon from '../../components/AppIcon';
import Button from '../../components/ui/Button';
import RecentAdditionsCard from './components/RecentAdditionsCard';
import StatisticsCard from './components/StatisticsCard';
import MiniCalendar from './components/MiniCalendar';
import RequestCard from './components/RequestCard';
import { getDashboardStatistics, getRecentItems } from '../../services/dashboardService';
import { getCalendarEvents } from '../../services/calendarService';
import { getJellyseerrRequests, deleteJellyseerrRequest } from '../../services/requestService';
import { triggerSync } from '../../services/syncService';

const MainDashboard = () => {
  const [lastRefresh, setLastRefresh] = useState(new Date());
  const [statistics, setStatistics] = useState([]);
  const [recentAdditions, setRecentAdditions] = useState([]);
  const [upcomingReleases, setUpcomingReleases] = useState([]);
  const [pendingRequests, setPendingRequests] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isSyncing, setIsSyncing] = useState(false);
  const navigate = useNavigate();

  // Load statistics from database
  const loadStatistics = async () => {
    try {
      const stats = await getDashboardStatistics();
      
      //if (stats && stats?.length > 0) {
        const formattedStats = stats?.map(stat => {
          // Map snake_case API response to camelCase
          const statType = stat?.stat_type;
          const totalCount = stat?.total_count;
          const details = stat?.details || {};

          const baseData = {
            title: statType === 'users' ? 'Total Users' :
                   statType === 'movies' ? 'Movies' :
                   statType === 'tv_shows' ? 'TV Shows' : 'Monitored Items',
            value: totalCount?.toString() || '0',
            icon: statType === 'users' ? 'Users' :
                  statType === 'movies' ? 'Film' :
                  statType === 'tv_shows' ? 'Tv' : 'Eye',
            color: statType === 'users' ? 'primary' :
                   statType === 'movies' ? 'secondary' :
                   statType === 'tv_shows' ? 'accent' : 'success',
            trend: 'neutral',
            trendValue: '0'
          };

          // Add subtitle and details based on stat type
          if (statType === 'users') {
            baseData.subtitle = `${details?.active_users || totalCount} Active`;
            baseData.details = [
              { label: 'Active Users', value: details?.active_users?.toString() || totalCount?.toString() || '0' },
              { label: 'Total Watch Hours', value: details?.total_watch_hours?.toString() || '0' }
            ];
          } else if (statType === 'movies') {
            baseData.subtitle = 'In library';
            baseData.details = [
              { label: 'Total Hours', value: details?.total_hours?.toString() || '0' }
            ];
          } else if (statType === 'tv_shows') {
            baseData.subtitle = `${details?.total_episodes || 0} Episodes`;
            baseData.details = [
              { label: 'Total Series', value: details?.total_series?.toString() || '0' },
              { label: 'Total Episodes', value: details?.total_episodes?.toString() || '0' },
              { label: 'Total Hours', value: details?.total_hours?.toString() || '0' }
            ];
          } else if (statType === 'monitored_items') {
            baseData.subtitle = 'Radarr & Sonarr';
            baseData.details = [
              { label: 'Monitored', value: details?.monitored?.toString() || '0' },
              { label: 'Unmonitored', value: details?.unmonitored?.toString() || '0' },
              { label: 'Downloading', value: details?.downloading?.toString() || '0' },
              { label: 'Downloaded', value: details?.downloaded?.toString() || '0' },
              { label: 'Missing', value: details?.missing?.toString() || '0' },
              { label: 'Queued', value: details?.queued?.toString() || '0' },
              { label: 'Unreleased', value: details?.unreleased?.toString() || '0' }
            ];
          }

          return baseData;
        });

        setStatistics(formattedStats);
      //}
    } catch (error) {
      console.error('Error loading statistics:', error);
    }
  };

  // Load library items from database
  const loadLibraryItems = async () => {
    try {
      const items = await getRecentItems(6);
      
      // Map snake_case API response to camelCase for frontend
      const formattedItems = items?.map(item => ({
        id: item?.id,
        title: item?.title,
        year: item?.year,
        type: item?.media_type, // 'tv' or 'movie'
        image: item?.image_url,
        imageAlt: item?.image_alt,
        quality: item?.quality,
        rating: item?.rating,
        description: item?.description,
        addedDate: item?.added_date,
        size: item?.size,
        createdAt: item?.created_at
      })) || [];
      
      setRecentAdditions(formattedItems);
    } catch (error) {
      console.error('Error loading library items:', error);
    }
  };

  // Load calendar events from database
  const loadCalendarEvents = async () => {
    try {
      const events = await getCalendarEvents();
      setUpcomingReleases(events || []);
    } catch (error) {
      console.error('Error loading calendar events:', error);
    }
  };

  // Load Jellyseerr requests from database
  const loadJellyseerrRequests = async () => {
    try {
      const requests = await getJellyseerrRequests();
      
      // Map API response to match RequestCard component expectations
      const formattedRequests = requests?.map(request => ({
        id: request?.id,
        title: request?.title,
        mediaType: request?.mediaType, // 'movie' or 'tv'
        requestedBy: request?.requestedBy,
        requestedDate: request?.requestedDate,
        status: request?.status, // 1 = approved, 0 = pending
        imageUrl: request?.imageUrl,
        imageAlt: request?.imageAlt,
        year: request?.year,
        description: request?.description,
        priority: request?.priority,
        quality: request?.quality
      })) || [];
      
      setPendingRequests(formattedRequests);
    } catch (error) {
      console.error('Error loading Jellyseerr requests:', error);
    }
  };

  // Load all data
  const loadAllData = async () => {
    setIsLoading(true);
    try {
      await Promise.all([
        loadStatistics(),
        loadLibraryItems(),
        loadCalendarEvents(),
        loadJellyseerrRequests()
      ]);
    } catch (error) {
      console.error('Error loading dashboard data:', error);
    } finally {
      setIsLoading(false);
    }
  };

  // Initial load
  useEffect(() => {
    loadAllData();
  }, []);

  const handleApproveRequest = async (id) => {
    try {
      const success = await deleteJellyseerrRequest(id);
      if (success) {
        console.log('Approved request:', id);
        await loadJellyseerrRequests();
      }
    } catch (error) {
      console.error('Error approving request:', error);
    }
  };

  const handleRejectRequest = async (id) => {
    try {
      const success = await deleteJellyseerrRequest(id);
      if (success) {
        console.log('Rejected request:', id);
        await loadJellyseerrRequests();
      }
    } catch (error) {
      console.error('Error rejecting request:', error);
    }
  };

  const handleRefresh = async () => {
    setIsSyncing(true);
    setLastRefresh(new Date());
    
    try {
      // Trigger backend sync
      await triggerSync();
      
      // Wait for backend to process
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // Reload all data
      await loadAllData();
    } catch (error) {
      console.error('Error during refresh:', error);
    } finally {
      setIsSyncing(false);
    }
  };

  // Manual sync trigger
  const handleManualSync = async () => {
    setIsSyncing(true);
    try {
      console.log('Manual sync triggered...');
      await triggerSync();
      
      // Wait a moment for backend to process
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // Reload all data
      await Promise.all([
        loadStatistics(),
        loadLibraryItems(),
        loadCalendarEvents(),
        loadJellyseerrRequests() // Fixed: Changed from loadPendingRequests to loadJellyseerrRequests
      ]);
      
      setLastRefresh(new Date());
    } catch (error) {
      console.error('Manual sync failed:', error);
    } finally {
      setIsSyncing(false);
    }
  };

  return (
    <div className="min-h-screen bg-background">
      <Header />
      <main className="pt-20 md:pt-24 px-4 md:px-6 lg:px-8 pb-8">
        <div className="max-w-[1600px] mx-auto">
          <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4 mb-6 md:mb-8">
            <div>
              <h1 className="text-2xl md:text-3xl lg:text-4xl font-bold text-foreground mb-2">
                Dashboard Overview
              </h1>
              <p className="text-sm md:text-base text-muted-foreground">
                Monitor your entire Servarr media ecosystem from one place
              </p>
            </div>
            <div className="flex items-center gap-3">
              <div className="flex items-center gap-2 text-xs md:text-sm text-muted-foreground">
                <Icon name="Clock" size={16} />
                <span>Last updated: {lastRefresh?.toLocaleTimeString()}</span>
              </div>
              <Button
                variant="outline"
                size="sm"
                onClick={handleManualSync}
                disabled={isSyncing}
                iconName="RefreshCw"
                iconSize={16}>
                {isSyncing ? 'Syncing...' : 'Refresh'}
              </Button>
            </div>
          </div>

          {isLoading ? (
            <div className="flex items-center justify-center py-12">
              <div className="text-center">
                <Icon name="Loader" size={48} className="animate-spin text-primary mx-auto mb-4" />
                <p className="text-muted-foreground">Loading dashboard data...</p>
              </div>
            </div>
          ) : (
            <>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6 mb-6 md:mb-8">
                {statistics?.map((stat, index) => (
                <StatisticsCard key={index} {...stat} />
                ))}
              </div>

              <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 md:gap-8 mb-6 md:mb-8">
                <div className="lg:col-span-2">
                  <div className="bg-card border border-border rounded-lg p-4 md:p-6">
                    <div className="flex items-center justify-between mb-4 md:mb-6">
                      <h2 className="text-lg md:text-xl font-semibold text-foreground">
                        Recent Library Additions
                      </h2>
                      <Link to="/library">
                        <Button variant="ghost" size="sm" iconName="ArrowRight" iconPosition="right">
                          View All
                        </Button>
                      </Link>
                    </div>
                    {recentAdditions?.length > 0 ? (
                      <div className="grid grid-cols-2 md:grid-cols-3 gap-3 md:gap-4">
                        {recentAdditions?.map((item) => (
                        <RecentAdditionsCard
                          key={item?.id}
                          item={item} />
                        ))}
                      </div>
                    ) : (
                      <p className="text-center text-muted-foreground py-8">No recent additions</p>
                    )}
                  </div>
                </div>

                <div>
                  <MiniCalendar events={upcomingReleases} />
                </div>
              </div>

              <div className="bg-card border border-border rounded-lg p-4 md:p-6">
                <div className="flex items-center justify-between mb-4 md:mb-6">
                  <div>
                    <h2 className="text-lg md:text-xl font-semibold text-foreground mb-1">
                      Jellyseerr Requests
                    </h2>
                    <p className="text-sm text-muted-foreground">
                      {pendingRequests?.length} pending request{pendingRequests?.length !== 1 ? 's' : ''} awaiting approval
                    </p>
                  </div>
                  <div className="flex items-center gap-2">
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => navigate('/jellyseerr-requests')}
                      className="text-primary hover:text-primary/80"
                    >
                      See All
                    </Button>
                    <Button
                      variant="outline"
                      size="sm"
                      iconName="Filter"
                      iconSize={16}>
                      Filter
                    </Button>
                  </div>
                </div>
                {pendingRequests?.length > 0 ? (
                  <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
                    {pendingRequests?.map((request) => (
                    <RequestCard
                      key={request?.id}
                      request={request}
                      onApprove={handleApproveRequest}
                      onReject={handleRejectRequest} />
                    ))}
                  </div>
                ) : (
                  <p className="text-center text-muted-foreground py-8">No pending requests</p>
                )}
              </div>
            </>
          )}
        </div>
      </main>
    </div>
  );

};

export default MainDashboard;