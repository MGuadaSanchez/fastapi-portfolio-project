from dotenv import load_dotenv
import os

# --- ÚLTIMO INTENTO: RUTA ABSOLUTA ---
env_path = "C:/Users/Guada/Documents/PROGRAMACION/python/FastAPI/.env"
print(f"--- Intentando cargar .env desde la ruta absoluta: {env_path} ---")
load_dotenv(dotenv_path=env_path)
# ------------------------------------

#pip install fastapi
#pip install "uvicorn[standard]"
#o 
#pip install "fastapi[all]" se instalan los dos anteriores y mas

from fastapi import FastAPI
from routers import products,  jwt_auth_users, users_db
from dotenv import load_dotenv
from pathlib import Path

# --- Carga robusta de variables de entorno ---
# Construye la ruta absoluta al directorio del script actual
BASE_DIR = Path(__file__).resolve().parent
# Le dice a dotenv que cargue el archivo .env que está en ese directorio
load_dotenv(dotenv_path=BASE_DIR / ".env")
# -----------------------------------------

#creo una variable y llamo a la clase FastAPI
app = FastAPI() #instanciamos FastAPI(?)

#Routers|
app.include_router(products.router)
app.include_router(jwt_auth_users.router)
app.include_router(users_db.router)

# Inicia el server en local con: uvicorn main:app --reload
# URL local: http://127.0.0.1:8000
# URL en vivo: https://guada-fastapi-api.onrender.com

@app.get("/")
async def root():
    return "Hola FastAPI"


#pestaña Url: http://127.0.0.1:8000/url
@app.get("/url")
async def url():
    return {"url: " : "Pagina http:host/url"}

# Documentación local con Swagger: http://127.0.0.1:8000/docs
# Documentación en vivo con Swagger: https://guada-fastapi-api.onrender.com/docs
# Documentación con Redocly: http://127.0.0.1:8000/redoc
