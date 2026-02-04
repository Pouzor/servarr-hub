from typing import List, Dict, Any
from datetime import datetime, timedelta
from app.services.base_connector import BaseConnector


class JellyfinConnector(BaseConnector):
    """Connecteur pour l'API Jellyfin"""
    
    def _get_headers(self) -> Dict[str, str]:
        """Headers spécifiques à Jellyfin"""
        return {
            **super()._get_headers(),
            "X-Emby-Token": self.api_key
        }
    
    async def test_connection(self) -> tuple[bool, str]:
        """Tester la connexion à Jellyfin"""
        try:
            response = await self._get("/System/Info/Public")
            version = response.get("Version", "unknown")
            return True, f"Connecté à Jellyfin v{version}"
        except Exception as e:
            return False, f"Erreur de connexion: {str(e)}"
    
    async def get_users(self) -> List[Dict[str, Any]]:
        """
        Récupérer tous les utilisateurs
        
        Returns:
            Liste des utilisateurs
        """
        try:
            users = await self._get("/Users")
            return users
        except Exception as e:
            print(f"❌ Erreur récupération utilisateurs Jellyfin: {e}")
            return []
    
    async def get_library_items(self) -> Dict[str, Any]:
        """
        Récupérer le nombre d'items par type dans la bibliothèque
        
        Returns:
            Statistiques de la bibliothèque
        """
        try:
            # Récupérer les items de la bibliothèque
            response = await self._get("/Items/Counts")
            
            return {
                "movies": response.get("MovieCount", 0),
                "series": response.get("SeriesCount", 0),
                "episodes": response.get("EpisodeCount", 0),
                "albums": response.get("AlbumCount", 0),
                "songs": response.get("SongCount", 0)
            }
        except Exception as e:
            print(f"❌ Erreur récupération items Jellyfin: {e}")
            return {}
    
    async def get_recent_items(self, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Récupérer les items récemment ajoutés
        
        Args:
            limit: Nombre maximum d'items à retourner
            
        Returns:
            Liste des items récents
        """
        try:
            params = {
                "Limit": limit,
                "Recursive": True,
                "SortBy": "DateCreated",
                "SortOrder": "Descending",
                "IncludeItemTypes": "Movie,Series"
            }
            
            response = await self._get("/Items", params=params)
            return response.get("Items", [])
        except Exception as e:
            print(f"❌ Erreur récupération items récents Jellyfin: {e}")
            return []
    
    async def get_playback_stats(self, days: int = 30) -> Dict[str, Any]:
        """
        Récupérer les statistiques de lecture
        
        Args:
            days: Période en jours
            
        Returns:
            Statistiques de playback
        """
        try:
            # Note: Jellyfin n'a pas d'endpoint natif pour les stats détaillées
            # On peut utiliser le plugin "Playback Reporting" ou construire depuis les sessions
            users = await self.get_users()
            
            return {
                "total_users": len(users),
                "active_users": len([u for u in users if not u.get("Policy", {}).get("IsDisabled", False)]),
                "period_days": days
            }
        except Exception as e:
            print(f"❌ Erreur récupération stats playback: {e}")
            return {}
