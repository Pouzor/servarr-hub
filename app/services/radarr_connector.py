from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from app.services.base_connector import BaseConnector


class RadarrConnector(BaseConnector):
    """Connecteur pour l'API Radarr"""
    
    def _get_headers(self) -> Dict[str, str]:
        """Headers spécifiques à Radarr"""
        return {
            **super()._get_headers(),
            "X-Api-Key": self.api_key
        }
    
    async def test_connection(self) -> tuple[bool, str]:
        """Tester la connexion à Radarr"""
        try:
            response = await self._get("/api/v3/system/status")
            version = response.get("version", "unknown")
            return True, f"Connecté à Radarr v{version}"
        except Exception as e:
            return False, f"Erreur de connexion: {str(e)}"
    
    async def get_movies(self) -> List[Dict[str, Any]]:
        """
        Récupérer tous les films
        
        Returns:
            Liste des films avec leurs détails
        """
        try:
            movies = await self._get("/api/v3/movie")
            return movies
        except Exception as e:
            print(f"❌ Erreur récupération films Radarr: {e}")
            return []
    
    async def get_calendar(self, days_ahead: int = 30) -> List[Dict[str, Any]]:
        """
        Récupérer le calendrier des sorties
        
        Args:
            days_ahead: Nombre de jours à venir
            
        Returns:
            Liste des films à venir
        """
        try:
            start_date = datetime.now().date()
            end_date = start_date + timedelta(days=days_ahead)
            
            params = {
                "start": start_date.isoformat(),
                "end": end_date.isoformat()
            }
            
            calendar = await self._get("/api/v3/calendar", params=params)
            return calendar
        except Exception as e:
            print(f"❌ Erreur récupération calendrier Radarr: {e}")
            return []
    
    async def get_recent_additions(self, days: int = 7) -> List[Dict[str, Any]]:
        """
        Récupérer les films récemment ajoutés
        
        Args:
            days: Nombre de jours en arrière
            
        Returns:
            Liste des films récemment ajoutés
        """
        try:
            movies = await self.get_movies()
            
            # Filtrer par date d'ajout
            cutoff_date = datetime.now() - timedelta(days=days)
            recent = [
                movie for movie in movies
                if movie.get("added") and 
                datetime.fromisoformat(movie["added"].replace("Z", "+00:00")) > cutoff_date
            ]
            
            # Trier par date d'ajout (plus récent en premier)
            recent.sort(key=lambda x: x.get("added", ""), reverse=True)
            
            return recent
        except Exception as e:
            print(f"❌ Erreur récupération films récents: {e}")
            return []
    
    async def get_statistics(self) -> Dict[str, Any]:
        """
        Récupérer les statistiques Radarr
        
        Returns:
            Statistiques (nombre de films monitorés, téléchargés, etc.)
        """
        try:
            movies = await self.get_movies()
            
            total = len(movies)
            monitored = sum(1 for m in movies if m.get("monitored"))
            downloaded = sum(1 for m in movies if m.get("hasFile"))
            missing = monitored - downloaded
            
            return {
                "total": total,
                "monitored": monitored,
                "downloaded": downloaded,
                "missing": missing
            }
        except Exception as e:
            print(f"❌ Erreur récupération stats Radarr: {e}")
            return {}
