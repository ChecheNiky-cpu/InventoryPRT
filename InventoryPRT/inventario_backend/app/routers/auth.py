# inventario_backend/app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from ..database import crud

from ..models import models

from ..schemas import schemas  # Importaciones relativas
from ..database.database import get_db

router = APIRouter(
    prefix="/auth",  # Prefijo para todas las rutas de este archivo
    tags=["Autenticación"]  # Etiqueta para la documentación
)


@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Endpoint para iniciar sesión y obtener un token JWT.
    Recibe username y password en form-data.
    """
    user = crud.get_user(db, username=form_data.username)
    if not user or not crud.verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=crud.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = crud.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me", response_model=schemas.UsuarioInDB)
async def read_users_me(current_user: models.Usuario = Depends(crud.get_current_user)):
    """
    Endpoint protegido que devuelve la información del usuario
    autenticado actualmente (basado en el token JWT).
    """
    return current_user
