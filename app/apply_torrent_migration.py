"""
Script pour appliquer la migration torrent_info
"""

import sys

from sqlalchemy import text

from app.db import engine


def apply_migration():
    """Applique la migration pour ajouter torrent_info"""

    print("🚀 Application de la migration torrent_info...")

    try:
        with engine.connect() as connection:
            # Vérifier si la colonne existe déjà
            result = connection.execute(
                text("""
                SELECT COUNT(*) as count
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_SCHEMA = DATABASE()
                AND TABLE_NAME = 'library_items'
                AND COLUMN_NAME = 'torrent_info'
            """)
            )

            exists = result.fetchone()[0] > 0

            if exists:
                print("⚠️  La colonne torrent_info existe déjà, migration annulée.")
                return

            # Ajouter la colonne
            print("📝 Ajout de la colonne torrent_info...")
            connection.execute(
                text("""
                ALTER TABLE library_items
                ADD COLUMN torrent_info JSON DEFAULT NULL
            """)
            )
            connection.commit()

            print("✅ Migration appliquée avec succès !")

            # Vérification
            result = connection.execute(
                text("""
                SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_SCHEMA = DATABASE()
                AND TABLE_NAME = 'library_items'
                AND COLUMN_NAME = 'torrent_info'
            """)
            )

            row = result.fetchone()
            print(f"✅ Colonne créée : {row[0]} | Type: {row[1]} | Nullable: {row[2]}")

    except Exception as e:
        print(f"❌ Erreur lors de la migration : {e}")
        sys.exit(1)


if __name__ == "__main__":
    apply_migration()
