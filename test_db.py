import os
import psycopg
from dotenv import load_dotenv
from getpass import getpass

# Cargar las variables del archivo .env
load_dotenv()

# Obtener los datos de conexión
host = os.getenv("POSTGRES_HOST")
port = os.getenv("POSTGRES_PORT")
user = os.getenv("POSTGRES_USER")
database = os.getenv("POSTGRES_DB")
password = os.getenv("POSTGRES_PASSWORD")

# Solicitar la contraseña sin guardarla en el archivo .env
if not password:
    password = getpass("Ingresa la contraseña de PostgreSQL: ")

try:
    with psycopg.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        dbname=database,
        connect_timeout=10
    ) as connection:

        with connection.cursor() as cursor:
            cursor.execute("SELECT current_database(), current_user;")
            result = cursor.fetchone()

            print("¡Conexión exitosa con PostgreSQL!")
            print(f"Base de datos: {result[0]}")
            print(f"Usuario: {result[1]}")

except Exception as error:
    print("No fue posible conectar con PostgreSQL.")
    print(f"Detalle: {error}")
