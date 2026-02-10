from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.orm import Session

from app.api.schemas import SyncMetadataResponse
from app.db import get_db
from app.models import SyncMetadata
from app.schedulers.sync_service import SyncService

router = APIRouter(prefix="/sync", tags=["Synchronization"])


@router.post("/trigger")
async def trigger_sync(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """Déclencher manuellement une synchronisation complète"""

    async def run_sync():
        sync_service = SyncService(db)
        await sync_service.sync_all()

    background_tasks.add_task(run_sync)

    return {"message": "Synchronisation lancée en arrière-plan", "status": "started"}


@router.post("/trigger/{service_name}")
async def trigger_service_sync(service_name: str, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """Déclencher la synchronisation d'un service spécifique"""

    async def run_service_sync():
        sync_service = SyncService(db)

        if service_name == "radarr":
            await sync_service.sync_radarr()
        elif service_name == "sonarr":
            await sync_service.sync_sonarr()
        elif service_name == "jellyfin":
            await sync_service.sync_jellyfin()
        elif service_name == "jellyseerr":
            await sync_service.sync_jellyseerr()

    background_tasks.add_task(run_service_sync)

    return {"message": f"Synchronisation {service_name} lancée", "status": "started"}


@router.get("/status", response_model=list[SyncMetadataResponse])
async def get_sync_status(db: Session = Depends(get_db)):
    """Récupérer le statut des dernières synchronisations"""
    sync_metadata = db.query(SyncMetadata).all()
    return sync_metadata
