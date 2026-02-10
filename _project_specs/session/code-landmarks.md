<!--
UPDATE WHEN:
- Adding new entry points or key files
- Introducing new patterns
- Discovering non-obvious behavior

Helps quickly navigate the codebase when resuming work.
-->

# Code Landmarks

Quick reference to important parts of the codebase.

## Entry Points
| Location | Purpose |
|----------|---------|
| `app/main.py` | FastAPI app entry, lifespan, router registration |
| `init_db.py` | Database table initialization |

## Core Business Logic
| Location | Purpose |
|----------|---------|
| `app/services/sync_service.py` | Sync orchestration for all services |
| `app/services/analytics_service.py` | Jellyfin playback webhook processing |
| `app/services/torrent_enrichment_service.py` | Torrent-to-library matching |
| `app/services/metrics_service.py` | System metrics (CPU, RAM, disk) |

## Connectors (External APIs)
| Location | Purpose |
|----------|---------|
| `app/services/base_connector.py` | Abstract HTTP client base |
| `app/services/radarr_connector.py` | Radarr movie API |
| `app/services/sonarr_connector.py` | Sonarr TV API |
| `app/services/jellyfin_connector.py` | Jellyfin media server API |
| `app/services/jellyseerr_connector.py` | Jellyseerr request API |
| `app/services/qbittorrent_connector.py` | qBittorrent torrent API |
| `app/services/connector_factory.py` | Factory for connector instantiation |

## Routes
| Location | Purpose |
|----------|---------|
| `app/api/routes/dashboard.py` | Dashboard stats, recent items, calendar |
| `app/api/routes/analytics.py` | Playback webhook + analytics queries |
| `app/api/routes/services.py` | Service configuration CRUD |
| `app/api/routes/sync.py` | Manual sync triggers |
| `app/api/routes/torrents.py` | Torrent info + enrichment |
| `app/api/routes/jellyseerr.py` | Media request approve/decline |

## Configuration
| Location | Purpose |
|----------|---------|
| `app/core/config.py` | Pydantic Settings, env vars |
| `app/core/security.py` | API key auth middleware |
| `app/db.py` | SQLAlchemy engine + session |

## Models
| Location | Purpose |
|----------|---------|
| `app/models/models.py` | 11 SQLAlchemy ORM models |
| `app/models/enums.py` | ServiceType, MediaType, etc. |
| `app/api/schemas.py` | Pydantic request/response schemas |

## Schedulers
| Location | Purpose |
|----------|---------|
| `app/schedulers/scheduler.py` | APScheduler setup (15 min sync) |
| `app/schedulers/analytics_scheduler.py` | Metrics (30s) + cleanup (1h) |

## Key Patterns
| Pattern | Example Location | Notes |
|---------|------------------|-------|
| Connector pattern | `app/services/base_connector.py` | All external APIs extend this |
| Factory pattern | `app/services/connector_factory.py` | Instantiates connector from DB config |
| API key auth | `app/core/security.py` | `X-API-Key` header, except analytics |

## Gotchas & Non-Obvious Behavior
| Location | Issue | Notes |
|----------|-------|-------|
| `app/services/qbittorrent_connector.py` | Uses aiohttp, not httpx | Session-based cookie auth requires it |
| `app/api/routes/analytics.py` | No auth required | Public webhook endpoint |
| Codebase | French language | Comments, docstrings, variables in French |
