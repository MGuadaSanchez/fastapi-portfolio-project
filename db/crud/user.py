"""Módulo CRUD para operaciones de la base de datos con usuarios."""

from bson import ObjectId
from passlib.context import CryptContext
from pymongo.database import Database

# Los modelos Pydantic son necesarios para el type hinting en las funciones
from ..models.user import UserCreate, UserUpdate

# Configuración del hasheo de contraseñas
crypt = CryptContext(schemes=["bcrypt"])

# --- Funciones de Búsqueda ---

def get_user_by_id(db: Database, user_id: str) -> dict | None:
    """Busca un usuario por su ID."""
    try:
        return db.users.find_one({"_id": ObjectId(user_id)})
    except:
        return None

def get_user_by_email(db: Database, email: str) -> dict | None:
    """Busca un usuario por su email."""
    return db.users.find_one({"email": email})

def get_user_by_username(db: Database, username: str) -> dict | None:
    """Busca un usuario por su username."""
    return db.users.find_one({"username": username})

def get_all_users(db: Database) -> list:
    """Obtiene todos los usuarios."""
    return list(db.users.find())

# --- Funciones de Escritura ---

def create_user(db: Database, user: UserCreate) -> str:
    """Crea un nuevo usuario en la base de datos y devuelve su ID."""
    user_dict = user.dict()
    user_dict["hashed_password"] = crypt.hash(user.password)
    del user_dict["password"]
    user_dict["disabled"] = False
    
    inserted_id = db.users.insert_one(user_dict).inserted_id
    return str(inserted_id)

def update_user_in_db(db: Database, user_id: str, user_data: UserUpdate) -> int:
    """Actualiza un usuario."""
    update_data = user_data.dict(exclude_unset=True)
    if not update_data:
        return 0 # No hay datos para actualizar
            
    result = db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": update_data}
    )
    return result.matched_count

def delete_user_in_db(db: Database, user_id: str) -> int:
    """Elimina un usuario. Devuelve 1 si se eliminó, 0 si no se encontró."""
    result = db.users.find_one_and_delete({"_id": ObjectId(user_id)})
    return 1 if result else 0