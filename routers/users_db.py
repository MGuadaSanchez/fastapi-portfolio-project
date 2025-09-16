from fastapi import APIRouter, HTTPException, status
from db.models.user import User, UserCreate, UserUpdate
from db.schemas.user import user_schema, users_schema
from db.client import db_client
from db.crud import user as user_crud # Importamos el nuevo módulo CRUD

router = APIRouter(prefix="/userdb",
                   tags=["UserDB"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})

@router.get("/", response_model=list[User])
async def get_all_users():
    """Endpoint para obtener todos los usuarios."""
    users_list = user_crud.get_all_users(db_client)
    return users_schema(users_list)

@router.get("/{id}", response_model=User)
async def get_user_by_id(id: str):
    """Endpoint para obtener un usuario por su ID."""
    user_doc = user_crud.get_user_by_id(db_client, id)
    if not user_doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontró el usuario.")
    return User(**user_schema(user_doc))

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def add_user(user: UserCreate):
    """Endpoint para añadir un nuevo usuario."""
    if user_crud.get_user_by_email(db_client, user.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El email ya está en uso.")

    new_user_id = user_crud.create_user(db_client, user)
    new_user_doc = user_crud.get_user_by_id(db_client, new_user_id)
    
    return User(**user_schema(new_user_doc))

@router.put("/{id}", response_model=User)
async def update_user(id: str, user_data: UserUpdate):
    """Endpoint para actualizar el username y/o email de un usuario."""
    if not user_data.dict(exclude_unset=True):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No hay datos para actualizar.")

    if user_data.email:
        existing_user = user_crud.get_user_by_email(db_client, user_data.email)
        if existing_user and str(existing_user["_id"]) != id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El email ya está en uso.")

    if user_crud.update_user_in_db(db_client, id, user_data) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontró el usuario para actualizar.")

    updated_user_doc = user_crud.get_user_by_id(db_client, id)
    return User(**user_schema(updated_user_doc))

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: str):
    """Endpoint para eliminar un usuario por su ID."""
    if user_crud.delete_user_in_db(db_client, id) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se pudo eliminar el usuario.")