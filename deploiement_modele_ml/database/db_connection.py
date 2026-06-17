from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://attrition_user:Attrition2026!@localhost:5432/employes_db")