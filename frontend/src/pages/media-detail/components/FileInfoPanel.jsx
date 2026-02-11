import React from 'react';
import Icon from '../../../components/AppIcon';
import StatusIndicator from '../../monitoring/components/StatusIndicator';

const FileInfoPanel = ({ media }) => {
  const getSeedRatioColor = (ratio) => {
    if (ratio >= 3) return 'text-success';
    if (ratio >= 1.5) return 'text-warning';
    return 'text-error';
  };

  const formatSecondsToTime = (seconds) => {
    if (!seconds) return 'N/A';
    const days = Math.floor(seconds / 86400);
    const hours = Math.floor((seconds % 86400) / 3600);
    if (days > 0) return `${days}d ${hours}h`;
    if (hours > 0) return `${hours}h`;
    return `${Math.floor(seconds / 60)}m`;
  };

  return (
    <div className="bg-card border border-border rounded-lg p-6 space-y-6">
      <h2 className="text-xl font-semibold text-foreground flex items-center gap-2">
        <Icon name="HardDrive" size={20} className="text-primary" />
        File Information
      </h2>

      {/* Quality */}
      <div className="space-y-2">
        <h3 className="text-sm font-semibold text-muted-foreground uppercase">Quality</h3>
        <div className="flex items-center gap-2">
          <div className="bg-accent px-3 py-1 rounded-md">
            <span className="text-sm font-bold text-accent-foreground">{media?.quality || 'N/A'}</span>
          </div>
        </div>
      </div>

      {/* File Size */}
      <div className="space-y-2">
        <h3 className="text-sm font-semibold text-muted-foreground uppercase">File Size</h3>
        <div className="flex items-center gap-2">
          <Icon name="HardDrive" size={16} className="text-muted-foreground" />
          <span className="text-foreground font-medium">{media?.size || '0.0 GB'}</span>
        </div>
      </div>

      {/* Files Count */}
      {media?.nbMedia && (
        <div className="space-y-2">
          <h3 className="text-sm font-semibold text-muted-foreground uppercase">Files</h3>
          <div className="flex items-center gap-2">
            <Icon name="FileStack" size={16} className="text-muted-foreground" />
            <span className="text-foreground font-medium">{media?.nbMedia}</span>
          </div>
        </div>
      )}

      {/* Subtitles */}
      <div className="space-y-2">
        <h3 className="text-sm font-semibold text-muted-foreground uppercase">Subtitles</h3>
        {media?.subtitles && media?.subtitles?.length > 0 ? (
          <div className="space-y-2">
            {media?.subtitles?.map((subtitle, index) => (
              <div key={index} className="flex items-center justify-between bg-muted px-3 py-2 rounded-md">
                <div className="flex items-center gap-2">
                  <Icon name="Subtitles" size={14} className="text-success" />
                  <span className="text-sm text-foreground">{subtitle?.language}</span>
                </div>
                <span className="text-xs text-muted-foreground">{subtitle?.format}</span>
              </div>
            ))}
          </div>
        ) : (
          <div className="flex items-center gap-2 text-muted-foreground">
            <Icon name="Subtitles" size={16} />
            <span className="text-sm">No subtitles available</span>
          </div>
        )}
      </div>

      {/* qBittorrent Info */}
      {media?.torrentInfo && (
        <div className="space-y-3 pt-3 border-t border-border">
          <h3 className="text-sm font-semibold text-muted-foreground uppercase flex items-center gap-2">
            <Icon name="Download" size={16} />
            Torrent Info
          </h3>

          {/* Status */}
          <div className="flex items-center justify-between">
            <span className="text-sm text-muted-foreground">Status</span>
            <StatusIndicator
              status={media?.torrentInfo?.status === 'seeding' ? 'available' : 'downloading'}
              type="availability"
            />
          </div>

          {/* Ratio */}
          <div className="flex items-center justify-between">
            <span className="text-sm text-muted-foreground">Ratio</span>
            <span className={`text-sm font-bold ${getSeedRatioColor(media?.torrentInfo?.ratio)}`}>
              {media?.torrentInfo?.ratio?.toFixed(2) || '0.00'}
            </span>
          </div>

          {/* Seeding Time */}
          {media?.torrentInfo?.seedingTime && (
            <div className="flex items-center justify-between">
              <span className="text-sm text-muted-foreground">Seeding Time</span>
              <span className="text-sm text-foreground">
                {formatSecondsToTime(media?.torrentInfo?.seedingTime)}
              </span>
            </div>
          )}

          {/* Progress */}
          <div className="flex items-center justify-between">
            <span className="text-sm text-muted-foreground">Progress</span>
            <span className="text-sm text-foreground font-medium">
              {media?.torrentInfo?.progress || 100}%
            </span>
          </div>
        </div>
      )}

      {/* Watch Status */}
      <div className="space-y-3 pt-3 border-t border-border">
        <h3 className="text-sm font-semibold text-muted-foreground uppercase flex items-center gap-2">
          <Icon name="Eye" size={16} />
          Watch Status
        </h3>

        {/* View Count */}
        <div className="flex items-center justify-between">
          <span className="text-sm text-muted-foreground">Views</span>
          <span className="text-sm text-foreground font-medium">{media?.viewCount || 0}</span>
        </div>

        {/* Playback Progress */}
        {media?.playbackProgress !== undefined && (
          <div className="space-y-1">
            <div className="flex items-center justify-between">
              <span className="text-sm text-muted-foreground">Progress</span>
              <span className="text-sm text-foreground font-medium">{media?.playbackProgress}%</span>
            </div>
            <div className="w-full bg-muted rounded-full h-2">
              <div
                className="bg-primary h-2 rounded-full transition-all"
                style={{ width: `${media?.playbackProgress}%` }}
              ></div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default FileInfoPanel;