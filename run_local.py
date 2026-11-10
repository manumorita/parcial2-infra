
import os
from getpass import getpass

import uvicorn

# Solicitar la contraseña sin mostrarla en pantalla
password = getpass("Contraseña de PostgreSQL: ")

# Guardarla temporalmente en el entorno del proceso
os.environ["POSTGRES_PASSWORD"] = password

# Iniciar la API
uvicorn.run("main:app", host="127.0.0.1", port=8000)
