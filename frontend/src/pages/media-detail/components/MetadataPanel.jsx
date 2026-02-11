import React from 'react';
import Icon from '../../../components/AppIcon';

const MetadataPanel = ({ media }) => {
  return (
    <div className="bg-card border border-border rounded-lg p-6 space-y-6">
      <h2 className="text-xl font-semibold text-foreground flex items-center gap-2">
        <Icon name="Info" size={20} className="text-primary" />
        Details
      </h2>

      {/* Overview */}
      <div>
        <h3 className="text-sm font-semibold text-muted-foreground uppercase mb-2">Overview</h3>
        <p className="text-foreground">{media?.description}</p>
      </div>

      {/* Metadata Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Release Date */}
        {media?.releaseDate && (
          <div>
            <h3 className="text-sm font-semibold text-muted-foreground uppercase mb-1">Release Date</h3>
            <p className="text-foreground">{media?.releaseDate}</p>
          </div>
        )}

        {/* Status */}
        {media?.status && (
          <div>
            <h3 className="text-sm font-semibold text-muted-foreground uppercase mb-1">Status</h3>
            <p className="text-foreground">{media?.status}</p>
          </div>
        )}

        {/* Network/Studio */}
        {media?.network && (
          <div>
            <h3 className="text-sm font-semibold text-muted-foreground uppercase mb-1">
              {media?.mediaType === 'tv' ? 'Network' : 'Studio'}
            </h3>
            <p className="text-foreground">{media?.network}</p>
          </div>
        )}

        {/* Quality Profile */}
        {media?.qualityProfile && (
          <div>
            <h3 className="text-sm font-semibold text-muted-foreground uppercase mb-1">Quality Profile</h3>
            <p className="text-foreground">{media?.qualityProfile}</p>
          </div>
        )}

        {/* Path */}
        {media?.path && (
          <div className="md:col-span-2">
            <h3 className="text-sm font-semibold text-muted-foreground uppercase mb-1">Path</h3>
            <p className="text-foreground text-sm font-mono bg-muted px-3 py-2 rounded break-all">
              {media?.path}
            </p>
          </div>
        )}
      </div>

      {/* Cast */}
      {media?.cast && media?.cast?.length > 0 && (
        <div>
          <h3 className="text-sm font-semibold text-muted-foreground uppercase mb-3">Cast</h3>
          <div className="flex flex-wrap gap-2">
            {media?.cast?.map((actor, index) => (
              <span
                key={index}
                className="px-3 py-1 bg-muted text-foreground text-sm rounded-md"
              >
                {actor}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default MetadataPanel;