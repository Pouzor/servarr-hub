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
from app.core.config import settings
from app.models.models import (
    PlaybackSession, MediaStatistic, DeviceStatistic,
    DailyAnalytic, ServerMetric, LibraryItem
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


# ============================================
# WEBHOOK ENDPOINT (PUBLIC)
# ============================================

@router.post("/webhook/playback", status_code=status.HTTP_200_OK)
async def receive_playback_webhook(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Endpoint pour recevoir les webhooks de lecture depuis Jellyfin
    
    Événements supportés :
    - Play : Début de lecture
    - Stop : Fin de lecture
    - Pause : Mise en pause
    - Resume : Reprise de lecture
    """
    try:
        # Récupérer le payload
        payload = await request.json()
        
        # Extraire les données principales
        event_type_raw = payload.get("Event")
        item = payload.get("Item", {})
        user = payload.get("User", {})
        session = payload.get("Session", {})
        play_state = session.get("PlayState", {})
        
        # Mapping des événements
        event_mapping = {
            "Play": "playback.start",
            "Stop": "playback.stop",
            "Pause": "playback.pause",
            "Resume": "playback.unpause",
        }
        
        event_type = event_mapping.get(event_type_raw)
        
        if not event_type:
            logger.warning(f"⚠️  Type d'événement non supporté : {event_type_raw}")
            return {"status": "ignored", "event": event_type_raw}
        
        logger.info(f"📥 Webhook reçu : {event_type} - {item.get('Name', 'Unknown')}")
        
        # Extraction des IDs
        media_id = item.get("Id")
        user_id = user.get("Id")
        
        if not media_id or not user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Item.Id et User.Id sont requis"
            )
        
        # Traitement selon le type d'événement
        if event_type == "playback.start":
            # Déterminer le type de média
            item_type = item.get("Type", "Movie")
            media_type = "tv" if item_type == "Episode" else "movie"
            
            # Info épisode si série
            episode_info = None
            if item_type == "Episode":
                season = item.get("ParentIndexNumber", 0)
                episode = item.get("IndexNumber", 0)
                episode_info = f"S{season:02d}E{episode:02d}"
            
            # Extraire la qualité vidéo depuis les MediaStreams
            media_streams = item.get("MediaStreams", [])
            video_stream = next((s for s in media_streams if s.get("Type") == "Video"), {})
            video_height = video_stream.get("Height", 0)
            
            # Mapper la qualité
            quality_map = {
                2160: "FOUR_K_HDR",
                1080: "FULL_HD",
                720: "HD",
                480: "SD"
            }
            video_quality = quality_map.get(video_height, "UNKNOWN")
            
            # Codec vidéo source
            video_codec_source = video_stream.get("Codec", "unknown")
            
            # Déterminer si c'est du transcodage
            play_method = play_state.get("PlayMethod", "DirectPlay")
            is_transcoding = play_method == "Transcode"
            is_direct_playing = play_method == "DirectPlay"
            
            # Codec cible si transcodage
            video_codec_target = None
            if is_transcoding:
                video_codec_target = "h264"  # Par défaut pour le transcodage
            
            # Durée en secondes
            run_time_ticks = item.get("RunTimeTicks", 0)
            duration_seconds = run_time_ticks // 10000000 if run_time_ticks else None
            
            # Déterminer le type d'appareil
            device_name = session.get("DeviceName", "Unknown")
            client_name = session.get("Client", "Unknown")
            
            # Mapper vers DeviceType
            device_type = "WEB_BROWSER"  # Par défaut
            if "Chrome" in device_name or "Firefox" in device_name or "Safari" in device_name:
                device_type = "WEB_BROWSER"
            elif "Android" in device_name or "iOS" in device_name:
                device_type = "MOBILE"
            elif "TV" in device_name or "Roku" in device_name or "Fire" in device_name:
                device_type = "TV"
            
            # URL du poster : Utiliser l'URL publique de Jellyfin
            poster_url = None
            if item.get("ImageTags", {}).get("Primary"):
                # Configuration de l'URL publique Jellyfin
                jellyfin_url = getattr(settings, 'JELLYFIN_PUBLIC_URL', 'https://changeme.com')
                poster_url = f"{jellyfin_url}/Items/{media_id}/Images/Primary"
            
            session_data = {
                "media_id": media_id,
                "media_title": item.get("Name", "Unknown"),
                "media_type": media_type,
                "media_year": item.get("ProductionYear"),
                "episode_info": episode_info,
                "poster_url": poster_url,
                "user_id": user_id,
                "user_name": user.get("Name", "Unknown"),
                "device_name": device_name,
                "client_name": client_name,
                "video_quality": video_quality,
                "is_transcoding": is_transcoding,
                "is_direct_playing": is_direct_playing,
                "transcoding_progress": 0,
                "transcoding_speed": None,
                "video_codec_source": video_codec_source,
                "video_codec_target": video_codec_target,
                "duration_seconds": duration_seconds
            }
            
            # Recherche du LibraryItem correspondant
            library_item = None
            if media_type == "movie":
                library_item = db.query(LibraryItem).filter(
                    LibraryItem.title == item.get("Name"),
                    LibraryItem.media_type == MediaType.MOVIE,
                    LibraryItem.year == item.get("ProductionYear")
                ).first()
            elif media_type == "tv":
                series_name = item.get("SeriesName")
                if series_name:
                    library_item = db.query(LibraryItem).filter(
                        LibraryItem.title == series_name,
                        LibraryItem.media_type == MediaType.TV
                    ).first()

            if library_item:
                session_data["library_item_id"] = library_item.id

            session = AnalyticsService.start_session(db, session_data)
            logger.info(f"✅ Session créée : {session.id} - {session.media_title}")
            return {"status": "success", "session_id": session.id, "event": event_type}
        
        elif event_type == "playback.stop":
            # Position de lecture en secondes
            playback_position_ticks = play_state.get("PositionTicks", 0)
            watched_seconds = playback_position_ticks // 10000000 if playback_position_ticks else 0
            
            session = AnalyticsService.stop_session(db, media_id, user_id, watched_seconds)
            
            if session:
                logger.info(f"✅ Session arrêtée : {session.id} - {session.media_title} ({watched_seconds}s)")
                return {"status": "success", "session_id": session.id, "event": event_type}
            else:
                logger.warning(f"⚠️  Aucune session active trouvée pour media_id={media_id}, user_id={user_id}")
                return {"status": "no_active_session", "event": event_type}
        
        elif event_type == "playback.pause":
            session = AnalyticsService.pause_session(db, media_id, user_id)
            if session:
                logger.info(f"⏸️  Session mise en pause : {session.id}")
            return {"status": "success", "session_id": session.id if session else None, "event": event_type}
        
        elif event_type == "playback.unpause":
            session = AnalyticsService.resume_session(db, media_id, user_id)
            if session:
                logger.info(f"▶️  Session reprise : {session.id}")
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
            hours = stat.total_watched_seconds // 3600
            minutes = (stat.total_watched_seconds % 3600) // 60
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
