import os

SECRET_KEY = os.getenv("SECRET_KEY")
if SECRET_KEY is None:
    raise ValueError("Error: La variable de entorno SECRET_KEY no está definida.")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30