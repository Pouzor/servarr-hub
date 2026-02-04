from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.schedulers.sync_service import SyncService
import asyncio


class AppScheduler:
    """Gestionnaire de tâches planifiées"""
    
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.is_running = False
    
    async def run_sync_job(self):
        """Tâche de synchronisation à exécuter"""
        db = SessionLocal()
        try:
            sync_service = SyncService(db)
            await sync_service.sync_all()
        except Exception as e:
            print(f"❌ Erreur lors de la synchro planifiée: {e}")
        finally:
            db.close()
    
    def start(self, interval_minutes: int = 15):
        """
        Démarrer le scheduler
        
        Args:
            interval_minutes: Intervalle entre chaque synchro (défaut: 15 min)
        """
        if self.is_running:
            print("⚠️  Scheduler déjà démarré")
            return
        
        # Ajouter le job de synchronisation
        self.scheduler.add_job(
            self.run_sync_job,
            trigger=IntervalTrigger(minutes=interval_minutes),
            id="sync_job",
            name="Synchronisation des données",
            replace_existing=True
        )
        
        # Démarrer le scheduler
        self.scheduler.start()
        self.is_running = True
        
        print(f"⏰ Scheduler démarré (intervalle: {interval_minutes} minutes)")
    
    def stop(self):
        """Arrêter le scheduler"""
        if not self.is_running:
            return
        
        self.scheduler.shutdown()
        self.is_running = False
        print("⏸️  Scheduler arrêté")


# Instance globale du scheduler
app_scheduler = AppScheduler()
