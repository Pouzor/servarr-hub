"""
Test du connector qBittorrent
"""

import asyncio

from app.services.qbittorrent_connector import QBittorrentConnector


async def test():
    connector = QBittorrentConnector(
        base_url="http://192.168.1.0",
        username="admin",
        password="",  # Ton vrai mot de passe
        port=8090,
    )

    try:
        # Test de connexion
        print("🧪 Test de connexion...")
        success, message = await connector.test_connection()
        print(f"{'✅' if success else '❌'} {message}")

        # Test de récupération d'un torrent (si tu as un hash)
        # torrent_hash = "abc123..."
        # info = await connector.get_torrent_info(torrent_hash)
        # print(f"Torrent info: {info}")

    finally:
        await connector.close()


if __name__ == "__main__":
    asyncio.run(test())
