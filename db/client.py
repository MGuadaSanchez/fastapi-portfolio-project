### Mongo Client### Server local

# Descarga version community: https://www.mongodb.com/try/download
# Instalación: https://www.mongodb.com/docs/manual/tutorial
# Módulo de conexión Mongo DB: pip install pymongo
# Ejecución: sudo mongod --dbpath "path\a\la\dabase\de\datos"
# Conexión: mongodb://localhost

import os
from pymongo import MongoClient


#Base de datos local
#db_client = MongoClient().local

#Base de datos remota
MONGO_DB_URL = os.getenv("MONGO_DB_URL")
if MONGO_DB_URL is None:
    raise ValueError("Error: La variable de entorno MONGO_DB_URL no está definida.")

client = MongoClient(MONGO_DB_URL)
db_client = client.get_default_database()

