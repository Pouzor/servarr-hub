from sqlalchemy import Column, String, Integer, Boolean, Text, DateTime, Date, JSON, Enum as SQLEnum, Index
from sqlalchemy.sql import func
from app.db import Base
from app.models.enums import (
    ServiceType, StatType, SyncStatus, 
    MediaType, RequestPriority, CalendarStatus
)
import uuid


def generate_uuid():
    """Génère un UUID au format string"""
    return str(uuid.uuid4())


# Table 1: Service Configurations
class ServiceConfiguration(Base):
    __tablename__ = "service_configurations"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    service_name = Column(SQLEnum(ServiceType), unique=True, nullable=False, index=True)
    url = Column(Text, nullable=False)
    api_key = Column(Text, nullable=False)
    port = Column(Integer)
    is_active = Column(Boolean, default=True, index=True)
    last_tested_at = Column(DateTime(timezone=True))
    test_status = Column(Text)
    test_message = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


# Table 2: Dashboard Statistics
class DashboardStatistic(Base):
    __tablename__ = "dashboard_statistics"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    stat_type = Column(SQLEnum(StatType), unique=True, nullable=False, index=True)
    total_count = Column(Integer, default=0)
    details = Column(JSON, default={})
    last_synced = Column(DateTime(timezone=True), index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


# Table 3: Sync Metadata
class SyncMetadata(Base):
    __tablename__ = "sync_metadata"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    service_name = Column(SQLEnum(ServiceType), nullable=False, index=True)
    last_sync_time = Column(DateTime(timezone=True))
    sync_status = Column(SQLEnum(SyncStatus), default=SyncStatus.PENDING, index=True)
    error_message = Column(Text)
    next_sync_time = Column(DateTime(timezone=True), index=True)
    sync_duration_ms = Column(Integer)
    records_synced = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


# Table 4: Library Items
class LibraryItem(Base):
    __tablename__ = "library_items"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    title = Column(Text, nullable=False)
    year = Column(Integer, nullable=False)
    media_type = Column(SQLEnum(MediaType), nullable=False, index=True)
    image_url = Column(Text, nullable=False)
    image_alt = Column(Text, nullable=False)
    quality = Column(Text, nullable=False)
    rating = Column(Text)
    description = Column(Text)
    added_date = Column(Text, nullable=False)
    size = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


# Table 5: Calendar Events
class CalendarEvent(Base):
    __tablename__ = "calendar_events"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    title = Column(Text, nullable=False)
    media_type = Column(SQLEnum(MediaType), nullable=False)
    release_date = Column(Date, nullable=False, index=True)
    episode = Column(Text)
    image_url = Column(Text, nullable=False)
    image_alt = Column(Text, nullable=False)
    status = Column(SQLEnum(CalendarStatus), nullable=False, default=CalendarStatus.MONITORED, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


# Table 6: Jellyseerr Requests
class JellyseerrRequest(Base):
    __tablename__ = "jellyseerr_requests"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    title = Column(Text, nullable=False)
    media_type = Column(SQLEnum(MediaType), nullable=False)
    year = Column(Integer, nullable=False)
    image_url = Column(Text, nullable=False)
    image_alt = Column(Text, nullable=False)
    priority = Column(SQLEnum(RequestPriority), nullable=False, default=RequestPriority.MEDIUM, index=True)
    requested_by = Column(Text, nullable=False)
    requested_date = Column(Text, nullable=False)
    quality = Column(Text, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
