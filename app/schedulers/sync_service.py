from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from typing import Dict, Any
import time

from app.models import (
    ServiceConfiguration, ServiceType, SyncMetadata, SyncStatus,
    LibraryItem, CalendarEvent, JellyseerrRequest, DashboardStatistic,
    MediaType, CalendarStatus, RequestPriority, StatType
)
from app.services import (
    RadarrConnector, SonarrConnector, 
    JellyfinConnector, JellyseerrConnector
)


class SyncService:
    """Service de synchronisation des données depuis les APIs externes"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_active_service(self, service_type: ServiceType) -> ServiceConfiguration:
        """Récupérer la configuration d'un service actif"""
        return self.db.query(ServiceConfiguration).filter(
            ServiceConfiguration.service_name == service_type,
            ServiceConfiguration.is_active == True
        ).first()
    
    def update_sync_metadata(
        self, 
        service_type: ServiceType, 
        status: SyncStatus,
        records: int = 0,
        duration_ms: int = 0,
        error: str = None
    ):
        """Mettre à jour les métadonnées de sync"""
        sync_meta = self.db.query(SyncMetadata).filter(
            SyncMetadata.service_name == service_type
        ).first()
        
        if not sync_meta:
            sync_meta = SyncMetadata(service_name=service_type)
            self.db.add(sync_meta)
        
        sync_meta.last_sync_time = datetime.now(timezone.utc)
        sync_meta.sync_status = status
        sync_meta.records_synced = records
        sync_meta.sync_duration_ms = duration_ms
        sync_meta.error_message = error
        sync_meta.next_sync_time = datetime.now(timezone.utc) + timedelta(minutes=15)
        
        self.db.commit()


    async def sync_monitored_items(self) -> Dict[str, Any]:
        """
        Synchroniser les statistiques des items monitorés (Radarr + Sonarr)
        """
        print("📊 Synchronisation des items monitorés...")
        start_time = time.time()
    
        try:
            # Initialiser les totaux
            total_monitored = 0
            total_unmonitored = 0
            downloading = 0
            downloaded = 0
            missing = 0
            queued = 0
            unreleased = 0
        
            # === RADARR ===
            radarr_service = self.get_active_service(ServiceType.RADARR)
            if radarr_service:
                radarr_connector = RadarrConnector(
                    base_url=radarr_service.url, 
                    api_key=radarr_service.api_key, 
                    port=radarr_service.port
                )
                try:
                    radarr_stats = await radarr_connector.get_statistics()
                
                    # Ajouter les stats Radarr
                    total_monitored += radarr_stats.get("monitored_movies", 0)
                    total_unmonitored += radarr_stats.get("total_movies", 0) - radarr_stats.get("monitored_movies", 0)
                    downloaded += radarr_stats.get("downloaded_movies", 0)
                    missing += radarr_stats.get("missing_movies", 0)
                
                    print(f"  📽️  Radarr: {radarr_stats.get('monitored_movies', 0)} monitorés")
                except Exception as e:
                    print(f"  ⚠️  Erreur stats Radarr: {e}")
                finally:
                    await radarr_connector.close()
        
            # === SONARR ===
            sonarr_service = self.get_active_service(ServiceType.SONARR)
            if sonarr_service:
                sonarr_connector = SonarrConnector(
                    base_url=sonarr_service.url,
                    api_key=sonarr_service.api_key,
                    port=sonarr_service.port
                )
                try:
                    sonarr_stats = await sonarr_connector.get_statistics()
                
                    # Ajouter les stats Sonarr
                    total_monitored += sonarr_stats.get("monitored_series", 0)
                    total_unmonitored += sonarr_stats.get("total_series", 0) - sonarr_stats.get("monitored_series", 0)
                    downloaded += sonarr_stats.get("downloaded_episodes", 0)
                    missing += sonarr_stats.get("missing_episodes", 0)
                
                    print(f"  📺 Sonarr: {sonarr_stats.get('monitored_series', 0)} monitorés")
                except Exception as e:
                    print(f"  ⚠️  Erreur stats Sonarr: {e}")
                finally:
                    await sonarr_connector.close()
        
            # Mettre à jour ou créer la statistique MONITORED_ITEMS
            monitored_stat = self.db.query(DashboardStatistic).filter(
                DashboardStatistic.stat_type == StatType.MONITORED_ITEMS
            ).first()
        
            if not monitored_stat:
                monitored_stat = DashboardStatistic(stat_type=StatType.MONITORED_ITEMS)
                self.db.add(monitored_stat)
        
        # Total = items monitorés
            monitored_stat.total_count = total_monitored
            monitored_stat.details = {
                "monitored": total_monitored,
                "unmonitored": total_unmonitored,
                "downloading": downloading,
                "downloaded": downloaded,
                "missing": missing,
                "queued": queued,
                "unreleased": unreleased
            }
            monitored_stat.last_synced = datetime.now(timezone.utc)
        
            self.db.commit()
        
            duration_ms = int((time.time() - start_time) * 1000)
        
            print(f"✅ Monitored Items: {total_monitored} monitorés, {missing} manquants")
            return {
                "success": True,
                "monitored": total_monitored,
                "unmonitored": total_unmonitored,
                "details": monitored_stat.details
            }
        
        except Exception as e:
            print(f"❌ Erreur sync monitored items: {e}")
            return {"success": False, "error": str(e)}

    
    async def sync_radarr(self) -> Dict[str, Any]:
        """Synchroniser les données Radarr"""
        print("🎬 Synchronisation Radarr...")
        start_time = time.time()
        
        service = self.get_active_service(ServiceType.RADARR)
        if not service:
            print("⚠️  Service Radarr non configuré")
            return {"success": False, "message": "Service non configuré"}
        
        connector = RadarrConnector(base_url=service.url, api_key=service.api_key, port=service.port)
        
        try:
            # Récupérer les films récents
            recent_movies = await connector.get_recent_additions(days=30)
            
            # Ajouter à la DB (éviter les doublons)
            added_count = 0
            for movie in recent_movies[:20]:  # Limiter à 20 pour ne pas surcharger
                # Vérifier si existe déjà (par titre + année)
                existing = self.db.query(LibraryItem).filter(
                    LibraryItem.title == movie.get("title"),
                    LibraryItem.year == movie.get("year"),
                    LibraryItem.media_type == MediaType.MOVIE
                ).first()
                
                if not existing:
                    # Calculer la taille
                    size_bytes = movie.get("sizeOnDisk", 0)
                    size_gb = round(size_bytes / (1024**3), 1)
                    
                    # Date d'ajout
                    added_date = movie.get("added", "")
                    if added_date:
                        added_dt = datetime.fromisoformat(added_date.replace("Z", "+00:00"))
                        time_ago = self._format_time_ago(added_dt)
                    else:
                        time_ago = "Unknown"
                    
                    # Récupérer l'image
                    image_url = ""
                    for img in movie.get("images", []):
                        if img.get("coverType") == "poster":
                            image_url = img.get("remoteUrl", "")
                            break
                    if not image_url and movie.get("images"):
                        image_url = movie.get("images", [{}])[0].get("remoteUrl", "")
                    
                    item = LibraryItem(
                        title=movie.get("title", "Unknown"),
                        year=movie.get("year", 0),
                        media_type=MediaType.MOVIE,
                        image_url=image_url,
                        image_alt=f"{movie.get('title')} poster",
                        quality=movie.get("qualityProfileId", "Unknown"),
                        rating=str(movie.get("ratings", {}).get("imdb", {}).get("value", "")),
                        description=movie.get("overview", ""),
                        added_date=time_ago,
                        size=f"{size_gb} GB"
                    )
                    self.db.add(item)
                    added_count += 1
            
            # Récupérer le calendrier
            calendar = await connector.get_calendar(days_ahead=30)
            
            # Ajouter au calendrier
            calendar_count = 0
            for event in calendar[:20]:
                release_date_str = event.get("physicalRelease") or event.get("digitalRelease")
                if not release_date_str:
                    continue
                
                try:
                    release_date = datetime.fromisoformat(
                        release_date_str.replace("Z", "+00:00")
                    ).date()
                except:
                    continue
                
                existing = self.db.query(CalendarEvent).filter(
                    CalendarEvent.title == event.get("title"),
                    CalendarEvent.release_date == release_date
                ).first()
                
                if not existing:
                    # Récupérer l'image
                    image_url = ""
                    for img in event.get("images", []):
                        if img.get("coverType") == "poster":
                            image_url = img.get("remoteUrl", "")
                            break
                    if not image_url and event.get("images"):
                        image_url = event.get("images", [{}])[0].get("remoteUrl", "")
                    
                    cal_event = CalendarEvent(
                        title=event.get("title", "Unknown"),
                        media_type=MediaType.MOVIE,
                        release_date=release_date,
                        image_url=image_url,
                        image_alt=f"{event.get('title')} poster",
                        status=CalendarStatus.MONITORED
                    )
                    self.db.add(cal_event)
                    calendar_count += 1
            
            self.db.commit()
            
            duration_ms = int((time.time() - start_time) * 1000)
            self.update_sync_metadata(
                ServiceType.RADARR, 
                SyncStatus.SUCCESS,
                added_count + calendar_count,
                duration_ms
            )
            
            print(f"✅ Radarr: {added_count} films, {calendar_count} événements")
            return {
                "success": True,
                "movies_added": added_count,
                "calendar_events": calendar_count
            }
            
        except Exception as e:
            duration_ms = int((time.time() - start_time) * 1000)
            self.update_sync_metadata(
                ServiceType.RADARR,
                SyncStatus.FAILED,
                0,
                duration_ms,
                str(e)
            )
            print(f"❌ Erreur sync Radarr: {e}")
            return {"success": False, "error": str(e)}
        finally:
            await connector.close()
    
    async def sync_sonarr(self) -> Dict[str, Any]:
        """Synchroniser les données Sonarr"""
        print("📺 Synchronisation Sonarr...")
        start_time = time.time()
        
        service = self.get_active_service(ServiceType.SONARR)
        if not service:
            print("⚠️  Service Sonarr non configuré")
            return {"success": False, "message": "Service non configuré"}
        
        connector = SonarrConnector(base_url=service.url, api_key=service.api_key, port=service.port)
        
        try:
            # Récupérer les séries récentes
            recent_series = await connector.get_recent_additions(days=30)
            
            added_count = 0
            for series in recent_series[:20]:
                existing = self.db.query(LibraryItem).filter(
                    LibraryItem.title == series.get("title"),
                    LibraryItem.year == series.get("year"),
                    LibraryItem.media_type == MediaType.TV
                ).first()
                
                if not existing:
                    size_bytes = series.get("statistics", {}).get("sizeOnDisk", 0)
                    size_gb = round(size_bytes / (1024**3), 1)
                    
                    added_date = series.get("added", "")
                    if added_date:
                        added_dt = datetime.fromisoformat(added_date.replace("Z", "+00:00"))
                        time_ago = self._format_time_ago(added_dt)
                    else:
                        time_ago = "Unknown"
                    
                    # Récupérer l'image
                    image_url = ""
                    for img in series.get("images", []):
                        if img.get("coverType") == "poster":
                            image_url = img.get("remoteUrl", "")
                            break
                    if not image_url and series.get("images"):
                        image_url = series.get("images", [{}])[0].get("remoteUrl", "")
                    
                    item = LibraryItem(
                        title=series.get("title", "Unknown"),
                        year=series.get("year", 0),
                        media_type=MediaType.TV,
                        image_url=image_url,
                        image_alt=f"{series.get('title')} poster",
                        quality=str(series.get("qualityProfileId", "Unknown")),
                        rating=str(series.get("ratings", {}).get("value", "")),
                        description=series.get("overview", ""),
                        added_date=time_ago,
                        size=f"{size_gb} GB"
                    )
                    self.db.add(item)
                    added_count += 1
            
            # Récupérer le calendrier
            calendar = await connector.get_calendar(days_ahead=30)
            
            calendar_count = 0
            for event in calendar[:20]:
                if not event.get("airDate"):
                    continue
                
                try:
                    air_date = datetime.fromisoformat(
                        event.get("airDate") + "T00:00:00+00:00"
                    ).date()
                except:
                    continue
                
                # Titre avec info épisode
                series_title = event.get("series", {}).get("title", "Unknown")
                season = event.get("seasonNumber", 0)
                episode_num = event.get("episodeNumber", 0)
                
                existing = self.db.query(CalendarEvent).filter(
                    CalendarEvent.title == series_title,
                    CalendarEvent.release_date == air_date,
                    CalendarEvent.episode == f"Season {season}, Episode {episode_num}"
                ).first()
                
                if not existing:
                    # Récupérer l'image
                    image_url = ""
                    series_data = event.get("series", {})
                    for img in series_data.get("images", []):
                        if img.get("coverType") == "poster":
                            image_url = img.get("remoteUrl", "")
                            break
                    if not image_url and series_data.get("images"):
                        image_url = series_data.get("images", [{}])[0].get("remoteUrl", "")
                    
                    cal_event = CalendarEvent(
                        title=series_title,
                        media_type=MediaType.TV,
                        release_date=air_date,
                        episode=f"Season {season}, Episode {episode_num}",
                        image_url=image_url,
                        image_alt=f"{series_title} poster",
                        status=CalendarStatus.MONITORED
                    )
                    self.db.add(cal_event)
                    calendar_count += 1
            
            self.db.commit()
            
            duration_ms = int((time.time() - start_time) * 1000)
            self.update_sync_metadata(
                ServiceType.SONARR,
                SyncStatus.SUCCESS,
                added_count + calendar_count,
                duration_ms
            )
            
            print(f"✅ Sonarr: {added_count} séries, {calendar_count} événements")
            return {
                "success": True,
                "series_added": added_count,
                "calendar_events": calendar_count
            }
            
        except Exception as e:
            duration_ms = int((time.time() - start_time) * 1000)
            self.update_sync_metadata(
                ServiceType.SONARR,
                SyncStatus.FAILED,
                0,
                duration_ms,
                str(e)
            )
            print(f"❌ Erreur sync Sonarr: {e}")
            return {"success": False, "error": str(e)}
        finally:
            await connector.close()
    
    async def sync_jellyfin(self) -> Dict[str, Any]:
        """Synchroniser les données Jellyfin"""
        print("🎥 Synchronisation Jellyfin...")
        start_time = time.time()
        
        service = self.get_active_service(ServiceType.JELLYFIN)
        if not service:
            print("⚠️  Service Jellyfin non configuré")
            return {"success": False, "message": "Service non configuré"}
        
        connector = JellyfinConnector(base_url=service.url, api_key=service.api_key, port=service.port)
        
        try:
            # Récupérer les stats
            users = await connector.get_users()
            library_stats = await connector.get_library_items()
            
            # Mettre à jour les statistiques
            # Users
            user_stat = self.db.query(DashboardStatistic).filter(
                DashboardStatistic.stat_type == StatType.USERS
            ).first()
            
            if not user_stat:
                user_stat = DashboardStatistic(stat_type=StatType.USERS)
                self.db.add(user_stat)
            
            user_stat.total_count = len(users)
            user_stat.details = {
                "active_users": len([u for u in users if not u.get("Policy", {}).get("IsDisabled", False)])
            }
            user_stat.last_synced = datetime.now(timezone.utc)
            
            # Movies
            movie_stat = self.db.query(DashboardStatistic).filter(
                DashboardStatistic.stat_type == StatType.MOVIES
            ).first()
            
            if not movie_stat:
                movie_stat = DashboardStatistic(stat_type=StatType.MOVIES)
                self.db.add(movie_stat)
            
            movie_stat.total_count = library_stats.get("movies", 0)
            movie_stat.last_synced = datetime.now(timezone.utc)
            
            # TV Shows
            tv_stat = self.db.query(DashboardStatistic).filter(
                DashboardStatistic.stat_type == StatType.TV_SHOWS
            ).first()
            
            if not tv_stat:
                tv_stat = DashboardStatistic(stat_type=StatType.TV_SHOWS)
                self.db.add(tv_stat)
            
            tv_stat.total_count = library_stats.get("series", 0)
            tv_stat.details = {
                "total_episodes": library_stats.get("episodes", 0)
            }
            tv_stat.last_synced = datetime.now(timezone.utc)
            
            self.db.commit()
            
            duration_ms = int((time.time() - start_time) * 1000)
            self.update_sync_metadata(
                ServiceType.JELLYFIN,
                SyncStatus.SUCCESS,
                len(users),
                duration_ms
            )
            
            print(f"✅ Jellyfin: {len(users)} users, {library_stats.get('movies', 0)} films")
            return {
                "success": True,
                "users": len(users),
                "library_stats": library_stats
            }
            
        except Exception as e:
            duration_ms = int((time.time() - start_time) * 1000)
            self.update_sync_metadata(
                ServiceType.JELLYFIN,
                SyncStatus.FAILED,
                0,
                duration_ms,
                str(e)
            )
            print(f"❌ Erreur sync Jellyfin: {e}")
            return {"success": False, "error": str(e)}
        finally:
            await connector.close()
    
    async def sync_jellyseerr(self) -> Dict[str, Any]:
        """Synchroniser les données Jellyseerr"""
        print("📝 Synchronisation Jellyseerr...")
        start_time = time.time()
        
        service = self.get_active_service(ServiceType.JELLYSEERR)
        if not service:
            print("⚠️  Service Jellyseerr non configuré")
            return {"success": False, "message": "Service non configuré"}
        
        connector = JellyseerrConnector(base_url=service.url, api_key=service.api_key, port=service.port)
        
        try:
            # Tester d'abord la connexion
            success, message = await connector.test_connection()
            if not success:
                raise Exception(f"Test de connexion échoué: {message}")
            
            # Récupérer les requêtes pendantes
            requests = await connector.get_requests(limit=50, status="pending")
            
            if not requests:
                print("ℹ️  Aucune requête Jellyseerr en attente")
                duration_ms = int((time.time() - start_time) * 1000)
                self.update_sync_metadata(
                    ServiceType.JELLYSEERR,
                    SyncStatus.SUCCESS,
                    0,
                    duration_ms
                )
                return {"success": True, "requests_added": 0}
            
            # Nettoyer les anciennes requêtes
            self.db.query(JellyseerrRequest).delete()
            
            # Ajouter les nouvelles
            added_count = 0
            for req in requests[:20]:
                try:
                    media = req.get("media", {})
                    requested_by = req.get("requestedBy", {})
                    
                    # Extraction sécurisée de l'année
                    year = 0
                    if media.get("releaseDate"):
                        try:
                            year = int(media.get("releaseDate", "")[:4])
                        except:
                            year = 0
                    
                    # Extraction sécurisée de la date de création
                    requested_date = "Unknown"
                    if req.get("createdAt"):
                        try:
                            created_dt = datetime.fromisoformat(req.get("createdAt").replace("Z", "+00:00"))
                            requested_date = self._format_time_ago(created_dt)
                        except:
                            pass
                    
                    request_item = JellyseerrRequest(
                        title=media.get("title", "Unknown"),
                        media_type=MediaType.MOVIE if req.get("type") == "movie" else MediaType.TV,
                        year=year,
                        image_url=f"https://image.tmdb.org/t/p/w500{media.get('posterPath', '')}" if media.get('posterPath') else "",
                        image_alt=f"{media.get('title', 'Unknown')} poster",
                        priority=RequestPriority.MEDIUM,
                        requested_by=requested_by.get("displayName", "Unknown"),
                        requested_date=requested_date,
                        quality="4K" if req.get("is4k") else "1080p",
                        description=media.get("overview", "")
                    )
                    self.db.add(request_item)
                    added_count += 1
                except Exception as item_error:
                    print(f"⚠️  Erreur traitement requête Jellyseerr: {item_error}")
                    continue
            
            self.db.commit()
            
            duration_ms = int((time.time() - start_time) * 1000)
            self.update_sync_metadata(
                ServiceType.JELLYSEERR,
                SyncStatus.SUCCESS,
                added_count,
                duration_ms
            )
            
            print(f"✅ Jellyseerr: {added_count} requêtes")
            return {
                "success": True,
                "requests_added": added_count
            }
            
        except Exception as e:
            duration_ms = int((time.time() - start_time) * 1000)
            self.update_sync_metadata(
                ServiceType.JELLYSEERR,
                SyncStatus.FAILED,
                0,
                duration_ms,
                str(e)
            )
            print(f"❌ Erreur sync Jellyseerr: {e}")
            return {"success": False, "error": str(e)}
        finally:
            await connector.close()
    
    async def sync_all(self) -> Dict[str, Any]:
        """Synchroniser tous les services"""
        print("\n" + "="*50)
        print("🔄 DÉBUT DE LA SYNCHRONISATION GLOBALE")
        print("="*50 + "\n")
        
        results = {}
        
        results["radarr"] = await self.sync_radarr()
        results["sonarr"] = await self.sync_sonarr()
        results["jellyfin"] = await self.sync_jellyfin()
        results["jellyseerr"] = await self.sync_jellyseerr()
        
        print("\n" + "="*50)
        print("✅ SYNCHRONISATION TERMINÉE")
        print("="*50 + "\n")
        
        return results
    
    def _format_time_ago(self, dt: datetime) -> str:
        """Formater une date en 'X hours ago', 'X days ago'"""
        # S'assurer que dt est timezone-aware
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        
        now = datetime.now(timezone.utc)
        delta = now - dt
        
        if delta.days > 0:
            return f"{delta.days} day{'s' if delta.days > 1 else ''} ago"
        elif delta.seconds >= 3600:
            hours = delta.seconds // 3600
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif delta.seconds >= 60:
            minutes = delta.seconds // 60
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        else:
            return "just now"
