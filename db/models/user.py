"""Define los modelos de datos Pydantic para la entidad Usuario."""

from pydantic import BaseModel, EmailStr

# =============================================================================
# Modelo Base (Campos Públicos Comunes)
# =============================================================================
class UserBase(BaseModel):
    """Modelo base con campos comunes y públicos para un usuario."""
    username: str
    email: EmailStr

# =============================================================================
# Modelo para Creación (Entrada de API)
# =============================================================================
class UserCreate(UserBase):
    """Modelo para recibir los datos al crear un nuevo usuario."""
    password: str

# =============================================================================
# Modelo para Respuestas de API (Salida)
# =============================================================================
class User(UserBase):
    """Modelo para devolver los datos públicos de un usuario."""
    id: str

# =============================================================================
# Modelo para la Base de Datos (Uso Interno)
# =============================================================================
class UserInDB(UserBase):
    """Modelo que representa al usuario tal como se almacena en la BD,
    incluyendo campos privados."""
    id: str | None = None
    hashed_password: str
    disabled: bool | None = False

# =============================================================================
# Modelo para Actualización (Entrada de API)
# =============================================================================
class UserUpdate(BaseModel):
    """Modelo para recibir los datos al actualizar un usuario existente.
    Todos los campos son opcionales."""
    username: str | None = None
    email: EmailStr | None = None