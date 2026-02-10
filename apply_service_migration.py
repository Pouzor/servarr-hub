"""
Script pour appliquer la migration username/password
"""

import sys

from sqlalchemy import text

from app.db import engine


def apply_migration():
    """Applique la migration pour username/password"""

    print("🚀 Application de la migration username/password...")

    try:
        with engine.connect() as connection:
            # Vérifier si les colonnes existent déjà
            result = connection.execute(
                text("""
                SELECT COUNT(*) as count
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_SCHEMA = DATABASE()
                AND TABLE_NAME = 'service_configurations'
                AND COLUMN_NAME IN ('username', 'password')
            """)
            )

            exists_count = result.fetchone()[0]

            if exists_count == 2:
                print("⚠️  Les colonnes username/password existent déjà, migration annulée.")
                return

            # Modifier api_key pour nullable
            print("📝 Modification de api_key en nullable...")
            connection.execute(
                text("""
                ALTER TABLE service_configurations
                MODIFY COLUMN api_key TEXT NULL
            """)
            )

            # Ajouter username si n'existe pas
            if exists_count < 2:
                print("📝 Ajout de la colonne username...")
                connection.execute(
                    text("""
                    ALTER TABLE service_configurations
                    ADD COLUMN username TEXT NULL
                """)
                )

                print("📝 Ajout de la colonne password...")
                connection.execute(
                    text("""
                    ALTER TABLE service_configurations
                    ADD COLUMN password TEXT NULL
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
                AND TABLE_NAME = 'service_configurations'
                AND COLUMN_NAME IN ('api_key', 'username', 'password')
                ORDER BY COLUMN_NAME
            """)
            )

            print("\n✅ Colonnes créées :")
            for row in result:
                print(f"  - {row[0]} | Type: {row[1]} | Nullable: {row[2]}")

    except Exception as e:
        print(f"❌ Erreur lors de la migration : {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    apply_migration()
