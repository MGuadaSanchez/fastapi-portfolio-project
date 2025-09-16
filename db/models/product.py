"""Define el modelo de datos Pydantic para la entidad Producto."""

from pydantic import BaseModel

class Product(BaseModel):
    """Modelo que representa un producto en la aplicación."""
    id : str | None = None  # ID único del producto (opcional ingresarlo, lo genera MongoDB).
    name : str              # Nombre único del producto.
    stock : int             # Cantidad de stock disponible.
