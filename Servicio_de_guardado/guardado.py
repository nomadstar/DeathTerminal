import os
import psycopg2
from datetime import datetime

# Configuración de la base de datos
DB_HOST = os.getenv("POSTGRES_HOST", "postgresdb")
DB_NAME = os.getenv("POSTGRES_DB", "db")
DB_USER = os.getenv("POSTGRES_USER", "user")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")

def guardar_progreso(usuario_id, nivel_id):
    try:
        fecha_completado = datetime.now()

        # Conexión a la base de datos
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()

        # Inserción en la tabla progresion
        insert_query = """
        INSERT INTO progresion (usuario_id, nivel_id, fecha_completado)
        VALUES (%s, %s, %s);
        """
        cursor.execute(insert_query, (usuario_id, nivel_id, fecha_completado))
        conn.commit()

        cursor.close()
        conn.close()
        print("Progreso guardado exitosamente.")
    except Exception as e:
        print("Error al guardar el progreso:", e)

if __name__ == "__main__":
    # Simulación de entrada de usuario
    usuario_id = int(input("Ingrese el usuario_id: "))
    nivel_id = int(input("Ingrese el nivel_id: "))
    guardar_progreso(usuario_id, nivel_id)
