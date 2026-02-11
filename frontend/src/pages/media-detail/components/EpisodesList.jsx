import React, { useState } from 'react';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';
import StatusIndicator from '../../monitoring/components/StatusIndicator';

const EpisodesList = ({ seasons }) => {
  const [expandedSeasons, setExpandedSeasons] = useState([0]); // First season expanded by default

  const toggleSeason = (seasonIndex) => {
    setExpandedSeasons((prev) =>
      prev?.includes(seasonIndex)
        ? prev?.filter((i) => i !== seasonIndex)
        : [...prev, seasonIndex]
    );
  };

  const getDownloadStatusConfig = (status) => {
    switch (status) {
      case 'downloaded':
        return { type: 'availability', status: 'available' };
      case 'downloading':
        return { type: 'availability', status: 'downloading' };
      case 'missing':
        return { type: 'availability', status: 'missing' };
      default:
        return { type: 'availability', status: 'missing' };
    }
  };

  const handleEpisodeMonitorToggle = (seasonIndex, episodeIndex) => {
    // TODO: API call to toggle episode monitoring
    console.log(`Toggle monitoring for S${seasonIndex + 1}E${episodeIndex + 1}`);
  };

  const handleManualSearch = (seasonIndex, episodeIndex) => {
    // TODO: API call to trigger manual search
    console.log(`Manual search for S${seasonIndex + 1}E${episodeIndex + 1}`);
  };

  return (
    <div className="bg-card border border-border rounded-lg overflow-hidden">
      <div className="p-6 border-b border-border">
        <h2 className="text-xl font-semibold text-foreground flex items-center gap-2">
          <Icon name="List" size={20} className="text-primary" />
          Seasons & Episodes
        </h2>
      </div>

      <div className="divide-y divide-border">
        {seasons?.map((season, seasonIndex) => (
          <div key={seasonIndex}>
            {/* Season Header */}
            <button
              onClick={() => toggleSeason(seasonIndex)}
              className="w-full px-6 py-4 flex items-center justify-between hover:bg-muted/50 transition-colors"
            >
              <div className="flex items-center gap-3">
                <Icon
                  name={expandedSeasons?.includes(seasonIndex) ? 'ChevronDown' : 'ChevronRight'}
                  size={20}
                  className="text-muted-foreground"
                />
                <h3 className="text-lg font-semibold text-foreground">
                  {season?.name || `Season ${season?.seasonNumber}`}
                </h3>
                <span className="text-sm text-muted-foreground">
                  {season?.episodes?.length} episodes
                </span>
              </div>
              <div className="flex items-center gap-4">
                <div className="text-sm text-muted-foreground">
                  {season?.episodes?.filter((ep) => ep?.downloaded)?.length} / {season?.episodes?.length} downloaded
                </div>
              </div>
            </button>

            {/* Episodes List */}
            {expandedSeasons?.includes(seasonIndex) && (
              <div className="bg-muted/30">
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead className="bg-muted">
                      <tr>
                        <th className="px-6 py-3 text-left text-xs font-semibold text-muted-foreground uppercase">
                          Episode
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-semibold text-muted-foreground uppercase">
                          Title
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-semibold text-muted-foreground uppercase">
                          Air Date
                        </th>
                        <th className="px-6 py-3 text-center text-xs font-semibold text-muted-foreground uppercase">
                          Status
                        </th>
                        <th className="px-6 py-3 text-center text-xs font-semibold text-muted-foreground uppercase">
                          Subtitles
                        </th>
                        <th className="px-6 py-3 text-right text-xs font-semibold text-muted-foreground uppercase">
                          File Size
                        </th>
                        <th className="px-6 py-3 text-center text-xs font-semibold text-muted-foreground uppercase">
                          Watched
                        </th>
                        <th className="px-6 py-3 text-center text-xs font-semibold text-muted-foreground uppercase">
                          Actions
                        </th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-border">
                      {season?.episodes?.map((episode, episodeIndex) => (
                        <tr key={episodeIndex} className="hover:bg-muted/50 transition-colors">
                          {/* Episode Number */}
                          <td className="px-6 py-4 whitespace-nowrap">
                            <span className="text-sm font-medium text-foreground">
                              {episode?.episodeNumber}
                            </span>
                          </td>

                          {/* Title */}
                          <td className="px-6 py-4">
                            <div className="flex items-center gap-2">
                              {episode?.monitored && (
                                <Icon name="Eye" size={14} className="text-success" />
                              )}
                              <span className="text-sm text-foreground">{episode?.title}</span>
                            </div>
                          </td>

                          {/* Air Date */}
                          <td className="px-6 py-4 whitespace-nowrap">
                            <span className="text-sm text-muted-foreground">{episode?.airDate || 'TBA'}</span>
                          </td>

                          {/* Download Status */}
                          <td className="px-6 py-4 text-center">
                            <div className="flex justify-center">
                              <StatusIndicator
                                {...getDownloadStatusConfig(episode?.downloadStatus)}
                              />
                            </div>
                          </td>

                          {/* Subtitles */}
                          <td className="px-6 py-4 text-center">
                            {episode?.hasSubtitles ? (
                              <div className="flex justify-center items-center gap-1">
                                <Icon name="Subtitles" size={14} className="text-success" />
                                {episode?.subtitleLanguages && (
                                  <span className="text-xs text-muted-foreground">
                                    ({episode?.subtitleLanguages?.join(', ')})
                                  </span>
                                )}
                              </div>
                            ) : (
                              <Icon name="Subtitles" size={14} className="text-muted-foreground" />
                            )}
                          </td>

                          {/* File Size */}
                          <td className="px-6 py-4 text-right whitespace-nowrap">
                            <span className="text-sm text-foreground font-medium">
                              {episode?.fileSize || '-'}
                            </span>
                          </td>

                          {/* Watched Status */}
                          <td className="px-6 py-4 text-center">
                            {episode?.watched ? (
                              <Icon name="CheckCircle2" size={16} className="text-success mx-auto" />
                            ) : (
                              <Icon name="Circle" size={16} className="text-muted-foreground mx-auto" />
                            )}
                          </td>

                          {/* Actions */}
                          <td className="px-6 py-4">
                            <div className="flex items-center justify-center gap-2">
                              <Button
                                size="xs"
                                variant="ghost"
                                iconName={episode?.monitored ? 'Eye' : 'EyeOff'}
                                onClick={() => handleEpisodeMonitorToggle(seasonIndex, episodeIndex)}
                                title={episode?.monitored ? 'Unmonitor' : 'Monitor'}
                              />
                              <Button
                                size="xs"
                                variant="ghost"
                                iconName="Search"
                                onClick={() => handleManualSearch(seasonIndex, episodeIndex)}
                                title="Manual Search"
                              />
                            </div>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default EpisodesList;