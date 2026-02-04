from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db import check_db_connection, init_db

# Créer l'application FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG
)

# Configuration CORS (pour accès depuis un frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # À restreindre en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Événements au démarrage de l'app"""
    print(f"🚀 Démarrage de {settings.APP_NAME} v{settings.APP_VERSION}")
    
    # Vérifier la connexion DB
    if check_db_connection():
        print("✅ Connexion à la base de données OK")
        # Créer les tables si elles n'existent pas
        init_db()
        print("✅ Tables initialisées")
    else:
        print("❌ Échec de connexion à la base de données")


@app.get("/")
async def root():
    """Endpoint racine"""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    db_status = check_db_connection()
    return {
        "status": "healthy" if db_status else "unhealthy",
        "database": "connected" if db_status else "disconnected"
    }
