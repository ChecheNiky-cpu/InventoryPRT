# inventario_backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import auth, productos, usuarios  # Importar los routers

# --- Crear Tablas (si no existen) ---
# Intenta crear las tablas definidas en models.py
try:
    print("Intentando crear tablas...")
    Base.metadata.create_all(bind=engine)
    print("Tablas creadas o ya existentes.")
except Exception as e:
    print(f"Error al inicializar la base de datos: {e}")
    # Considera salir o manejar el error de forma más robusta en producción

# --- Crear Instancia FastAPI ---
app = FastAPI(
    title="API de Inventario",
    description="Backend para la aplicación de gestión de inventario.",
    version="0.1.0"
)

# --- Configuración de CORS ---
# Permitir solicitudes desde cualquier origen durante el desarrollo.
# ¡RESTRÍNGE ESTO EN PRODUCCIÓN!
# Ejemplo: ["http://localhost:3000", "http://localhost:8081", "exp://..."]
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Incluir Routers ---
# Monta los endpoints definidos en los archivos de routers
app.include_router(auth.router)
app.include_router(productos.router)
# Si tienes endpoints específicos de usuarios (aparte de auth)
app.include_router(usuarios.router)

# --- Endpoint Raíz ---


@app.get("/", tags=["Root"])
def read_root():
    """Endpoint raíz de bienvenida."""
    return {"message": "Bienvenido a la API de Inventario v0.1.0"}

# --- (Opcional) Limpieza o configuración adicional al iniciar/cerrar ---
# @app.on_event("startup")
# async def startup_event():
#     print("Iniciando la aplicación FastAPI...")

# @app.on_event("shutdown")
# def shutdown_event():
#     print("Cerrando la aplicación FastAPI...")
