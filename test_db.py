import os
import psycopg
from dotenv import load_dotenv
from getpass import getpass

load_dotenv()

host = os.getenv("POSTGRES_HOST")
port = os.getenv("POSTGRES_PORT")
user = os.getenv("POSTGRES_USER")
database = os.getenv("POSTGRES_DB")
password = os.getenv("POSTGRES_PASSWORD")

# si la contraseña no está en el .env, se pide por consola
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
        result = connection.execute(
            "SELECT current_database(), current_user;"
        ).fetchone()

        print("¡Conexión exitosa con PostgreSQL!")
        print(f"Base de datos: {result[0]}")
        print(f"Usuario: {result[1]}")

except Exception as error:
    print("No fue posible conectar con PostgreSQL.")
    print(f"Detalle: {error}")