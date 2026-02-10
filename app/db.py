"""
Configuration de la base de données
"""

import logging

from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Désactiver les logs SQLAlchemy
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
logging.getLogger("sqlalchemy.pool").setLevel(logging.WARNING)

# Créer l'engine SQLAlchemy
engine = create_engine(
    settings.DATABASE_URL, echo=False, pool_pre_ping=True, pool_size=10, max_overflow=20, pool_recycle=3600
)


# ⬇️ NOUVEAU : Event listener pour forcer le rechargement des enums
@event.listens_for(engine, "connect")
def receive_connect(dbapi_conn, connection_record):
    """Force le rechargement des métadonnées à chaque connexion"""
    # Invalider le cache des types
    connection_record.info.pop("sqlalchemy_cache", None)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dépendance pour obtenir une session DB"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_db_connection():
    """Vérifier la connexion à la base de données"""
    try:
        with engine.connect():
            return True
    except Exception as e:
        print(f"Erreur de connexion à la base de données : {e}")
        return False


def init_db():
    """Initialiser la base de données (créer les tables)"""
    Base.metadata.create_all(bind=engine)
