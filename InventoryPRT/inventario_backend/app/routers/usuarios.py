# inventario_backend/app/routers/usuarios.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import crud

from ..schemas import schemas  # Importaciones relativas
from ..database.database import get_db

router = APIRouter(
    prefix="/users",
    tags=["Usuarios"]
)


@router.post("/", response_model=schemas.UsuarioInDB, status_code=status.HTTP_201_CREATED)
def create_user_endpoint(user: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    """Crea un nuevo usuario."""
    db_user = crud.get_user(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)

# Nota: El endpoint /users/me (para obtener el usuario actual) está en auth.py
# porque requiere autenticación y está más relacionado con el flujo de sesión.
