import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

ENV = os.getenv("ENV", "local")

if ENV in ["ci", "hf"]:
    engine = None

elif ENV == "local":
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")

    DATABASE_URL = (
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    engine = create_engine(DATABASE_URL)

else:
    engine = None