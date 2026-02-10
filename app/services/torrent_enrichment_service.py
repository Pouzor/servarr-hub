"""
Service pour enrichir les library_items avec les données qBittorrent
"""

import logging
from datetime import datetime

from sqlalchemy.orm import Session

from app.models.models import LibraryItem, ServiceConfiguration
from app.services.connector_factory import create_connector

logger = logging.getLogger(__name__)


class TorrentEnrichmentService:
    """Service pour enrichir les items de bibliothèque avec les données torrents"""

    def __init__(self, db: Session):
        self.db = db
        self.qbt_connector = None

    async def _get_qbt_connector(self):
        """Récupère ou crée le connector qBittorrent"""
        if self.qbt_connector is None:
            qbt_service = (
                self.db.query(ServiceConfiguration)
                .filter(ServiceConfiguration.service_name == "qbittorrent", ServiceConfiguration.is_active == True)
                .first()
            )

            if not qbt_service:
                logger.error("❌ Service qBittorrent non configuré")
                return None

            self.qbt_connector = create_connector(qbt_service)

        return self.qbt_connector

    async def enrich_item(self, item: LibraryItem) -> bool:
        """
        Enrichit un item avec les données qBittorrent

        Args:
            item: LibraryItem à enrichir

        Returns:
            True si enrichissement réussi, False sinon
        """
        if not item.torrent_hash:
            logger.warning(f"⚠️  Item {item.id} n'a pas de torrent_hash")
            return False

        try:
            connector = await self._get_qbt_connector()
            if not connector:
                return False

            # Récupérer les infos du torrent
            torrent_info = await connector.get_torrent_info(item.torrent_hash)

            if not torrent_info:
                logger.warning(f"⚠️  Torrent {item.torrent_hash} non trouvé pour item {item.id}")
                return False

            # Mettre à jour l'item
            item.torrent_info = torrent_info
            item.updated_at = datetime.utcnow()

            self.db.commit()

            logger.info(
                f"✅ Item {item.id} enrichi avec succès "
                f"(ratio: {torrent_info.get('ratio')}, status: {torrent_info.get('status')})"
            )
            return True

        except Exception as e:
            logger.error(f"❌ Erreur lors de l'enrichissement de l'item {item.id} : {e}")
            self.db.rollback()
            return False

    async def enrich_all_items(self, limit: int | None = None) -> dict:
        """
        Enrichit tous les items qui ont un torrent_hash

        Args:
            limit: Nombre maximum d'items à traiter (None = tous)

        Returns:
            Statistiques de l'enrichissement
        """
        try:
            # Récupérer les items avec un torrent_hash
            query = self.db.query(LibraryItem).filter(
                LibraryItem.torrent_hash.isnot(None), LibraryItem.torrent_hash != ""
            )

            if limit:
                query = query.limit(limit)

            items = query.all()

            logger.info(f"📊 {len(items)} items à enrichir")

            stats = {"total": len(items), "success": 0, "failed": 0, "skipped": 0}

            for item in items:
                success = await self.enrich_item(item)
                if success:
                    stats["success"] += 1
                else:
                    stats["failed"] += 1

            logger.info(f"✅ Enrichissement terminé : {stats}")

            return stats

        except Exception as e:
            logger.error(f"❌ Erreur lors de l'enrichissement global : {e}")
            return {"total": 0, "success": 0, "failed": 0, "error": str(e)}
        finally:
            # Fermer le connector
            if self.qbt_connector:
                await self.qbt_connector.close()

    async def enrich_recent_items(self, days: int = 7) -> dict:
        """
        Enrichit les items récents (ajoutés dans les X derniers jours)

        Args:
            days: Nombre de jours en arrière

        Returns:
            Statistiques de l'enrichissement
        """
        try:
            from datetime import timedelta

            cutoff_date = datetime.utcnow() - timedelta(days=days)

            items = (
                self.db.query(LibraryItem)
                .filter(
                    LibraryItem.torrent_hash.isnot(None),
                    LibraryItem.torrent_hash != "",
                    LibraryItem.created_at >= cutoff_date,
                )
                .all()
            )

            logger.info(f"📊 {len(items)} items récents à enrichir")

            stats = {"total": len(items), "success": 0, "failed": 0}

            for item in items:
                success = await self.enrich_item(item)
                if success:
                    stats["success"] += 1
                else:
                    stats["failed"] += 1

            logger.info(f"✅ Enrichissement des items récents terminé : {stats}")

            return stats

        except Exception as e:
            logger.error(f"❌ Erreur lors de l'enrichissement des items récents : {e}")
            return {"total": 0, "success": 0, "failed": 0, "error": str(e)}
        finally:
            if self.qbt_connector:
                await self.qbt_connector.close()
