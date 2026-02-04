from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime, date
from app.models.enums import (
    ServiceType, StatType, SyncStatus,
    MediaType, RequestPriority, CalendarStatus
)


# Service Configuration Schemas
class ServiceConfigurationBase(BaseModel):
    service_name: ServiceType
    url: str
    api_key: str
    port: Optional[int] = None
    is_active: bool = True


class ServiceConfigurationCreate(ServiceConfigurationBase):
    pass


class ServiceConfigurationUpdate(BaseModel):
    url: Optional[str] = None
    api_key: Optional[str] = None
    port: Optional[int] = None
    is_active: Optional[bool] = None


class ServiceConfigurationResponse(ServiceConfigurationBase):
    id: str
    last_tested_at: Optional[datetime] = None
    test_status: Optional[str] = None
    test_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


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
