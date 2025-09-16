# Proyecto API RESTful con FastAPI

API RESTful desarrollada con FastAPI y MongoDB para gestionar usuarios y productos. Incluye autenticación de usuarios con tokens JWT.

## Características

- **Autenticación de Usuarios:** Sistema de registro y login con tokens JWT (JSON Web Tokens).
- **Gestión de Usuarios:** Operaciones CRUD (Crear, Leer, Actualizar, Borrar) para usuarios.
- **Ruta Protegida:** Endpoint `/users/me` que solo es accesible con un token válido.
- **Gestión de Productos:** Operaciones CRUD completas para productos.
- **Documentación Automática:** Documentación interactiva de la API disponible en `/docs` (Swagger UI) y `/redoc`.

## Tecnologías Utilizadas

- **Backend:** FastAPI
- **Base de Datos:** MongoDB
- **Autenticación:** Python-JOSE (JWT), Passlib (hashing)
- **Servidor ASGI:** Uvicorn
- **Modelos de Datos:** Pydantic
- **Variables de Entorno:** Python-dotenv

## Instalación y Puesta en Marcha

Sigue estos pasos para ejecutar el proyecto en tu máquina local.

**1. Clona el repositorio**
```bash
git clone https://github.com/MGuadaSanchez/fastapi-portfolio-project.git
cd fastapi-portfolio-project
```

**2. Crea un entorno virtual (Recomendado)**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

**3. Instala las dependencias**
```bash
pip install -r requirements.txt
```

**4. Configura las variables de entorno**
Crea un archivo llamado `.env` en la raíz del proyecto y añade las siguientes variables:
```
MONGO_DB_URL="tu_url_de_conexion_a_mongodb"
SECRET_KEY="una_clave_secreta_larga_y_aleatoria"
```

**5. Inicia el servidor**
```bash
uvicorn main:app --reload
```
El servidor estará disponible en `http://127.0.0.1:8000`.

## Documentación de la API

Una vez que el servidor esté en marcha, puedes acceder a la documentación interactiva de la API en las siguientes rutas:

- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
