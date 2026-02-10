"""
Script pour vider le cache d'enum de SQLAlchemy
"""

import sys

from sqlalchemy import inspect

from app.db import engine
from app.models.models import ServiceConfiguration


def clear_enum_cache():
    """Vide complètement le cache d'enum de SQLAlchemy"""

    print("🧹 Nettoyage du cache SQLAlchemy...")

    try:
        # 1. Vider le cache de l'engine
        engine.dispose()
        print("✅ Cache de l'engine vidé")

        # 2. Vider le cache de la table
        ServiceConfiguration.__table__._columns._all_columns.clear()
        print("✅ Cache des colonnes vidé")

        # 3. Forcer le rechargement des métadonnées
        inspector = inspect(engine)

        # Récupérer la définition réelle depuis la BDD
        columns = inspector.get_columns("service_configurations")

        for col in columns:
            if col["name"] == "service_name":
                print(f"✅ Colonne service_name en BDD : {col['type']}")

        print("\n✅ Cache nettoyé avec succès !")
        print("👉 Redémarre maintenant l'application avec : uvicorn app.main:app --reload")

    except Exception as e:
        print(f"❌ Erreur : {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    clear_enum_cache()
