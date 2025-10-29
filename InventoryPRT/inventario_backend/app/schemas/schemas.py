# inventario_backend/app/schemas.py
from pydantic import BaseModel, Field
from typing import Optional

# --- Esquemas de Producto ---


class ProductoBase(BaseModel):
    nombre: str
    categoria: Optional[str] = None
    # Valor por defecto y validación >= 0
    cantidad: int = Field(ge=0, default=0)
    # Valor por defecto y validación >= 0
    stock_minimo: Optional[int] = Field(default=0, ge=0)


class ProductoCreate(ProductoBase):
    pass  # Hereda todos los campos de ProductoBase


class ProductoUpdate(BaseModel):  # Esquema para actualización parcial
    nombre: Optional[str] = None
    categoria: Optional[str] = None
    # None significa no actualizar
    cantidad: Optional[int] = Field(default=None, ge=0)
    stock_minimo: Optional[int] = Field(
        default=None, ge=0)  # None significa no actualizar


class ProductoInDB(ProductoBase):
    id: int  # El ID que viene de la base de datos

    class Config:
        # Para compatibilidad con SQLAlchemy (Pydantic V2+)
        from_attributes = True

# --- Esquemas de Usuario ---


class UsuarioBase(BaseModel):
    username: str


class UsuarioCreate(UsuarioBase):
    password: str  # Se recibe la contraseña en texto plano al crear


class UsuarioInDB(UsuarioBase):
    id: int
    # No exponemos el password_hash

    class Config:
        from_attributes = True

# --- Esquemas para Autenticación (JWT) ---


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
