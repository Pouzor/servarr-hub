"""
Routes API pour les analytics et webhooks
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, and_
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta, date
from app.db import get_db
from app.services.analytics_service import AnalyticsService
from app.core.security import verify_api_key
from app.models.models import (
    PlaybackSession, MediaStatistic, DeviceStatistic, 
    DailyAnalytic, ServerMetric
)
from app.models.enums import MediaType, DeviceType
from app.api.schemas import (
    PlaybackSessionResponse, MediaStatisticResponse,
    DailyAnalyticResponse, UsageAnalyticsResponse,
    MediaPlaybackAnalyticsItem, ActiveSessionItem,
    DeviceBreakdownItem, ServerPerformanceResponse
)
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.post("/webhook/playback", status_code=status.HTTP_200_OK)
async def receive_playback_webhook(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Endpoint pour recevoir les webhooks de lecture depuis Jellyfin
    
    Événements supportés :
    - PlaybackStart (Play)
    - PlaybackStop (Stop)
    - PlaybackPause (Pause)
    - PlaybackUnpause (Resume)
    """
    try:
        # Récupérer le payload
        payload = await request.json()
        
        logger.info(f"📥 Webhook reçu : {payload}")
        
        # Le plugin "Webhooks unofficial" envoie le format suivant :
        # {
        #   "NotificationType": "PlaybackStart",
        #   "ServerId": "...",
        #   "ServerName": "...",
        #   "UserId": "...",
        #   "UserName": "...",
        #   "ItemId": "...",
        #   "ItemName": "...",
        #   "ItemType": "Movie" ou "Episode",
        #   "Year": 2021,
        #   "PlaybackPosition": "00:00:00",
        #   "PlaybackPositionTicks": 0,
        #   "RunTimeTicks": 88800000000,
        #   "DeviceName": "...",
        #   "ClientName": "...",
        #   "PlayMethod": "DirectPlay" ou "Transcode",
        #   ...
        # }
        
        notification_type = payload.get("NotificationType")
        
        # Mapping des événements Jellyfin vers nos événements
        event_mapping = {
            "PlaybackStart": "playback.start",
            "PlaybackStop": "playback.stop",
            "PlaybackPause": "playback.pause",
            "PlaybackUnpause": "playback.unpause",
        }
        
        event_type = event_mapping.get(notification_type)
        
        if not event_type:
            logger.warning(f"⚠️  Type de notification non supporté : {notification_type}")
            return {"status": "ignored", "notification_type": notification_type}
        
        logger.info(f"📥 Webhook reçu : {event_type}")
        
        # Extraction des données
        media_id = payload.get("ItemId")
        user_id = payload.get("UserId")
        
        if not media_id or not user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ItemId et UserId sont requis"
            )
        
        # Traitement selon le type d'événement
        if event_type == "playback.start":
            # Déterminer si c'est une série ou un film
            item_type = payload.get("ItemType", "Movie")
            media_type = "tv" if item_type == "Episode" else "movie"
            
            # Info épisode si c'est une série
            episode_info = None
            if item_type == "Episode":
                season = payload.get("SeasonNumber", 0)
                episode = payload.get("EpisodeNumber", 0)
                episode_info = f"S{season:02d}E{episode:02d}"
            
            # Extraire la qualité vidéo
            video_height = payload.get("VideoHeight", 0)
            quality_map = {
                2160: "4k",
                1080: "1080p",
                720: "720p",
                480: "480p"
            }
            video_quality = quality_map.get(video_height, "unknown")
            
            # Déterminer si c'est du transcodage
            play_method = payload.get("PlayMethod", "DirectPlay")
            is_transcoding = play_method == "Transcode"
            is_direct_playing = play_method == "DirectPlay"
            
            # Durée en secondes (RunTimeTicks / 10000000)
            run_time_ticks = payload.get("RunTimeTicks", 0)
            duration_seconds = run_time_ticks // 10000000 if run_time_ticks else None
            
            session_data = {
                "media_id": media_id,
                "media_title": payload.get("ItemName", "Unknown"),
                "media_type": media_type,
                "media_year": payload.get("Year"),
                "episode_info": episode_info,
                "poster_url": None,  # Pas disponible dans le format default
                "user_id": user_id,
                "user_name": payload.get("UserName", "Unknown"),
                "device_name": payload.get("DeviceName"),
                "client_name": payload.get("ClientName"),
                "video_quality": video_quality,
                "is_transcoding": is_transcoding,
                "is_direct_playing": is_direct_playing,
                "transcoding_progress": 0,
                "transcoding_speed": None,
                "video_codec_source": payload.get("VideoCodec"),
                "video_codec_target": payload.get("TranscodeVideoCodec") if is_transcoding else None,
                "duration_seconds": duration_seconds
            }
            
            session = AnalyticsService.start_session(db, session_data)
            return {"status": "success", "session_id": session.id, "event": event_type}
        
        elif event_type == "playback.stop":
            # Position de lecture en secondes
            playback_position_ticks = payload.get("PlaybackPositionTicks", 0)
            watched_seconds = playback_position_ticks // 10000000 if playback_position_ticks else 0
            
            session = AnalyticsService.stop_session(db, media_id, user_id, watched_seconds)
            
            if session:
                return {"status": "success", "session_id": session.id, "event": event_type}
            else:
                return {"status": "no_active_session", "event": event_type}
        
        elif event_type == "playback.pause":
            session = AnalyticsService.pause_session(db, media_id, user_id)
            return {"status": "success", "session_id": session.id if session else None, "event": event_type}
        
        elif event_type == "playback.unpause":
            session = AnalyticsService.resume_session(db, media_id, user_id)
            return {"status": "success", "session_id": session.id if session else None, "event": event_type}
        
        else:
            logger.warning(f"⚠️  Événement non supporté : {event_type}")
            return {"status": "ignored", "event": event_type}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erreur lors du traitement du webhook : {e}")
        import traceback
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur serveur : {str(e)}"
        )



# ============================================
# ANALYTICS ENDPOINTS (PROTÉGÉS PAR API KEY)
# ============================================

@router.get("/usage", response_model=List[UsageAnalyticsResponse])
async def get_usage_analytics(
    start_date: Optional[date] = Query(None, description="Date de début (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="Date de fin (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    """
    📊 VUE 1 : Usage Analytics - Graphique temporel
    
    Retourne les métriques quotidiennes (hours watched, total plays)
    Par défaut : 7 derniers jours
    """
    try:
        # Par défaut : 7 derniers jours
        if not end_date:
            end_date = date.today()
        if not start_date:
            start_date = end_date - timedelta(days=7)
        
        # Récupérer les analytics quotidiennes
        daily_stats = db.query(DailyAnalytic).filter(
            and_(
                DailyAnalytic.date >= start_date,
                DailyAnalytic.date <= end_date
            )
        ).order_by(DailyAnalytic.date).all()
        
        return [
            UsageAnalyticsResponse(
                date=stat.date,
                hours_watched=stat.hours_watched,
                total_plays=stat.total_plays
            )
            for stat in daily_stats
        ]
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de la récupération des usage analytics : {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/media", response_model=List[MediaPlaybackAnalyticsItem])
async def get_media_playback_analytics(
    limit: int = Query(50, ge=1, le=100, description="Nombre de résultats"),
    sort_by: str = Query("plays", description="Tri par : plays, duration, last_played"),
    order: str = Query("desc", description="Ordre : asc ou desc"),
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    """
    📊 VUE 2 : Media Playback Analytics - Tableau détaillé
    
    Retourne la liste des médias avec leurs statistiques
    """
    try:
        # Construire la requête
        query = db.query(MediaStatistic)
        
        # Tri
        if sort_by == "plays":
            query = query.order_by(desc(MediaStatistic.total_plays) if order == "desc" else MediaStatistic.total_plays)
        elif sort_by == "duration":
            query = query.order_by(desc(MediaStatistic.total_watched_seconds) if order == "desc" else MediaStatistic.total_watched_seconds)
        elif sort_by == "last_played":
            query = query.order_by(desc(MediaStatistic.last_played_at) if order == "desc" else MediaStatistic.last_played_at)
        
        media_stats = query.limit(limit).all()
        
        # Formater les résultats
        results = []
        for stat in media_stats:
            # Formater la durée (ex: "2h 28m")
            hours = stat.total_duration_seconds // 3600
            minutes = (stat.total_duration_seconds % 3600) // 60
            duration_str = f"{hours}h {minutes}m" if hours > 0 else f"{minutes}m"
            
            # Déterminer le status
            status_str = "Direct" if stat.direct_play_count > stat.transcoded_count else "Transcoded"
            
            # Qualité
            quality_str = stat.most_used_quality.value if stat.most_used_quality else "Unknown"
            
            results.append(
                MediaPlaybackAnalyticsItem(
                    media_title=stat.media_title,
                    media_type=stat.media_type,
                    plays=stat.total_plays,
                    duration=duration_str,
                    quality=quality_str,
                    status=status_str,
                    poster_url=stat.poster_url
                )
            )
        
        return results
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de la récupération des media analytics : {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/sessions/active", response_model=List[ActiveSessionItem])
async def get_active_sessions(
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    """
    📊 VUE 3 : Sessions actives en temps réel
    
    Retourne les sessions de lecture en cours
    """
    try:
        sessions = AnalyticsService.get_active_sessions(db)
        
        return [
            ActiveSessionItem(
                media_title=s.media_title,
                user_name=s.user_name,
                quality_from=s.video_codec_source or "Unknown",
                quality_to=s.video_codec_target or s.video_quality.value,
                progress=s.transcoding_progress,
                speed=s.transcoding_speed or 1.0,
                device_type=s.device_type
            )
            for s in sessions
        ]
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de la récupération des sessions actives : {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/devices", response_model=List[DeviceBreakdownItem])
async def get_device_breakdown(
    period_days: int = Query(7, ge=1, le=365, description="Période en jours"),
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    """
    📊 VUE 3 : Device Breakdown - Répartition par type d'appareil
    
    Retourne le nombre de sessions par type d'appareil sur une période
    """
    try:
        # Calculer la période
        end_date = date.today()
        start_date = end_date - timedelta(days=period_days)
        
        # Requête pour compter les sessions par device_type
        device_stats = db.query(
            PlaybackSession.device_type,
            func.count(PlaybackSession.id).label('session_count')
        ).filter(
            and_(
                func.date(PlaybackSession.start_time) >= start_date,
                func.date(PlaybackSession.start_time) <= end_date
            )
        ).group_by(PlaybackSession.device_type).all()
        
        # Calculer le total pour les pourcentages
        total_sessions = sum([stat.session_count for stat in device_stats])
        
        if total_sessions == 0:
            return []
        
        # Formater les résultats
        return [
            DeviceBreakdownItem(
                device_type=stat.device_type,
                session_count=stat.session_count,
                percentage=round((stat.session_count / total_sessions) * 100, 1)
            )
            for stat in device_stats
        ]
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de la récupération du device breakdown : {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/server-metrics", response_model=Optional[ServerPerformanceResponse])
async def get_server_metrics(
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    """
    📊 VUE 3 : Server Performance - Métriques serveur en temps réel
    
    Retourne les dernières métriques du serveur + sessions actives
    """
    try:
        # Récupérer la dernière métrique serveur
        latest_metric = db.query(ServerMetric).order_by(
            desc(ServerMetric.recorded_at)
        ).first()
        
        if not latest_metric:
            # Si aucune métrique, retourner des valeurs par défaut
            return None
        
        # Récupérer les sessions actives
        active_sessions = AnalyticsService.get_active_sessions(db)
        
        # Formater les sessions actives
        active_session_items = [
            ActiveSessionItem(
                media_title=s.media_title,
                user_name=s.user_name,
                quality_from=s.video_codec_source or "Unknown",
                quality_to=s.video_codec_target or s.video_quality.value,
                progress=s.transcoding_progress,
                speed=s.transcoding_speed or 1.0,
                device_type=s.device_type
            )
            for s in active_sessions
        ]
        
        return ServerPerformanceResponse(
            cpu_usage_percent=latest_metric.cpu_usage_percent or 0.0,
            cpu_status=latest_metric.cpu_status or "success",
            memory_usage_gb=latest_metric.memory_usage_gb or 0.0,
            memory_total_gb=latest_metric.memory_total_gb or 16.0,
            memory_status=latest_metric.memory_status or "success",
            storage_used_tb=latest_metric.storage_used_tb or 0.0,
            storage_total_tb=latest_metric.storage_total_tb or 10.0,
            storage_status=latest_metric.storage_status or "success",
            bandwidth_mbps=latest_metric.bandwidth_mbps or 0.0,
            bandwidth_status=latest_metric.bandwidth_status or "error",
            active_sessions=active_session_items,
            active_transcoding_count=latest_metric.active_transcoding_count
        )
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de la récupération des server metrics : {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
