from fastapi import APIRouter

# ruta para nombramientos
router = APIRouter()

@router.get("/nombramientos")
async def get_nombramientos():
    return {"message": "Lista de nombramientos"}

@router.post("/nombramientos")
async def create_nombramiento(nombramiento: dict):
    return {"message": "Nombramiento creado", "nombramiento": nombramiento}
