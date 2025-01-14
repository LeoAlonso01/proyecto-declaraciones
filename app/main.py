from fastapi import FastAPI
from  app.routers import declaraciones, usuarios, nombramientos
from app.database import create_tables

app = FastAPI(
    title="Declaraciones API",
    description="API para el manejo de declaraciones patrimoniales",
    version="0.1",
)

# creacion de tablas para la aplicacion
@app.on_event("startup")
async def startup():
    await create_tables()

# incluir las rutas de los diferentes modulos   
app.include_router(declaraciones.router)
app.include_router(usuarios.router)
app.include_router(nombramientos.router)

@app.get("/")
async def root():
    return {"message": "Bienvenido a la API de Gestión de Declaraciones Patrimoniales"}
