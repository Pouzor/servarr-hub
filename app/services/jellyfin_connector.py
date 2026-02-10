from datetime import datetime, timedelta
from typing import Any

from app.services.base_connector import BaseConnector


class JellyfinConnector(BaseConnector):
    """Connecteur pour l'API Jellyfin"""

    def _get_headers(self) -> dict[str, str]:
        """Headers spécifiques à Jellyfin"""
        return {**super()._get_headers(), "X-Emby-Token": self.api_key}

    async def test_connection(self) -> tuple[bool, str]:
        """Tester la connexion à Jellyfin"""
        try:
            response = await self._get("/System/Info/Public")
            version = response.get("Version", "unknown")
            return True, f"Connecté à Jellyfin v{version}"
        except Exception as e:
            return False, f"Erreur de connexion: {str(e)}"

    async def get_users(self) -> list[dict[str, Any]]:
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

    async def get_library_items(self) -> dict[str, Any]:
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
                "songs": response.get("SongCount", 0),
            }
        except Exception as e:
            print(f"❌ Erreur récupération items Jellyfin: {e}")
            return {}

    async def get_recent_items(self, limit: int = 20) -> list[dict[str, Any]]:
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
                "IncludeItemTypes": "Movie,Series",
            }

            response = await self._get("/Items", params=params)
            return response.get("Items", [])
        except Exception as e:
            print(f"❌ Erreur récupération items récents Jellyfin: {e}")
            return []

    async def get_playback_stats(self, days: int = 30) -> dict[str, Any]:
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
                "period_days": days,
            }
        except Exception as e:
            print(f"❌ Erreur récupération stats playback: {e}")
            return {}

    async def get_total_watch_time(self, days: int = 30) -> dict[str, Any]:
        """
        Récupérer le temps de visionnage total via le plugin Playback Reporting

        Args:
            days: Nombre de jours à analyser (défaut: 30)

        Returns:
            Dictionnaire avec:
            - total_hours: Temps total en heures (float)
            - total_seconds: Temps total en secondes (int)
            - period_days: Période analysée
        """
        try:
            # Requête SQL personnalisée pour le temps total sur la période
            # Le plugin Playback Reporting expose l'endpoint /user_usage_stats/submit_custom_query
            url = "/user_usage_stats/submit_custom_query"

            # Calculer la date de début (il y a X jours)
            start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

            query = (
                f"SELECT SUM(PlayDuration) as TotalSeconds "  # noqa: S608
                f"FROM PlaybackActivity "
                f"WHERE DateCreated >= '{start_date}'"
            )

            body = {"CustomQueryString": query, "ReplaceUserId": False}

            response = await self._post(url, json=body)

            # Format de réponse: {"columns": ["TotalSeconds"], "results": [[123456]]}
            if response and response.get("results") and len(response["results"]) > 0:
                total_seconds = response["results"][0][0]
                if total_seconds is None:
                    total_seconds = 0
                else:
                    total_seconds = int(total_seconds)

                total_hours = round(total_seconds / 3600, 1)

                return {"total_hours": total_hours, "total_seconds": total_seconds, "period_days": days}
            else:
                print("⚠️  Aucune donnée de visionnage trouvée (plugin Playback Reporting installé ?)")
                return {"total_hours": 0, "total_seconds": 0, "period_days": days}

        except Exception as e:
            print(f"❌ Erreur récupération watch time (Playback Reporting): {e}")
            # Retourner des valeurs par défaut si le plugin n'est pas disponible
            return {"total_hours": 0, "total_seconds": 0, "period_days": days}

    async def get_movies_details(self) -> dict[str, Any]:
        """
        Récupérer les détails complets des films (nombre de films, durée totale)

        Returns:
            Dictionnaire avec:
            - total_movies: Nombre total de films
            - total_hours: Durée totale en heures de tous les films
        """
        try:
            # Récupérer tous les films avec leur durée (RunTimeTicks)
            params = {
                "Recursive": True,
                "IncludeItemTypes": "Movie",
                "Fields": "RunTimeTicks",
                "EnableTotalRecordCount": True,
            }

            response = await self._get("/Items", params=params)

            movies = response.get("Items", [])
            total_movies = response.get("TotalRecordCount", len(movies))

            # Calculer la durée totale
            # RunTimeTicks est en ticks (1 tick = 100 nanosecondes)
            # 1 seconde = 10,000,000 ticks
            total_ticks = sum(movie.get("RunTimeTicks", 0) for movie in movies)
            total_seconds = total_ticks / 10_000_000
            total_hours = round(total_seconds / 3600)

            return {"total_movies": total_movies, "total_hours": total_hours}

        except Exception as e:
            print(f"❌ Erreur récupération détails films: {e}")
            return {"total_movies": 0, "total_hours": 0}

    async def get_tv_shows_details(self) -> dict[str, Any]:
        """
        Récupérer les détails complets des séries TV (nombre de séries, épisodes, durée totale)

        Returns:
            Dictionnaire avec:
            - total_series: Nombre total de séries
            - total_episodes: Nombre total d'épisodes
            - total_hours: Durée totale en heures de tous les épisodes
        """
        try:
            # Récupérer tous les épisodes avec leur durée (RunTimeTicks)
            params = {
                "Recursive": True,
                "IncludeItemTypes": "Episode",
                "Fields": "RunTimeTicks",
                "EnableTotalRecordCount": True,
            }

            response = await self._get("/Items", params=params)

            episodes = response.get("Items", [])
            total_episodes = response.get("TotalRecordCount", len(episodes))

            # Calculer la durée totale
            # RunTimeTicks est en ticks (1 tick = 100 nanosecondes)
            # 1 seconde = 10,000,000 ticks
            total_ticks = sum(ep.get("RunTimeTicks", 0) for ep in episodes)
            total_seconds = total_ticks / 10_000_000
            total_hours = round(total_seconds / 3600)

            # Récupérer le nombre de séries
            series_params = {"Recursive": True, "IncludeItemTypes": "Series", "EnableTotalRecordCount": True}

            series_response = await self._get("/Items", params=series_params)
            total_series = series_response.get("TotalRecordCount", 0)

            return {"total_series": total_series, "total_episodes": total_episodes, "total_hours": total_hours}

        except Exception as e:
            print(f"❌ Erreur récupération détails TV shows: {e}")
            return {"total_series": 0, "total_episodes": 0, "total_hours": 0}
