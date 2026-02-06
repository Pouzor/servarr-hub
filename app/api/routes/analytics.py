"""
Routes API pour les analytics et webhooks
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import Dict, Any
from app.db import get_db
from app.services.analytics_service import AnalyticsService
from app.core.security import verify_api_key
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.post("/webhook/playback", status_code=status.HTTP_200_OK)
async def receive_playback_webhook(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Endpoint pour recevoir les webhooks de lecture depuis Jellyfin/Plex
    
    Événements supportés :
    - playback.start : Début de lecture
    - playback.stop : Fin de lecture
    - playback.pause : Mise en pause
    - playback.unpause : Reprise de lecture
    """
    try:
        # Récupérer le payload
        payload = await request.json()
        
        event_type = payload.get("event")
        data = payload.get("data", {})
        
        logger.info(f"📥 Webhook reçu : {event_type}")
        
        # Extraction des données communes
        media_id = data.get("media_id") or data.get("item_id")
        user_id = data.get("user_id")
        
        if not media_id or not user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="media_id et user_id sont requis"
            )
        
        # Traitement selon le type d'événement
        if event_type == "playback.start":
            session_data = {
                "media_id": media_id,
                "media_title": data.get("media_title") or data.get("title"),
                "media_type": data.get("media_type", "movie"),
                "media_year": data.get("year"),
                "episode_info": data.get("episode_info"),
                "poster_url": data.get("poster_url") or data.get("image_url"),
                "user_id": user_id,
                "user_name": data.get("user_name") or data.get("username"),
                "device_name": data.get("device_name"),
                "client_name": data.get("client_name") or data.get("player_name"),
                "video_quality": data.get("video_quality") or data.get("quality"),
                "is_transcoding": data.get("is_transcoding", False),
                "is_direct_playing": data.get("is_direct_playing", True),
                "transcoding_progress": data.get("transcoding_progress", 0),
                "transcoding_speed": data.get("transcoding_speed"),
                "video_codec_source": data.get("video_codec_source"),
                "video_codec_target": data.get("video_codec_target"),
                "duration_seconds": data.get("duration_seconds") or data.get("duration")
            }
            
            session = AnalyticsService.start_session(db, session_data)
            return {"status": "success", "session_id": session.id, "event": event_type}
        
        elif event_type == "playback.stop":
            watched_seconds = data.get("watched_seconds") or data.get("playback_position")
            session = AnalyticsService.stop_session(db, media_id, user_id, watched_seconds)
            
            if session:
                return {"status": "success", "session_id": session.id, "event": event_type}
            else:
                return {"status": "no_active_session", "event": event_type}
        
        elif event_type == "playback.pause":
            session = AnalyticsService.pause_session(db, media_id, user_id)
            return {"status": "success", "session_id": session.id if session else None, "event": event_type}
        
        elif event_type == "playback.unpause" or event_type == "playback.resume":
            session = AnalyticsService.resume_session(db, media_id, user_id)
            return {"status": "success", "session_id": session.id if session else None, "event": event_type}
        
        else:
            logger.warning(f"⚠️  Événement non supporté : {event_type}")
            return {"status": "ignored", "event": event_type}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erreur lors du traitement du webhook : {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur serveur : {str(e)}"
        )


@router.get("/sessions/active")
async def get_active_sessions(
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    """Récupère toutes les sessions de lecture actives"""
    try:
        sessions = AnalyticsService.get_active_sessions(db)
        
        return {
            "count": len(sessions),
            "sessions": [
                {
                    "id": s.id,
                    "media_title": s.media_title,
                    "media_type": s.media_type.value,
                    "user_name": s.user_name,
                    "device_type": s.device_type.value,
                    "video_quality": s.video_quality.value,
                    "playback_method": s.playback_method.value,
                    "transcoding_progress": s.transcoding_progress,
                    "start_time": s.start_time.isoformat(),
                    "status": s.status.value
                }
                for s in sessions
            ]
        }
    except Exception as e:
        logger.error(f"❌ Erreur lors de la récupération des sessions actives : {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
