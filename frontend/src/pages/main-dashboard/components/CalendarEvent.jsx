import React from 'react';
import Icon from '../../../components/AppIcon';
import Image from '../../../components/AppImage';

const CalendarEvent = ({ event }) => {
  const getTypeIcon = () => {
    return event?.mediaType === 'movie' ? 'Film' : 'Tv';
  };

  const getTypeColor = () => {
    return event?.mediaType === 'movie' ? 'text-blue-400' : 'text-purple-400';
  };

  const getStatusColor = () => {
    const colors = {
      monitored: 'bg-primary/10 text-primary border-primary/20',
      downloading: 'bg-warning/10 text-warning border-warning/20',
      available: 'bg-success/10 text-success border-success/20'
    };
    return colors?.[event?.status] || colors?.monitored;
  };

  return (
    <div className="bg-card border border-border rounded-lg p-3 md:p-4 hover:shadow-elevation-2 transition-smooth">
      <div className="flex gap-3">
        <div className="flex-shrink-0 w-16 h-24 md:w-20 md:h-28 rounded-md overflow-hidden bg-muted">
          <Image
            src={event?.imageUrl}
            alt={event?.imageAlt}
            className="w-full h-full object-cover"
          />
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between gap-2 mb-2">
            <h4 className="text-sm md:text-base font-semibold text-foreground line-clamp-1">
              {event?.title}
            </h4>
            <Icon name={getTypeIcon()} size={16} className={getTypeColor()} />
          </div>
          <div className="space-y-2">
            <div className="flex items-center gap-2 text-xs text-muted-foreground">
              <Icon name="Calendar" size={12} />
              <span>{event?.releaseDate}</span>
            </div>
            {event?.episode && (
              <div className="flex items-center gap-2 text-xs text-muted-foreground">
                <Icon name="Tv" size={12} />
                <span>{event?.episode}</span>
              </div>
            )}
            <div className={`inline-flex items-center gap-1 px-2 py-1 rounded-md text-xs font-medium ${getStatusColor()}`}>
              <span className="w-1.5 h-1.5 rounded-full bg-current"></span>
              <span className="capitalize">{event?.status}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CalendarEvent;