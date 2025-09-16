from fastapi import APIRouter, HTTPException, status
from db.models.product import Product
from db.schemas.product import product_schema, products_schema
from db.client import db_client
from bson import ObjectId

# --- Router Setup ---
# Se define el router con un prefijo, etiquetas para la documentación y una respuesta de error por defecto.
router = APIRouter(prefix="/productdb",    
                   tags=["ProductDB"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}}) 

# --- Helper Function ---
def find_product(field: str, key: any):
    """Función auxiliar para buscar un producto por un campo específico (ej. 'name' o '_id')."""
    try:
        product = db_client.products.find_one({field: key})
        if product:
            return Product(**product_schema(product))
    except:
        return None
    return None


# --- API Endpoints ---

@router.get("/", response_model=list[Product])
async def get_all_products():
    """Endpoint para obtener todos los productos de la base de datos."""
    return products_schema(db_client.products.find())

@router.get("/{id}", response_model=Product)
async def get_product_by_id(id: str):
    """Endpoint para obtener un producto por su ID."""
    product = find_product("_id", ObjectId(id))
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontró el producto.")
    return product

@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
async def add_product(product: Product):
    """Endpoint para añadir un nuevo producto."""
    if find_product("name", product.name):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El producto ya existe.")
    
    product_dict = dict(product)
    del product_dict["id"]
    
    id = db_client.products.insert_one(product_dict).inserted_id   
    
    # Se construye el objeto de respuesta directamente para ahorrar una consulta a la BD
    return Product(id=str(id), name=product.name, stock=product.stock)

@router.put("/", response_model=Product)
async def update_product(product: Product):
    """Endpoint para actualizar un producto existente."""
    product_dict = dict(product)
    del product_dict["id"]

    # Validación de nombre de producto único
    existing_product = find_product("name", product.name)
    if existing_product and existing_product.id != product.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El nombre del producto ya está en uso.")

    # Buscamos y actualizamos el producto
    found = db_client.products.find_one_and_replace({"_id": ObjectId(product.id)}, product_dict)
    
    if not found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontró el producto para actualizar.")

    return find_product("_id", ObjectId(product.id))


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(id: str):
    """Endpoint para eliminar un producto por su ID."""
    found = db_client.products.find_one_and_delete({"_id": ObjectId(id)})
           
    if not found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se pudo eliminar el producto.")