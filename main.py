# Importar las bibliotecas necesarias
from fastapi import FastAPI
from Router.routes import router

# Inicializar la aplicación FastAPI
app = FastAPI()
app.include_router(router)