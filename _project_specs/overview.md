# Project Overview

## Vision
ServarrHub is a unified Python FastAPI backend that aggregates data from a media server ecosystem (Jellyfin, Radarr, Sonarr, Jellyseerr, qBittorrent). It provides a single API for dashboard data, analytics, and management.

## Goals
- [ ] Unified dashboard API for all media services
- [ ] Real-time playback analytics from Jellyfin
- [ ] Automated sync of library data from Radarr/Sonarr
- [ ] Torrent management and enrichment via qBittorrent
- [ ] Media request management via Jellyseerr

## Non-Goals
- No frontend UI (API-only backend)
- No direct media streaming

## Success Metrics
- API response times under 200ms for dashboard endpoints
- Reliable 15-minute sync cycle without data loss
- Accurate playback session tracking
