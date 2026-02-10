from app.db import Base, check_db_connection, engine
from app.models import models  # noqa: F401 - import needed to register models with Base


def init_database():
    """Créer toutes les tables"""
    if not check_db_connection():
        print("❌ Impossible de se connecter à la base de données")
        return

    print("📦 Création des tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables créées avec succès!")


if __name__ == "__main__":
    init_database()
