import os
from getpass import getpass

import uvicorn

password = getpass("Contraseña de PostgreSQL: ")

# solo vive en este proceso, no se escribe en el .env
os.environ["POSTGRES_PASSWORD"] = password

uvicorn.run("main:app", host="127.0.0.1", port=8000)