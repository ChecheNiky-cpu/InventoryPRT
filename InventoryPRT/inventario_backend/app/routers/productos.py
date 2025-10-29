# inventario_backend/app/routers/productos.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import crud

from ..models import models

from ..schemas import schemas  # Importaciones relativas
from ..database.database import get_db

router = APIRouter(
    prefix="/productos",
    tags=["Productos"],
    # Aplica autenticación a TODAS las rutas aquí
    dependencies=[Depends(crud.get_current_user)]
)


@router.post("/", response_model=schemas.ProductoInDB, status_code=status.HTTP_201_CREATED)
def create_producto_endpoint(
    producto: schemas.ProductoCreate,
    db: Session = Depends(get_db)
    # current_user ya está inyectado por dependencies
):
    """Crea un nuevo producto en el inventario."""
    return crud.create_producto(db=db, producto=producto)


@router.get("/", response_model=List[schemas.ProductoInDB])
def read_productos_endpoint(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Obtiene una lista de productos, con paginación opcional."""
    productos = crud.get_productos(db, skip=skip, limit=limit)
    return productos


@router.get("/{producto_id}", response_model=schemas.ProductoInDB)
def read_producto_endpoint(
    producto_id: int,
    db: Session = Depends(get_db)
):
    """Obtiene un producto específico por su ID."""
    db_producto = crud.get_producto(db, producto_id=producto_id)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto not found")
    return db_producto


@router.put("/{producto_id}", response_model=schemas.ProductoInDB)
def update_producto_endpoint(
    producto_id: int,
    producto_update: schemas.ProductoUpdate,  # Esquema de actualización parcial
    db: Session = Depends(get_db)
):
    """Actualiza un producto existente (parcialmente)."""
    db_producto = crud.update_producto(
        db, producto_id=producto_id, producto_update=producto_update)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto not found")
    return db_producto


@router.delete("/{producto_id}", response_model=schemas.ProductoInDB)
def delete_producto_endpoint(
    producto_id: int,
    db: Session = Depends(get_db)
):
    """Elimina un producto por su ID."""
    db_producto = crud.delete_producto(db, producto_id=producto_id)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto not found")
    # Devuelve el objeto eliminado como confirmación
    return db_producto
