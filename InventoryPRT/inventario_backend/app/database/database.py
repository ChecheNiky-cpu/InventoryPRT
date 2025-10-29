# inventario_backend/app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()  # Carga variables desde ../.env

# Construye la ruta relativa al archivo .env
# dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
# load_dotenv(dotenv_path=dotenv_path)


# Default a SQLite dentro de 'app'
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./inventory_app.db")

engine = create_engine(
    DATABASE_URL,
    # connect_args solo es necesario para SQLite
    connect_args={
        "check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Función para obtener una sesión de base de datos (dependencia para FastAPI)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


print(f"Database URL: {DATABASE_URL}")
print(f"Engine created for: {engine.url}")
