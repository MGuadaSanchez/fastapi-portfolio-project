"""Módulo de schemas para transformar datos de usuarios de MongoDB a diccionarios de Python."""

def user_schema(user) -> dict:
    """Convierte un documento de usuario de MongoDB a un diccionario."""
    return {"id" : str(user["_id"]),
            "username": user["username"],
            "email" : user ["email"]}
    
def users_schema(users) -> list:
    """Convierte una lista de documentos de usuario a una lista de diccionarios."""
    return [user_schema(user) for user in users]