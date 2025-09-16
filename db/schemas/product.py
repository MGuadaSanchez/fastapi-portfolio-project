"""Módulo de schemas para transformar datos de productos de MongoDB a diccionarios de Python."""

def product_schema(product) -> dict:
    """Convierte un documento de producto de MongoDB a un diccionario."""
    return {"id" : str(product["_id"]),
            "name" : product["name"],
            "stock" : product ["stock"]}
    
def products_schema(products) -> list:
    """Convierte una lista de documentos de producto a una lista de diccionarios."""
    return [product_schema(product) for product in products]