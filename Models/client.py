# Definir el modelo de datos del cliente
from pydantic import BaseModel

class Cliente(BaseModel):
    id: str
    nombre: str
    categoria: str