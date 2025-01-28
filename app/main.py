from fastapi import FastAPI
from  app.routers import declaraciones, usuarios, nombramientos
from app.database import create_tables
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Declaraciones API",
    description="API para el manejo de declaraciones patrimoniales",
    version="0.3",
)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# creacion de tablas para la aplicacion
@app.on_event("startup")
async def startup():
    create_tables()

# incluir las rutas de los diferentes modulos   
app.include_router(declaraciones.router, prefix="/api", tags=["declaraciones"])
app.include_router(usuarios.router, prefix="/api", tags=["usuarios"])
app.include_router(nombramientos.router, prefix="/api", tags=["nombramientos"])

@app.get("/")
async def root():
    return {"message": "Bienvenido a la API de Gestión de Declaraciones Patrimoniales"}
