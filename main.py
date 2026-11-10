import os
import psycopg

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr

load_dotenv()

app = FastAPI(title="API Parcial 2 - Infraestructuras Paralelas")


def obtener_conexion():
    return psycopg.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        dbname=os.getenv("POSTGRES_DB")
    )


class Usuario(BaseModel):
    nombre: str
    correo: EmailStr


@app.on_event("startup")
def crear_tabla():
    with obtener_conexion() as conexion:
        conexion.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                correo VARCHAR(150) UNIQUE NOT NULL
            );
        """)


@app.get("/")
def inicio():
    return {"mensaje": "¡Nuestra API está funcionando!"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/usuarios")
def consultar_usuarios():
    try:
        with obtener_conexion() as conexion:
            filas = conexion.execute(
                "SELECT id, nombre, correo FROM usuarios ORDER BY id"
            ).fetchall()

        lista_usuarios = []
        for fila in filas:
            lista_usuarios.append({
                "id": fila[0],
                "nombre": fila[1],
                "correo": fila[2]
            })
        return lista_usuarios

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="No fue posible consultar los usuarios"
        )


@app.post("/usuarios")
def registrar_usuario(usuario: Usuario):
    try:
        with obtener_conexion() as conexion:
            fila = conexion.execute(
                """
                INSERT INTO usuarios (nombre, correo)
                VALUES (%s, %s)
                RETURNING id, nombre, correo
                """,
                (usuario.nombre, usuario.correo)
            ).fetchone()

        return {"id": fila[0], "nombre": fila[1], "correo": fila[2]}

    except psycopg.errors.UniqueViolation:
        # el correo tiene restricción UNIQUE en la tabla
        raise HTTPException(
            status_code=409,
            detail="Ese correo ya está registrado"
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="No fue posible registrar el usuario"
        )