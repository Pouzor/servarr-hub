"""
Factory pour créer les connectors selon le type de service
"""

from app.models import ServiceConfiguration
from app.services.jellyfin_connector import JellyfinConnector
from app.services.jellyseerr_connector import JellyseerrConnector
from app.services.qbittorrent_connector import QBittorrentConnector
from app.services.radarr_connector import RadarrConnector
from app.services.sonarr_connector import SonarrConnector


def create_connector(service: ServiceConfiguration):
    """
    Crée le bon connector selon le type de service

    Args:
        service: Configuration du service

    Returns:
        Instance du connector approprié

    Raises:
        ValueError: Si le type de service n'est pas supporté
    """
    service_type = service.service_name.lower()

    if service_type == "jellyfin":
        return JellyfinConnector(base_url=service.url, api_key=service.api_key, port=service.port)

    elif service_type == "jellyseerr":
        return JellyseerrConnector(base_url=service.url, api_key=service.api_key, port=service.port)

    elif service_type == "sonarr":
        return SonarrConnector(base_url=service.url, api_key=service.api_key, port=service.port)

    elif service_type == "radarr":
        return RadarrConnector(base_url=service.url, api_key=service.api_key, port=service.port)

    elif service_type == "qbittorrent":
        if not service.username or not service.password:
            raise ValueError("qBittorrent nécessite username et password")

        return QBittorrentConnector(
            base_url=service.url, username=service.username, password=service.password, port=service.port
        )

    else:
        raise ValueError(f"Type de service non supporté : {service_type}")
