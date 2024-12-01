import os
import psycopg2
from datetime import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configuración de la base de datos desde variables de entorno
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_NAME = os.getenv("POSTGRES_DB", "db")
DB_USER = os.getenv("POSTGRES_USER", "user")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")

# Ruta para guardar progreso
@app.route('/guardar_progreso', methods=['POST'])
def guardar_progreso():
    try:
        data = request.json
        usuario_id = data.get('usuario_id')
        nivel_id = data.get('nivel_id')

        print("Datos recibidos:", data)
        print("usuario_id:", usuario_id, "nivel_id:", nivel_id)



        if not usuario_id or not nivel_id:
            return jsonify({"error": "Faltan parámetros usuario_id o nivel_id"}), 400

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

        return jsonify({"message": "Progreso guardado exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
