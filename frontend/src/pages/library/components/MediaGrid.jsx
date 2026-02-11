import React from 'react';
import MediaCard from './MediaCard';
import Icon from '../../../components/AppIcon';

const MediaGrid = ({ media }) => {
  if (!media || media?.length === 0) {
    return (
      <div className="bg-card border border-border rounded-lg p-12 text-center">
        <div className="flex flex-col items-center gap-4">
          <div className="w-16 h-16 rounded-full bg-muted flex items-center justify-center">
            <Icon name="Search" size={32} className="text-muted-foreground" />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-foreground mb-1">No media found</h3>
            <p className="text-sm text-muted-foreground">Try adjusting your search or filters</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-4 md:gap-6">
      {media?.map((item) => (
        <MediaCard key={item?.id} item={item} />
      ))}
    </div>
  );
};

export default MediaGrid;