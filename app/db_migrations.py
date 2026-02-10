"""
Script de migration pour ajouter les tables analytics
"""

from sqlalchemy import inspect

from app.db import Base, check_db_connection, engine


def get_existing_tables():
    """Récupère la liste des tables existantes dans la DB"""
    inspector = inspect(engine)
    return inspector.get_table_names()


def create_analytics_tables():
    """Crée uniquement les nouvelles tables analytics"""
    print("🔍 Vérification de la connexion à la base de données...")
    if not check_db_connection():
        print("❌ Impossible de se connecter à la base de données!")
        return False

    print("✅ Connexion établie")

    existing_tables = get_existing_tables()
    print(f"\n📊 Tables existantes : {len(existing_tables)}")
    for table in existing_tables:
        print(f"  - {table}")

    new_tables = ["playback_sessions", "media_statistics", "device_statistics", "daily_analytics", "server_metrics"]

    tables_to_create = [t for t in new_tables if t not in existing_tables]

    if not tables_to_create:
        print("\n✅ Toutes les tables analytics existent déjà!")
        return True

    print(f"\n🆕 Nouvelles tables à créer : {len(tables_to_create)}")
    for table in tables_to_create:
        print(f"  - {table}")

    try:
        print("\n🚀 Création des nouvelles tables...")
        # Crée uniquement les tables qui n'existent pas
        Base.metadata.create_all(bind=engine, checkfirst=True)
        print("✅ Tables créées avec succès!")

        # Vérification
        new_existing_tables = get_existing_tables()
        created = set(new_existing_tables) - set(existing_tables)
        if created:
            print("\n✨ Tables créées :")
            for table in created:
                print(f"  - {table}")

        return True

    except Exception as e:
        print(f"❌ Erreur lors de la création des tables : {e}")
        return False


def show_table_info():
    """Affiche les informations détaillées sur toutes les tables"""
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    print("\n" + "=" * 60)
    print("📋 INFORMATIONS DÉTAILLÉES DES TABLES")
    print("=" * 60)

    for table_name in sorted(tables):
        columns = inspector.get_columns(table_name)
        indexes = inspector.get_indexes(table_name)

        print(f"\n📌 Table: {table_name}")
        print(f"   Colonnes: {len(columns)}")
        for col in columns:
            col_type = str(col["type"])
            nullable = "NULL" if col["nullable"] else "NOT NULL"
            print(f"      - {col['name']}: {col_type} {nullable}")

        if indexes:
            print(f"   Index: {len(indexes)}")
            for idx in indexes:
                unique = "UNIQUE" if idx["unique"] else ""
                print(f"      - {idx['name']} {unique}")


if __name__ == "__main__":
    print("=" * 60)
    print("🔧 MIGRATION BASE DE DONNÉES - ANALYTICS")
    print("=" * 60)

    # Créer les tables
    success = create_analytics_tables()

    if success:
        # Afficher les infos
        show_table_info()
        print("\n" + "=" * 60)
        print("✅ Migration terminée avec succès!")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("❌ Migration échouée")
        print("=" * 60)
