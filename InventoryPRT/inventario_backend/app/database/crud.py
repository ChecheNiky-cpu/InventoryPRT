# inventario_backend/app/crud.py
from sqlalchemy.orm import Session

from ..models import models
from ..schemas import schemas  # Importaciones relativas
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import os
from .database import get_db  # Importar get_db

# --- Configuración Hashing y JWT ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv(
    "SECRET_KEY", "cambiame_por_un_secreto_real_en_.env")  # Cargar desde .env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/token")  # URL relativa al router de auth

# --- Funciones Hashing y JWT ---


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.now(
        timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# --- CRUD Usuarios ---


def get_user(db: Session, username: str) -> Optional[models.Usuario]:
    return db.query(models.Usuario).filter(models.Usuario.username == username).first()


def create_user(db: Session, user: schemas.UsuarioCreate) -> models.Usuario:
    hashed_password = get_password_hash(user.password)
    db_user = models.Usuario(username=user.username,
                             password_hash=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- Autenticación / Usuario Actual ---


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> models.Usuario:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: Optional[str] = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

# --- CRUD Productos ---


def get_producto(db: Session, producto_id: int) -> Optional[models.Producto]:
    return db.query(models.Producto).filter(models.Producto.id == producto_id).first()


def get_productos(db: Session, skip: int = 0, limit: int = 100) -> list[models.Producto]:
    return db.query(models.Producto).offset(skip).limit(limit).all()


def create_producto(db: Session, producto: schemas.ProductoCreate) -> models.Producto:
    db_producto = models.Producto(**producto.model_dump())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto


def update_producto(db: Session, producto_id: int, producto_update: schemas.ProductoUpdate) -> Optional[models.Producto]:
    db_producto = get_producto(db, producto_id)
    if not db_producto:
        return None
    update_data = producto_update.model_dump(exclude_unset=True)  # Pydantic V2
    for key, value in update_data.items():
        setattr(db_producto, key, value)
    db.commit()
    db.refresh(db_producto)
    return db_producto


def delete_producto(db: Session, producto_id: int) -> Optional[models.Producto]:
    db_producto = get_producto(db, producto_id)
    if not db_producto:
        return None
    db.delete(db_producto)
    db.commit()
    # No se puede hacer refresh a un objeto borrado, solo retornamos el objeto antes de borrar
    return db_producto
