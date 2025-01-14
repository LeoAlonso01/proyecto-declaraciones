from fastapi import APIRouter

# primera ruta para la API de declaraciones

router = APIRouter()

@router.get("/declaraciones")
async def read_declaraciones():
    return {"message": "Ruta para obtener declaraciones"}