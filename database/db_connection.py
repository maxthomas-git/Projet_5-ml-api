import os
from sqlalchemy import create_engine

ENV = os.getenv("ENV", "local")

if ENV in ["ci", "hf"]:
    engine = None

elif ENV == "local":
    engine = create_engine(
        "postgresql+psycopg2://attrition_user:Attrition2026!@localhost:5432/employes_db"
    )

else:
    engine = None