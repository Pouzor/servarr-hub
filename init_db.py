from app.db import engine, Base, check_db_connection
from app.models import *

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
