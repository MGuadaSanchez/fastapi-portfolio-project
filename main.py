from dotenv import load_dotenv
import os

# --- ÚLTIMO INTENTO: RUTA ABSOLUTA ---
env_path = "C:/Users/Guada/Documents/PROGRAMACION/python/FastAPI/.env"
print(f"--- Intentando cargar .env desde la ruta absoluta: {env_path} ---")
load_dotenv(dotenv_path=env_path)
# ------------------------------------

from fastapi import FastAPI
from routers import products,  jwt_auth_users, users_db


#creo una variable y llamo a la clase FastAPI
app = FastAPI() #instanciamos FastAPI(?)

#Routers|
app.include_router(products.router)
app.include_router(jwt_auth_users.router)
app.include_router(users_db.router)

#Inicia el server con: uvicorn main:app --reload
#Url local: http://127.0.0.1:8000

@app.get("/")
async def root():
    return "Hola FastAPI"


#pestaña Url: http://127.0.0.1:8000/url
@app.get("/url")
async def url():
    return {"url: " : "Pagina http:host/url"}

#Documentación con Swagger: http://127.0.0.1:8000/docs
#Documentación con Redocly: http://127.0.0.1:8000/redoc
