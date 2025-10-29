# inventario_backend/app/models.py
from sqlalchemy import Column, Integer, String
# Importación relativa dentro del paquete 'app'
from ..database.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)


class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True, nullable=False)
    # Permitir nulos si no siempre hay categoría
    categoria = Column(String, index=True, nullable=True)
    cantidad = Column(Integer, default=0, nullable=False)
    # Permitir nulos si no siempre aplica
    stock_minimo = Column(Integer, default=0, nullable=True)
