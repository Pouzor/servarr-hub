"""
Script pour vérifier que les tables analytics sont bien créées
"""

from sqlalchemy import inspect

from app.db import check_db_connection, engine


def verify_analytics_tables():
    """Vérifie l'existence et la structure des tables analytics"""

    print("🔍 Vérification des tables analytics...\n")

    if not check_db_connection():
        print("❌ Impossible de se connecter à la base de données!")
        return False

    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()

    # Tables analytics attendues
    expected_tables = {
        "playback_sessions": [
            "id",
            "media_id",
            "media_title",
            "media_type",
            "user_id",
            "user_name",
            "device_type",
            "video_quality",
            "playback_method",
            "start_time",
            "end_time",
            "duration_seconds",
            "watched_seconds",
            "status",
            "is_active",
            "created_at",
            "updated_at",
        ],
        "media_statistics": [
            "id",
            "media_id",
            "media_title",
            "media_type",
            "total_plays",
            "total_duration_seconds",
            "total_watched_seconds",
            "unique_users",
            "last_played_at",
            "created_at",
            "updated_at",
        ],
        "device_statistics": [
            "id",
            "device_type",
            "period_start",
            "period_end",
            "session_count",
            "total_duration_seconds",
            "unique_users",
            "created_at",
            "updated_at",
        ],
        "daily_analytics": [
            "id",
            "date",
            "total_plays",
            "hours_watched",
            "unique_users",
            "unique_media",
            "movies_played",
            "tv_episodes_played",
            "created_at",
            "updated_at",
        ],
        "server_metrics": [
            "id",
            "cpu_usage_percent",
            "memory_usage_gb",
            "bandwidth_mbps",
            "storage_used_tb",
            "active_sessions_count",
            "recorded_at",
            "created_at",
        ],
    }

    all_good = True

    for table_name, expected_columns in expected_tables.items():
        if table_name not in existing_tables:
            print(f"❌ Table manquante: {table_name}")
            all_good = False
            continue

        # Vérifier les colonnes
        columns = inspector.get_columns(table_name)
        column_names = [col["name"] for col in columns]

        missing_columns = set(expected_columns) - set(column_names)

        if missing_columns:
            print(f"⚠️  Table {table_name} : colonnes manquantes {missing_columns}")
            all_good = False
        else:
            print(f"✅ Table {table_name} : OK ({len(column_names)} colonnes)")

    print("\n" + "=" * 60)
    if all_good:
        print("✅ Toutes les tables analytics sont correctement configurées!")
    else:
        print("❌ Certaines tables ou colonnes sont manquantes")
    print("=" * 60)

    return all_good


if __name__ == "__main__":
    verify_analytics_tables()
