import React from 'react';
import Icon from '../../../components/AppIcon';
import Image from '../../../components/AppImage';

const EventSidebar = ({ selectedDate, events, isLoading }) => {
  const formatDate = (date) => {
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    return date?.toLocaleDateString('en-US', options);
  };

  const getEventTypeIcon = (eventType, mediaType) => {
    if (eventType === 'release' && mediaType === 'tv') return 'Tv';
    if (eventType === 'release' && mediaType === 'movie') return 'Film';
    if (eventType === 'download') return 'Download';
    if (eventType === 'view') return 'Eye';
    return 'Calendar';
  };

  const getEventTypeColor = (eventType, mediaType) => {
    if (eventType === 'release' && mediaType === 'tv') return 'text-blue-400';
    if (eventType === 'release' && mediaType === 'movie') return 'text-green-400';
    if (eventType === 'download') return 'text-orange-400';
    if (eventType === 'view') return 'text-purple-400';
    return 'text-gray-400';
  };

  const getEventTypeLabel = (eventType, mediaType) => {
    if (eventType === 'release' && mediaType === 'tv') return 'TV Episode Release';
    if (eventType === 'release' && mediaType === 'movie') return 'Movie Release';
    if (eventType === 'download') return 'Download';
    if (eventType === 'view') return 'Viewed';
    return 'Event';
  };

  const getStatusColor = (status) => {
    const colors = {
      monitored: 'bg-primary/10 text-primary border-primary/20',
      downloading: 'bg-warning/10 text-warning border-warning/20',
      available: 'bg-success/10 text-success border-success/20'
    };
    return colors?.[status] || colors?.monitored;
  };

  if (isLoading) {
    return (
      <div className="bg-card border border-border rounded-lg p-6">
        <div className="flex items-center justify-center">
          <Icon name="Loader2" size={24} className="animate-spin text-muted-foreground" />
        </div>
      </div>
    );
  }

  return (
    <div className="bg-card border border-border rounded-lg overflow-hidden">
      {/* Header */}
      <div className="p-4 border-b border-border bg-muted/30">
        <h3 className="text-lg font-semibold text-foreground mb-1">
          Events
        </h3>
        <p className="text-sm text-muted-foreground">
          {formatDate(selectedDate)}
        </p>
      </div>

      {/* Events List */}
      <div className="p-4 space-y-4 max-h-[600px] overflow-y-auto">
        {events?.length === 0 ? (
          <div className="text-center py-8">
            <Icon name="Calendar" size={48} className="mx-auto mb-3 text-muted-foreground/50" />
            <p className="text-muted-foreground">No events for this date</p>
          </div>
        ) : (
          events?.map(event => (
            <div key={event?.id} className="bg-muted/30 border border-border rounded-lg p-3 hover:shadow-md transition-all">
              <div className="flex gap-3">
                {/* Event Image */}
                <div className="flex-shrink-0 w-16 h-24 rounded-md overflow-hidden bg-muted">
                  <Image
                    src={event?.imageUrl}
                    alt={event?.imageAlt}
                    className="w-full h-full object-cover"
                  />
                </div>

                {/* Event Details */}
                <div className="flex-1 min-w-0">
                  <div className="flex items-start justify-between gap-2 mb-2">
                    <h4 className="text-sm font-semibold text-foreground line-clamp-2">
                      {event?.title}
                    </h4>
                    <Icon 
                      name={getEventTypeIcon(event?.eventType, event?.type)} 
                      size={16} 
                      className={getEventTypeColor(event?.eventType, event?.type)} 
                    />
                  </div>

                  {/* Event Type Badge */}
                  <div className="mb-2">
                    <span className="inline-block text-xs font-medium text-muted-foreground bg-muted px-2 py-1 rounded">
                      {getEventTypeLabel(event?.eventType, event?.type)}
                    </span>
                  </div>

                  {/* Episode Info */}
                  {event?.episode && (
                    <div className="flex items-center gap-2 text-xs text-muted-foreground mb-2">
                      <Icon name="Tv" size={12} />
                      <span>{event?.episode}</span>
                    </div>
                  )}

                  {/* Download Progress */}
                  {event?.progress !== undefined && (
                    <div className="mb-2">
                      <div className="flex items-center justify-between text-xs text-muted-foreground mb-1">
                        <span>Download Progress</span>
                        <span>{event?.progress}%</span>
                      </div>
                      <div className="w-full bg-muted rounded-full h-1.5">
                        <div 
                          className="bg-orange-500 h-1.5 rounded-full transition-all"
                          style={{ width: `${event?.progress}%` }}
                        ></div>
                      </div>
                    </div>
                  )}

                  {/* Viewed By */}
                  {event?.viewedBy && (
                    <div className="flex items-center gap-2 text-xs text-muted-foreground mb-2">
                      <Icon name="User" size={12} />
                      <span>Viewed by {event?.viewedBy}</span>
                    </div>
                  )}

                  {/* Status Badge */}
                  <div className={`inline-flex items-center gap-1 px-2 py-1 rounded-md text-xs font-medium ${getStatusColor(event?.status)}`}>
                    <span className="w-1.5 h-1.5 rounded-full bg-current"></span>
                    <span className="capitalize">{event?.status}</span>
                  </div>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default EventSidebar;