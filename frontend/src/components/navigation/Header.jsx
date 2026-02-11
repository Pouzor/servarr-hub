import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import Icon from '../AppIcon';
import Button from '../ui/Button';

const Header = () => {
  const location = useLocation();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [connectionStatus, setConnectionStatus] = useState({
    radarr: 'connected',
    sonarr: 'connected',
    jellyfin: 'connected',
    jellyseerr: 'warning'
  });
  const [showQuickActions, setShowQuickActions] = useState(false);
  const [configProgress, setConfigProgress] = useState(false);

  useEffect(() => {
    const configComplete = localStorage.getItem('servarrhub_config_complete');
    setConfigProgress(!configComplete);
  }, []);

  const navigationItems = [
    {
      label: 'Dashboard',
      path: '/main-dashboard',
      icon: 'LayoutDashboard',
      tooltip: 'Unified monitoring hub'
    },
    {
      label: 'Library',
      path: '/library',
      icon: 'Library',
      tooltip: 'Browse media collection'
    },
    {
      label: 'Monitoring',
      path: '/monitoring',
      icon: 'Monitor',
      tooltip: 'Sonarr/Radarr media tracking'
    },
    {
      label: 'Analytics',
      path: '/jellyfin-statistics',
      icon: 'BarChart3',
      tooltip: 'Detailed usage statistics'
    },
    {
      label: 'Calendar',
      path: '/calendar',
      icon: 'Calendar',
      tooltip: 'Media release schedule and activity'
    },
    {
      label: 'Configuration',
      path: '/initial-configuration',
      icon: 'Settings',
      tooltip: 'API setup and service connections'
    }
  ];

  const quickActions = [
    {
      id: 1,
      title: 'The Matrix Resurrections',
      type: 'Movie Request',
      user: 'john_doe',
      time: '5 min ago',
      description: 'Requested in 4K quality'
    },
    {
      id: 2,
      title: 'Stranger Things S5',
      type: 'TV Request',
      user: 'jane_smith',
      time: '12 min ago',
      description: 'All episodes when available'
    },
    {
      id: 3,
      title: 'Dune: Part Two',
      type: 'Movie Request',
      user: 'mike_wilson',
      time: '1 hour ago',
      description: 'IMAX Enhanced preferred'
    }
  ];

  const isActive = (path) => location?.pathname === path;

  const getStatusColor = (status) => {
    switch (status) {
      case 'connected':
        return 'connected';
      case 'warning':
        return 'warning';
      case 'error':
        return 'error';
      default:
        return 'connected';
    }
  };

  const getOverallStatus = () => {
    const statuses = Object.values(connectionStatus);
    if (statuses?.includes('error')) return 'error';
    if (statuses?.includes('warning')) return 'warning';
    return 'connected';
  };

  const handleApprove = (id) => {
    console.log('Approved request:', id);
  };

  const handleReject = (id) => {
    console.log('Rejected request:', id);
  };

  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen);
  };

  const closeMobileMenu = () => {
    setIsMobileMenuOpen(false);
  };

  useEffect(() => {
    if (isMobileMenuOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = 'unset';
    }
    return () => {
      document.body.style.overflow = 'unset';
    };
  }, [isMobileMenuOpen]);

  return (
    <>
      <header className="nav-header">
        <div className="nav-header-container">
          <div className="nav-header-logo">
            <div className="nav-header-logo-icon">
              <Icon name="Server" size={24} color="var(--color-primary)" />
            </div>
            <span className="nav-header-logo-text">ServarrHub</span>
          </div>

          <nav className="nav-header-menu">
            {navigationItems?.map((item) => (
              <Link
                key={item?.path}
                to={item?.path}
                className={`nav-header-item ${isActive(item?.path) ? 'active' : ''}`}
                title={item?.tooltip}
              >
                <Icon name={item?.icon} size={18} className="mr-2" />
                {item?.label}
                {item?.path === '/initial-configuration' && configProgress && (
                  <span className="progress-badge">!</span>
                )}
              </Link>
            ))}
          </nav>

          <div className="nav-header-actions">
            <div className="relative">
              <button
                className={`status-indicator ${getStatusColor(getOverallStatus())}`}
                onClick={() => setShowQuickActions(!showQuickActions)}
                title="View connection status and quick actions"
              >
                <span className="status-indicator-dot"></span>
                <span className="hidden sm:inline">
                  {getOverallStatus() === 'connected' ? 'All Systems' : 'Issues Detected'}
                </span>
                {connectionStatus?.jellyseerr === 'warning' && (
                  <span className="ml-1 px-1.5 py-0.5 bg-warning/20 text-warning rounded text-xs font-bold">
                    3
                  </span>
                )}
              </button>

              <div className={`quick-action-menu ${!showQuickActions ? 'hidden' : ''}`}>
                <div className="quick-action-header">
                  <h3 className="quick-action-title">System Status & Requests</h3>
                </div>
                
                <div className="px-4 py-3 border-b border-border bg-muted/20">
                  <div className="grid grid-cols-2 gap-3">
                    <div className="flex items-center gap-2">
                      <span className={`w-2 h-2 rounded-full ${connectionStatus?.radarr === 'connected' ? 'bg-success' : 'bg-error'}`}></span>
                      <span className="text-xs text-muted-foreground">Radarr</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className={`w-2 h-2 rounded-full ${connectionStatus?.sonarr === 'connected' ? 'bg-success' : 'bg-error'}`}></span>
                      <span className="text-xs text-muted-foreground">Sonarr</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className={`w-2 h-2 rounded-full ${connectionStatus?.jellyfin === 'connected' ? 'bg-success' : 'bg-error'}`}></span>
                      <span className="text-xs text-muted-foreground">Jellyfin</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className={`w-2 h-2 rounded-full ${connectionStatus?.jellyseerr === 'connected' ? 'bg-success' : connectionStatus?.jellyseerr === 'warning' ? 'bg-warning' : 'bg-error'}`}></span>
                      <span className="text-xs text-muted-foreground">Jellyseerr</span>
                    </div>
                  </div>
                </div>

                <div className="quick-action-list">
                  {quickActions?.map((action) => (
                    <div key={action?.id} className="quick-action-item">
                      <div className="quick-action-item-header">
                        <div className="flex-1">
                          <h4 className="quick-action-item-title">{action?.title}</h4>
                          <p className="text-xs text-muted-foreground mt-0.5">
                            {action?.type} • {action?.user}
                          </p>
                        </div>
                        <span className="quick-action-item-time">{action?.time}</span>
                      </div>
                      <p className="quick-action-item-description">{action?.description}</p>
                      <div className="quick-action-item-actions">
                        <Button
                          variant="success"
                          size="xs"
                          onClick={() => handleApprove(action?.id)}
                          iconName="Check"
                          iconSize={14}
                        >
                          Approve
                        </Button>
                        <Button
                          variant="destructive"
                          size="xs"
                          onClick={() => handleReject(action?.id)}
                          iconName="X"
                          iconSize={14}
                        >
                          Reject
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </header>
      <button
        className="nav-mobile-toggle"
        onClick={toggleMobileMenu}
        aria-label="Toggle mobile menu"
        aria-expanded={isMobileMenuOpen}
      >
        <Icon name={isMobileMenuOpen ? 'X' : 'Menu'} size={24} />
      </button>
      <div className={`nav-mobile-menu ${!isMobileMenuOpen ? 'closed' : ''}`}>
        <div className="nav-mobile-menu-header">
          <div className="nav-header-logo">
            <div className="nav-header-logo-icon">
              <Icon name="Server" size={24} color="var(--color-primary)" />
            </div>
            <span className="nav-header-logo-text">ServarrHub</span>
          </div>
        </div>

        <nav className="nav-mobile-menu-items">
          {navigationItems?.map((item) => (
            <Link
              key={item?.path}
              to={item?.path}
              className={`nav-mobile-menu-item ${isActive(item?.path) ? 'active' : ''}`}
              onClick={closeMobileMenu}
            >
              <Icon name={item?.icon} size={20} className="mr-3" />
              {item?.label}
              {item?.path === '/initial-configuration' && configProgress && (
                <span className="progress-badge">!</span>
              )}
            </Link>
          ))}

          <div className="mt-6 pt-6 border-t border-border">
            <div className="mb-4">
              <h4 className="text-sm font-semibold text-foreground mb-3 font-heading">
                System Status
              </h4>
              <div className="space-y-2">
                {Object.entries(connectionStatus)?.map(([service, status]) => (
                  <div key={service} className="flex items-center justify-between">
                    <span className="text-sm text-muted-foreground capitalize">{service}</span>
                    <span className={`status-indicator ${getStatusColor(status)}`}>
                      <span className="status-indicator-dot"></span>
                      {status}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            <div>
              <h4 className="text-sm font-semibold text-foreground mb-3 font-heading">
                Pending Requests ({quickActions?.length})
              </h4>
              <div className="space-y-3">
                {quickActions?.map((action) => (
                  <div key={action?.id} className="p-3 bg-muted/30 rounded-lg">
                    <h5 className="text-sm font-medium text-foreground mb-1">{action?.title}</h5>
                    <p className="text-xs text-muted-foreground mb-2">{action?.description}</p>
                    <div className="flex gap-2">
                      <Button
                        variant="success"
                        size="xs"
                        onClick={() => handleApprove(action?.id)}
                        iconName="Check"
                        iconSize={14}
                        fullWidth
                      >
                        Approve
                      </Button>
                      <Button
                        variant="destructive"
                        size="xs"
                        onClick={() => handleReject(action?.id)}
                        iconName="X"
                        iconSize={14}
                        fullWidth
                      >
                        Reject
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </nav>
      </div>
    </>
  );
};

export default Header;