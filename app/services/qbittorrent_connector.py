"""
Connecteur pour qBittorrent
"""

import logging
from typing import Any

import aiohttp

from app.services.base_connector import BaseConnector

logger = logging.getLogger(__name__)


class QBittorrentConnector(BaseConnector):
    """Connecteur pour interagir avec l'API qBittorrent"""

    def __init__(self, base_url: str, username: str, password: str, port: int | None = None):
        """
        Initialise le connecteur qBittorrent

        Args:
            base_url: URL de base de qBittorrent (ex: http://192.168.1.58)
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
        self.session: aiohttp.ClientSession | None = None
        self._authenticated = False

    async def _ensure_session(self):
        """Crée une session HTTP si elle n'existe pas"""
        if self.session is None or self.session.closed:
            # Créer une session avec gestion automatique des cookies
            jar = aiohttp.CookieJar(unsafe=True)  # unsafe=True pour accepter les cookies de toutes les IPs
            self.session = aiohttp.ClientSession(cookie_jar=jar)
            self._authenticated = False

    async def _ensure_authenticated(self):
        """S'assure que la session est authentifiée"""
        if not self._authenticated:
            await self.login()

    async def login(self) -> bool:
        """
        Authentification sur qBittorrent

        Returns:
            True si authentification réussie, False sinon
        """
        try:
            await self._ensure_session()

            login_url = f"{self.base_url}/api/v2/auth/login"

            data = aiohttp.FormData()
            data.add_field("username", self.username)
            data.add_field("password", self.password)

            logger.info(f"🔐 Tentative de connexion à {login_url}")

            async with self.session.post(login_url, data=data) as response:
                text = await response.text()
                logger.info(f"📥 Réponse login : status={response.status}, body={text}")

                if response.status == 200 and text.strip() == "Ok.":
                    # Vérifier qu'on a bien reçu un cookie SID
                    cookies = self.session.cookie_jar.filter_cookies(self.base_url)
                    logger.info(f"🍪 Cookies reçus : {cookies}")

                    self._authenticated = True
                    logger.info("✅ Authentification qBittorrent réussie")
                    return True
                else:
                    logger.error(f"❌ Authentification échouée : status={response.status}, body={text}")
                    return False

        except Exception as e:
            logger.error(f"❌ Erreur lors de l'authentification qBittorrent : {e}")
            return False

    async def get_torrent_info(self, torrent_hash: str) -> dict[str, Any] | None:
        """
        Récupère les informations d'un torrent par son hash

        Args:
            torrent_hash: Hash du torrent

        Returns:
            Dictionnaire avec les infos du torrent ou None
        """
        try:
            await self._ensure_authenticated()

            # Récupérer les infos du torrent
            url = f"{self.base_url}/api/v2/torrents/info"
            params = {"hashes": torrent_hash}

            logger.info(f"🔍 Récupération infos torrent : {url}?hashes={torrent_hash}")

            async with self.session.get(url, params=params) as response:
                logger.info(f"📥 Réponse get_torrent_info : status={response.status}")

                if response.status == 200:
                    torrents = await response.json()

                    if torrents and len(torrents) > 0:
                        torrent = torrents[0]

                        # Formater les données
                        return {
                            "hash": torrent.get("hash"),
                            "name": torrent.get("name"),
                            "status": self._map_status(torrent.get("state")),
                            "ratio": round(torrent.get("ratio", 0), 2),
                            "tags": torrent.get("tags", "").split(",") if torrent.get("tags") else [],
                            "seeding_time": torrent.get("seeding_time", 0),  # en secondes
                            "download_date": torrent.get("completion_on"),  # timestamp
                            "size": torrent.get("size", 0),
                            "progress": round(torrent.get("progress", 0) * 100, 1),
                        }
                    else:
                        logger.warning(f"⚠️  Torrent {torrent_hash} non trouvé")
                        return None
                elif response.status == 403:
                    logger.error("❌ 403 Forbidden - Session expirée ?")
                    # Réessayer avec une nouvelle authentification
                    self._authenticated = False
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
            "uploading": "seeding",
            "stalledUP": "seeding",
            "queuedUP": "seeding",
            "downloading": "downloading",
            "stalledDL": "downloading",
            "queuedDL": "downloading",
            "pausedUP": "paused",
            "pausedDL": "paused",
            "error": "error",
            "missingFiles": "error",
            "checkingUP": "completed",
            "checkingDL": "completed",
        }

        return state_mapping.get(qbt_state, "unknown")

    async def test_connection(self) -> tuple[bool, str]:
        """
        Teste la connexion à qBittorrent

        Returns:
            Tuple (succès, message)
        """
        try:
            await self._ensure_session()

            # Tenter l'authentification
            if not await self.login():
                return False, "Échec de l'authentification. Vérifiez username/password."

            # Récupérer la version de qBittorrent
            url = f"{self.base_url}/api/v2/app/version"

            logger.info(f"🔍 Test connexion : {url}")

            async with self.session.get(url) as response:
                logger.info(f"📥 Réponse version : status={response.status}")

                if response.status == 200:
                    version = await response.text()
                    return True, f"Connecté à qBittorrent v{version}"
                else:
                    body = await response.text()
                    return False, f"Erreur HTTP {response.status} : {body}"

        except Exception as e:
            return False, f"Erreur de connexion : {str(e)}"

    async def close(self):
        """Ferme la session HTTP"""
        if self.session and not self.session.closed:
            await self.session.close()
            logger.info("🔒 Session qBittorrent fermée")
