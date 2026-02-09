"""
Connecteur pour qBittorrent
"""
import aiohttp
import logging
from typing import Optional, Dict, Any, Tuple
from app.services.base_connector import BaseConnector

logger = logging.getLogger(__name__)


class QBittorrentConnector(BaseConnector):
    """Connecteur pour interagir avec l'API qBittorrent"""
    
    def __init__(self, base_url: str, username: str, password: str, port: Optional[int] = None):
        """
        Initialise le connecteur qBittorrent
        
        Args:
            base_url: URL de base de qBittorrent (ex: http://192.168.0.22)
            username: Nom d'utilisateur
            password: Mot de passe
            port: Port (optionnel, ex: 8090)
        """
        # Construire l'URL complète
        if port:
            full_url = f"{base_url}:{port}"
        else:
            full_url = base_url
        
        super().__init__(base_url=full_url, api_key="")  # api_key vide car non utilisé
        
        self.username = username
        self.password = password
        self.session: Optional[aiohttp.ClientSession] = None
        self.cookies: Optional[Dict[str, str]] = None
    
    async def _ensure_session(self):
        """Crée une session HTTP si elle n'existe pas"""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
    
    async def login(self) -> bool:
        """
        Authentification sur qBittorrent
        
        Returns:
            True si authentification réussie, False sinon
        """
        try:
            await self._ensure_session()
            
            login_url = f"{self.base_url}/api/v2/auth/login"
            
            data = {
                'username': self.username,
                'password': self.password
            }
            
            async with self.session.post(login_url, data=data) as response:
                if response.status == 200:
                    text = await response.text()
                    if text == "Ok.":
                        # Sauvegarder les cookies de session
                        self.cookies = {cookie.key: cookie.value for cookie in self.session.cookie_jar}
                        logger.info("✅ Authentification qBittorrent réussie")
                        return True
                    else:
                        logger.error(f"❌ Authentification échouée : {text}")
                        return False
                else:
                    logger.error(f"❌ Erreur HTTP {response.status}")
                    return False
                    
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'authentification qBittorrent : {e}")
            return False
    
    async def get_torrent_info(self, torrent_hash: str) -> Optional[Dict[str, Any]]:
        """
        Récupère les informations d'un torrent par son hash
        
        Args:
            torrent_hash: Hash du torrent
            
        Returns:
            Dictionnaire avec les infos du torrent ou None
        """
        try:
            # S'assurer d'être authentifié
            if not self.cookies:
                if not await self.login():
                    return None
            
            await self._ensure_session()
            
            # Récupérer les infos du torrent
            url = f"{self.base_url}/api/v2/torrents/info"
            params = {'hashes': torrent_hash}
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    torrents = await response.json()
                    
                    if torrents and len(torrents) > 0:
                        torrent = torrents[0]
                        
                        # Formater les données
                        return {
                            'hash': torrent.get('hash'),
                            'name': torrent.get('name'),
                            'status': self._map_status(torrent.get('state')),
                            'ratio': round(torrent.get('ratio', 0), 2),
                            'tags': torrent.get('tags', '').split(',') if torrent.get('tags') else [],
                            'seeding_time': torrent.get('seeding_time', 0),  # en secondes
                            'download_date': torrent.get('completion_on'),  # timestamp
                            'size': torrent.get('size', 0),
                            'progress': round(torrent.get('progress', 0) * 100, 1)
                        }
                    else:
                        logger.warning(f"⚠️  Torrent {torrent_hash} non trouvé")
                        return None
                else:
                    logger.error(f"❌ Erreur HTTP {response.status}")
                    return None
                    
        except Exception as e:
            logger.error(f"❌ Erreur lors de la récupération du torrent : {e}")
            return None
    
    def _map_status(self, qbt_state: str) -> str:
        """
        Mappe les états qBittorrent vers des états simplifiés
        
        Args:
            qbt_state: État qBittorrent (ex: "uploading", "downloading", etc.)
            
        Returns:
            État simplifié : "seeding", "downloading", "paused", "completed", "error"
        """
        state_mapping = {
            'uploading': 'seeding',
            'stalledUP': 'seeding',
            'queuedUP': 'seeding',
            'downloading': 'downloading',
            'stalledDL': 'downloading',
            'queuedDL': 'downloading',
            'pausedUP': 'paused',
            'pausedDL': 'paused',
            'error': 'error',
            'missingFiles': 'error',
            'checkingUP': 'completed',
            'checkingDL': 'completed'
        }
        
        return state_mapping.get(qbt_state, 'unknown')
    
    async def test_connection(self) -> Tuple[bool, str]:
        """
        Teste la connexion à qBittorrent
        
        Returns:
            Tuple (succès, message)
        """
        try:
            # Tenter l'authentification
            if await self.login():
                # Récupérer la version de qBittorrent
                await self._ensure_session()
                
                url = f"{self.base_url}/api/v2/app/version"
                
                async with self.session.get(url) as response:
                    if response.status == 200:
                        version = await response.text()
                        return True, f"Connecté à qBittorrent v{version}"
                    else:
                        return False, f"Erreur HTTP {response.status}"
            else:
                return False, "Échec de l'authentification. Vérifiez username/password."
                
        except Exception as e:
            return False, f"Erreur de connexion : {str(e)}"
    
    async def close(self):
        """Ferme la session HTTP"""
        if self.session and not self.session.closed:
            await self.session.close()
            logger.info("🔒 Session qBittorrent fermée")
