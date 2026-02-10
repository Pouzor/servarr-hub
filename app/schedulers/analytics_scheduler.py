"""
Scheduler pour les tâches analytics
"""

import logging
import threading
import time
from datetime import datetime, timedelta

from app.db import SessionLocal
from app.services.analytics_service import AnalyticsService
from app.services.metrics_service import MetricsService

logger = logging.getLogger(__name__)


class AnalyticsScheduler:
    """Scheduler pour les tâches analytics en arrière-plan"""

    def __init__(self):
        self.running = False
        self.metrics_thread = None
        self.cleanup_thread = None

    def start(self):
        """Démarre tous les schedulers analytics"""
        if self.running:
            logger.warning("⚠️  Analytics scheduler déjà en cours")
            return

        self.running = True

        # Thread 1 : Capture des métriques serveur (toutes les 30 secondes)
        self.metrics_thread = threading.Thread(target=self._metrics_loop, daemon=True)
        self.metrics_thread.start()
        logger.info("✅ Metrics scheduler démarré (intervalle: 30s)")

        # Thread 2 : Nettoyage et agrégations (toutes les heures)
        self.cleanup_thread = threading.Thread(target=self._cleanup_loop, daemon=True)
        self.cleanup_thread.start()
        logger.info("✅ Cleanup scheduler démarré (intervalle: 1h)")

    def stop(self):
        """Arrête tous les schedulers"""
        self.running = False
        logger.info("🛑 Analytics scheduler arrêté")

    def _metrics_loop(self):
        """Boucle pour capturer les métriques serveur"""
        while self.running:
            try:
                db = SessionLocal()
                try:
                    MetricsService.capture_metrics(db)
                finally:
                    db.close()

                # Attendre 30 secondes
                time.sleep(30)

            except Exception as e:
                logger.error(f"❌ Erreur dans metrics_loop : {e}")
                time.sleep(30)

    def _cleanup_loop(self):
        """Boucle pour le nettoyage et les agrégations"""
        while self.running:
            try:
                db = SessionLocal()
                try:
                    # 1. Nettoyer les sessions orphelines (actives depuis > 24h)
                    AnalyticsService.cleanup_orphan_sessions(db, timeout_hours=24)

                    # 2. Mettre à jour les device statistics d'hier
                    yesterday = (datetime.utcnow() - timedelta(days=1)).date()
                    AnalyticsService.update_device_statistics(db, yesterday)

                    # 3. Nettoyer les vieilles métriques (garder 7 jours)
                    MetricsService.cleanup_old_metrics(db, keep_days=7)

                finally:
                    db.close()

                # Attendre 1 heure
                time.sleep(3600)

            except Exception as e:
                logger.error(f"❌ Erreur dans cleanup_loop : {e}")
                time.sleep(3600)


# Instance globale du scheduler
analytics_scheduler = AnalyticsScheduler()
