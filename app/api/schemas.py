from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional, Dict, Any, List
from datetime import datetime, date
from app.models.enums import (
    ServiceType, StatType, SyncStatus,
    MediaType, RequestPriority, CalendarStatus,
    DeviceType, PlaybackMethod, VideoQuality, SessionStatus
)

# ============================================
# SERVICE CONFIGURATION SCHEMAS (MODIFIÉ)
# ============================================

class ServiceConfigurationBase(BaseModel):
    service_name: ServiceType
    url: str
    api_key: Optional[str] = None
    port: Optional[int] = None
    username: Optional[str] = None
    password: Optional[str] = None
    is_active: bool = True
    
    @field_validator('api_key', 'username', 'password')
    @classmethod
    def validate_credentials(cls, v, info):
        """Valide que soit api_key soit username/password est fourni"""
        # Cette validation sera faite au niveau du endpoint
        return v


class ServiceConfigurationCreate(ServiceConfigurationBase):
    """Schéma pour créer un service"""
    
    @model_validator(mode='after')
    def validate_service_credentials(self):
        """Valide les credentials selon le type de service"""
        service_name = self.service_name
        
        # Services qui utilisent API key
        if service_name in [ServiceType.RADARR, ServiceType.SONARR, ServiceType.JELLYFIN, ServiceType.JELLYSEERR]:
            if not self.api_key:
                raise ValueError(f"{service_name.value} nécessite une api_key")
        
        # Services qui utilisent username/password
        elif service_name == ServiceType.QBITTORRENT:
            if not self.username or not self.password:
                raise ValueError(f"qBittorrent nécessite username et password (username={self.username}, password={'***' if self.password else None})")
        
        return self



class ServiceConfigurationUpdate(BaseModel):
    url: Optional[str] = None
    api_key: Optional[str] = None
    port: Optional[int] = None
    username: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None


class ServiceConfigurationResponse(ServiceConfigurationBase):
    id: str
    last_tested_at: Optional[datetime] = None
    test_status: Optional[str] = None
    test_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    # Ne pas exposer le password dans les réponses
    password: Optional[str] = Field(None, exclude=True)
    
    class Config:
        from_attributes = True


# ============================================
# SCHEMAS EXISTANTS (INCHANGÉS)
# ============================================

# Dashboard Statistics Schemas
class DashboardStatisticResponse(BaseModel):
    id: str
    stat_type: StatType
    total_count: int
    details: Dict[str, Any]
    last_synced: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Library Item Schemas
class LibraryItemResponse(BaseModel):
    id: str
    title: str
    year: int
    media_type: MediaType
    image_url: str
    image_alt: str
    quality: str
    rating: Optional[str] = None
    description: Optional[str] = None
    added_date: str
    size: str
    torrent_info: Optional[Dict[str, Any]] = None  # ⬅️ NOUVEAU
    created_at: datetime
    
    class Config:
        from_attributes = True


# Calendar Event Schemas
class CalendarEventResponse(BaseModel):
    id: str
    title: str
    media_type: MediaType
    release_date: date
    episode: Optional[str] = None
    image_url: str
    image_alt: str
    status: CalendarStatus
    created_at: datetime
    
    class Config:
        from_attributes = True


# Jellyseerr Request Schemas
class JellyseerrRequestResponse(BaseModel):
    id: str
    title: str
    media_type: MediaType
    year: int
    image_url: str
    image_alt: str
    priority: RequestPriority
    requested_by: str
    requested_date: str
    quality: str
    description: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class JellyseerrRequestAction(BaseModel):
    request_id: str
    action: str = Field(..., pattern="^(approve|decline)$")


# Sync Metadata Schemas
class SyncMetadataResponse(BaseModel):
    id: str
    service_name: ServiceType
    last_sync_time: Optional[datetime] = None
    sync_status: SyncStatus
    error_message: Optional[str] = None
    next_sync_time: Optional[datetime] = None
    sync_duration_ms: Optional[int] = None
    records_synced: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Dashboard Response
class DashboardResponse(BaseModel):
    statistics: List[DashboardStatisticResponse]
    recent_items: List[LibraryItemResponse]
    calendar_events: List[CalendarEventResponse]
    recent_requests: List[JellyseerrRequestResponse]


# Playback Session Schemas
class PlaybackSessionResponse(BaseModel):
    """Schéma de réponse pour une session de lecture"""
    id: str
    media_id: str
    media_title: str
    media_type: MediaType
    media_year: Optional[int] = None
    episode_info: Optional[str] = None
    poster_url: Optional[str] = None
    user_id: str
    user_name: str
    device_type: DeviceType
    device_name: Optional[str] = None
    client_name: Optional[str] = None
    video_quality: VideoQuality
    playback_method: PlaybackMethod
    transcoding_progress: int = 0
    transcoding_speed: Optional[float] = None
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_seconds: Optional[int] = None
    watched_seconds: int = 0
    status: SessionStatus
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Webhook Payload Schemas
class WebhookPlaybackData(BaseModel):
    """Schéma pour les données du webhook de lecture"""
    media_id: str = Field(..., description="ID du média (Jellyfin/Plex)")
    media_title: str = Field(..., description="Titre du média")
    media_type: str = Field(default="movie", description="Type: movie ou tv")
    media_year: Optional[int] = None
    episode_info: Optional[str] = Field(None, description="Info épisode (ex: S04E09)")
    poster_url: Optional[str] = None
    user_id: str = Field(..., description="ID de l'utilisateur")
    user_name: str = Field(..., description="Nom de l'utilisateur")
    device_name: Optional[str] = None
    client_name: Optional[str] = Field(None, description="Nom du client (ex: Jellyfin Web)")
    video_quality: Optional[str] = Field(None, description="Qualité vidéo (ex: 1080p, 4K)")
    is_transcoding: bool = False
    is_direct_playing: bool = True
    transcoding_progress: Optional[int] = 0
    transcoding_speed: Optional[float] = None
    video_codec_source: Optional[str] = None
    video_codec_target: Optional[str] = None
    duration_seconds: Optional[int] = None
    watched_seconds: Optional[int] = None


class WebhookPayload(BaseModel):
    """Schéma principal du webhook"""
    event: str = Field(..., description="Type d'événement: playback.start, playback.stop, etc.")
    data: WebhookPlaybackData


# Media Statistics Schemas
class MediaStatisticResponse(BaseModel):
    """Schéma de réponse pour les statistiques d'un média"""
    id: str
    media_id: str
    media_title: str
    media_type: MediaType
    media_year: Optional[int] = None
    poster_url: Optional[str] = None
    total_plays: int
    total_duration_seconds: int
    total_watched_seconds: int
    unique_users: int
    most_used_quality: Optional[VideoQuality] = None
    direct_play_count: int
    transcoded_count: int
    last_played_at: Optional[datetime] = None
    first_played_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Device Statistics Schemas
class DeviceStatisticResponse(BaseModel):
    """Schéma de réponse pour les statistiques par appareil"""
    id: str
    device_type: DeviceType
    period_start: date
    period_end: date
    session_count: int
    total_duration_seconds: int
    unique_users: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Daily Analytics Schemas
class DailyAnalyticResponse(BaseModel):
    """Schéma de réponse pour les analytics quotidiennes"""
    id: str
    date: date
    total_plays: int
    hours_watched: float
    unique_users: int
    unique_media: int
    movies_played: int
    tv_episodes_played: int
    direct_play_count: int
    transcoded_count: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Server Metrics Schemas
class ServerMetricResponse(BaseModel):
    """Schéma de réponse pour les métriques serveur"""
    id: str
    cpu_usage_percent: Optional[float] = None
    memory_usage_gb: Optional[float] = None
    memory_total_gb: Optional[float] = None
    storage_used_tb: Optional[float] = None
    storage_total_tb: Optional[float] = None
    bandwidth_mbps: Optional[float] = None
    cpu_status: Optional[str] = None
    memory_status: Optional[str] = None
    bandwidth_status: Optional[str] = None
    storage_status: Optional[str] = None
    active_sessions_count: int = 0
    active_transcoding_count: int = 0
    recorded_at: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True


# Analytics Dashboard Schemas
class UsageAnalyticsResponse(BaseModel):
    """Schéma pour le graphique Usage Analytics (Vue 1)"""
    date: date
    hours_watched: float
    total_plays: int


class MediaPlaybackAnalyticsItem(BaseModel):
    """Schéma pour un élément du tableau Media Playback Analytics (Vue 2)"""
    media_title: str
    media_type: MediaType
    plays: int
    duration: str  # Format: "2h 28m"
    quality: str
    status: str  # "Direct" ou "Transcoded"
    poster_url: Optional[str] = None


class ActiveSessionItem(BaseModel):
    """Schéma pour une session active (Vue 3)"""
    media_title: str
    user_name: str
    quality_from: str
    quality_to: str
    progress: int  # 0-100
    speed: float  # Ex: 1.2x
    device_type: DeviceType


class DeviceBreakdownItem(BaseModel):
    """Schéma pour la répartition par appareil (Vue 3)"""
    device_type: DeviceType
    session_count: int
    percentage: float


class ServerPerformanceResponse(BaseModel):
    """Schéma pour les métriques serveur (Vue 3)"""
    cpu_usage_percent: float
    cpu_status: str
    memory_usage_gb: float
    memory_total_gb: float
    memory_status: str
    storage_used_tb: float
    storage_total_tb: float
    storage_status: str
    bandwidth_mbps: float
    bandwidth_status: str
    active_sessions: List[ActiveSessionItem]
    active_transcoding_count: int
