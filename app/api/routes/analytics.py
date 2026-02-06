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
    """
    try:
        # Récupérer le payload
        payload = await request.json()
        
        # 🔍 DEBUG : Afficher le payload complet avec print()
        print("\n" + "="*60)
        print("📦 PAYLOAD COMPLET REÇU :")
        import json
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        print("="*60 + "\n")
        
        return {"status": "debug", "received": True}
    
    except Exception as e:
        print(f"❌ Erreur : {e}")
        import traceback
        print(traceback.format_exc())
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
