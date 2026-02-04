from typing import List, Dict, Any
from datetime import datetime, timedelta, timezone
from app.services.base_connector import BaseConnector


class SonarrConnector(BaseConnector):
    """Connecteur pour l'API Sonarr"""
    
    def _get_headers(self) -> Dict[str, str]:
        """Headers spécifiques à Sonarr"""
        return {
            **super()._get_headers(),
            "X-Api-Key": self.api_key
        }
    
    async def test_connection(self) -> tuple[bool, str]:
        """Tester la connexion à Sonarr"""
        try:
            response = await self._get("/api/v3/system/status")
            version = response.get("version", "unknown")
            return True, f"Connecté à Sonarr v{version}"
        except Exception as e:
            return False, f"Erreur de connexion: {str(e)}"
    
    async def get_series(self) -> List[Dict[str, Any]]:
        """
        Récupérer toutes les séries
        
        Returns:
            Liste des séries avec leurs détails
        """
        try:
            series = await self._get("/api/v3/series")
            return series
        except Exception as e:
            print(f"❌ Erreur récupération séries Sonarr: {e}")
            return []
    
    async def get_calendar(self, days_ahead: int = 30) -> List[Dict[str, Any]]:
        """
        Récupérer le calendrier des épisodes à venir
        
        Args:
            days_ahead: Nombre de jours à venir
            
        Returns:
            Liste des épisodes à venir
        """
        try:
            start_date = datetime.now(timezone.utc).date()
            end_date = start_date + timedelta(days=days_ahead)
            
            params = {
                "start": start_date.isoformat(),
                "end": end_date.isoformat()
            }
            
            calendar = await self._get("/api/v3/calendar", params=params)
            return calendar
        except Exception as e:
            print(f"❌ Erreur récupération calendrier Sonarr: {e}")
            return []
    
    async def get_recent_additions(self, days: int = 7) -> List[Dict[str, Any]]:
        """
        Récupérer les séries récemment ajoutées
        
        Args:
            days: Nombre de jours en arrière
            
        Returns:
            Liste des séries récemment ajoutées
        """
        try:
            series = await self.get_series()
            
            # Filtrer par date d'ajout - FIX: utiliser timezone-aware datetime
            cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
            recent = []
            
            for serie in series:
                if not serie.get("added"):
                    continue
                
                try:
                    # Convertir la date en timezone-aware
                    added_dt = datetime.fromisoformat(serie["added"].replace("Z", "+00:00"))
                    if added_dt > cutoff_date:
                        recent.append(serie)
                except (ValueError, AttributeError) as e:
                    # Ignorer les films avec des dates invalides
                    continue


            # Trier par date d'ajout
            recent.sort(key=lambda x: x.get("added", ""), reverse=True)
            
            return recent
        except Exception as e:
            print(f"❌ Erreur récupération séries récentes: {e}")
            return []
    
    async def get_statistics(self) -> Dict[str, Any]:
        """
        Récupérer les statistiques Sonarr
        
        Returns:
            Statistiques (séries, épisodes, etc.)
        """
        try:
            series = await self.get_series()
            
            total_series = len(series)
            monitored_series = sum(1 for s in series if s.get("monitored"))
            
            total_episodes = sum(s.get("statistics", {}).get("episodeCount", 0) for s in series)
            downloaded_episodes = sum(s.get("statistics", {}).get("episodeFileCount", 0) for s in series)
            missing_episodes = total_episodes - downloaded_episodes
            
            return {
                "total_series": total_series,
                "monitored_series": monitored_series,
                "total_episodes": total_episodes,
                "downloaded_episodes": downloaded_episodes,
                "missing_episodes": missing_episodes
            }
        except Exception as e:
            print(f"❌ Erreur récupération stats Sonarr: {e}")
            return {}
