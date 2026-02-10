"""
Routes pour gérer les torrents (qBittorrent)
"""

from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import verify_api_key
from app.db import get_db
from app.models.models import ServiceConfiguration
from app.services.connector_factory import create_connector
from app.services.torrent_enrichment_service import TorrentEnrichmentService

router = APIRouter(prefix="/api/torrents", tags=["torrents"])


@router.get("/{torrent_hash}")
async def get_torrent_info(
    torrent_hash: str, db: Session = Depends(get_db), _: str = Depends(verify_api_key)
) -> dict[str, Any]:
    """
    Récupère les informations d'un torrent depuis qBittorrent

    Args:
        torrent_hash: Hash du torrent

    Returns:
        Informations du torrent
    """
    # Récupérer la config qBittorrent
    qbt_service = (
        db.query(ServiceConfiguration)
        .filter(ServiceConfiguration.service_name == "qbittorrent", ServiceConfiguration.is_active == True)
        .first()
    )

    if not qbt_service:
        raise HTTPException(status_code=404, detail="Service qBittorrent non configuré")

    try:
        # Créer le connector
        connector = create_connector(qbt_service)

        # Récupérer les infos
        torrent_info = await connector.get_torrent_info(torrent_hash)

        # Fermer la session
        await connector.close()

        if not torrent_info:
            raise HTTPException(status_code=404, detail=f"Torrent {torrent_hash} non trouvé")

        return torrent_info

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération du torrent : {str(e)}") from e


@router.post("/enrich")
async def enrich_library_items(
    limit: int | None = None, db: Session = Depends(get_db), _: str = Depends(verify_api_key)
) -> dict[str, Any]:
    """
    Enrichit les library_items avec les données qBittorrent

    Args:
        limit: Nombre maximum d'items à traiter (optionnel)

    Returns:
        Statistiques de l'enrichissement
    """
    service = TorrentEnrichmentService(db)
    stats = await service.enrich_all_items(limit=limit)
    return stats


@router.post("/enrich/recent")
async def enrich_recent_items(
    days: int = 7, db: Session = Depends(get_db), _: str = Depends(verify_api_key)
) -> dict[str, Any]:
    """
    Enrichit les items récents avec les données qBittorrent

    Args:
        days: Nombre de jours en arrière (défaut: 7)

    Returns:
        Statistiques de l'enrichissement
    """
    service = TorrentEnrichmentService(db)
    stats = await service.enrich_recent_items(days=days)
    return stats
