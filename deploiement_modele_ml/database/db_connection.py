import os
from sqlalchemy import create_engine

# Si on est dans GitHub Actions (CI), pas de DB
if os.getenv("CI"): # si la variable CI existe dans l'environnement on est sur github
    engine = None
else:
    engine = create_engine("postgresql+psycopg2://attrition_user:Attrition2026!@localhost:5432/employes_db")