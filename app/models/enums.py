import enum


class ServiceType(str, enum.Enum):
    JELLYFIN = "jellyfin"
    JELLYSEERR = "jellyseerr"
    SONARR = "sonarr"
    RADARR = "radarr"


class StatType(str, enum.Enum):
    USERS = "users"
    MOVIES = "movies"
    TV_SHOWS = "tv_shows"
    MONITORED_ITEMS = "monitored_items"


class SyncStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    SUCCESS = "success"
    FAILED = "failed"


class MediaType(str, enum.Enum):
    MOVIE = "movie"
    TV = "tv"


class RequestPriority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class CalendarStatus(str, enum.Enum):
    MONITORED = "monitored"
    DOWNLOADING = "downloading"
    AVAILABLE = "available"
