"""Router para la autenticación de usuarios y gestión de tokens JWT."""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

# --- Mis Imports ---
from db.models.user import User
from db.client import db_client
from db.schemas.user import user_schema
from db.crud import user as user_crud # Importamos el nuevo módulo CRUD
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(tags=["Auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
crypt = CryptContext(schemes=["bcrypt"])

@router.post("/login", summary="Crea un token de acceso para el usuario")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # El campo 'username' del formulario se usa para el email
    user_doc = user_crud.get_user_by_email(db_client, form_data.username)
    
    if not user_doc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email o contraseña incorrectos"
        )

    password_match = crypt.verify(form_data.password, user_doc["hashed_password"])

    if not password_match:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email o contraseña incorrectos"
        )
        
    if user_doc["disabled"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tu cuenta está desactivada"
        )

    # El 'sub' del token será el username
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token_payload = {
        "sub": user_doc["username"],
        "exp": expire
    }
    
    access_token = jwt.encode(access_token_payload, SECRET_KEY, algorithm=ALGORITHM)
    
    return {"access_token": access_token, "token_type": "bearer"}

async def get_current_active_user(token: str = Depends(oauth2_scheme)) -> User:
    """
    Decodifica el token JWT para obtener el username, busca al usuario en la BD
    y devuelve el usuario si está activo.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    user_doc = user_crud.get_user_by_username(db_client, username)
    if user_doc is None:
        raise credentials_exception
        
    if user_doc["disabled"]:
        raise HTTPException(status_code=400, detail="Tu cuenta está desactivada")
        
    return User(**user_schema(user_doc))

@router.get("/users/me", response_model=User, summary="Obtiene los datos del usuario actual")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user