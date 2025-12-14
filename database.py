import os
import psycopg2


def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", ""),
        dbname=os.getenv("DB_NAME", "toxicidad_db"),
    )


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS predicciones (
            id SERIAL PRIMARY KEY,
            texto TEXT NOT NULL,
            toxicidad SMALLINT NOT NULL,
            probabilidad REAL NOT NULL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    conn.commit()
    cur.close()
    conn.close()


def guardar_prediccion(texto: str, toxicidad: int, probabilidad: float):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO predicciones (texto, toxicidad, probabilidad)
        VALUES (%s, %s, %s)
        """,
        (texto, toxicidad, probabilidad)
    )

    conn.commit()
    cur.close()
    conn.close()