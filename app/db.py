from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Créer le moteur SQLAlchemy
engine = create_engine(
    settings.DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    pool_recycle=3600,
    connect_args={"charset": "utf8mb4"}  # ⬅️ Force le rechargement des métadonnées
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base pour les modèles
Base = declarative_base()


def get_db():
    """
    Dependency pour obtenir une session DB
    À utiliser dans les endpoints FastAPI
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Créer toutes les tables"""
    Base.metadata.create_all(bind=engine)


def check_db_connection():
    """Vérifier la connexion à la base de données"""
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return True
    except Exception as e:
        print(f"Erreur de connexion DB: {e}")
        return False
