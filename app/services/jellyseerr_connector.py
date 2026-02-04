from typing import List, Dict, Any
from app.services.base_connector import BaseConnector


class JellyseerrConnector(BaseConnector):
    """Connecteur pour l'API Jellyseerr"""
    
    def _get_headers(self) -> Dict[str, str]:
        """Headers spécifiques à Jellyseerr"""
        return {
            **super()._get_headers(),
            "X-Api-Key": self.api_key
        }
    
    async def test_connection(self) -> tuple[bool, str]:
        """Tester la connexion à Jellyseerr"""
        try:
            response = await self._get("/api/v1/status")
            version = response.get("version", "unknown")
            return True, f"Connecté à Jellyseerr v{version}"
        except Exception as e:
            return False, f"Erreur de connexion: {str(e)}"
    
    async def get_requests(self, limit: int = 50, status: str = "pending") -> List[Dict[str, Any]]:
        """
        Récupérer les demandes de médias
        
        Args:
            limit: Nombre maximum de requêtes
            status: Statut des requêtes (pending, approved, declined)
            
        Returns:
            Liste des demandes
        """
        try:
            params = {
                "take": limit,
                "skip": 0,
                "filter": status
            }
            
            response = await self._get("/api/v1/request", params=params)
            return response.get("results", [])
        except Exception as e:
            print(f"❌ Erreur récupération requêtes Jellyseerr: {e}")
            return []
    
    async def approve_request(self, request_id: int) -> Dict[str, Any]:
        """
        Approuver une demande
        
        Args:
            request_id: ID de la demande
            
        Returns:
            Réponse de l'API
        """
        try:
            response = await self._post(f"/api/v1/request/{request_id}/approve")
            return response
        except Exception as e:
            print(f"❌ Erreur approbation requête: {e}")
            return {}
    
    async def decline_request(self, request_id: int) -> Dict[str, Any]:
        """
        Refuser une demande
        
        Args:
            request_id: ID de la demande
            
        Returns:
            Réponse de l'API
        """
        try:
            response = await self._post(f"/api/v1/request/{request_id}/decline")
            return response
        except Exception as e:
            print(f"❌ Erreur refus requête: {e}")
            return {}
    
    async def get_statistics(self) -> Dict[str, Any]:
        """
        Récupérer les statistiques des demandes
        
        Returns:
            Statistiques
        """
        try:
            all_requests = await self.get_requests(limit=1000, status="all")
            
            total = len(all_requests)
            pending = sum(1 for r in all_requests if r.get("status") == 1)  # 1 = pending
            approved = sum(1 for r in all_requests if r.get("status") == 2)  # 2 = approved
            declined = sum(1 for r in all_requests if r.get("status") == 3)  # 3 = declined
            
            return {
                "total": total,
                "pending": pending,
                "approved": approved,
                "declined": declined
            }
        except Exception as e:
            print(f"❌ Erreur récupération stats Jellyseerr: {e}")
            return {}
