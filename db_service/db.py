import os
import logging
import json
import socket
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from datetime import datetime, date
from bus_conf import send_to_bus_response, register_service, receive_from_bus

# Cargar variables de entorno
load_dotenv()

# Configuración de logging
LOG_DIR = "./logs"
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "db_service.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Configuración de PostgreSQL
DB_CONFIG = {
    "dbname": os.getenv("POSTGRES_DB", "db"),
    "user": os.getenv("POSTGRES_USER", "user"),
    "password": os.getenv("POSTGRES_PASSWORD", "password"),
    "host": os.getenv("POSTGRES_HOST", "db"),
    "port": 5432
}

def connect():
    """
    Función para crear una sesión con la base de datos usando SQLAlchemy.
    """
    db_url = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@" \
             f"{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    return Session()

def execute_query(sql,params=None):
    """
    Ejecuta una consulta SQL en la base de datos.
    :param sql: Consulta SQL a ejecutar.
    :param params: Parámetros para la consulta SQL.
    :return: Resultado de la consulta en formato JSON.
    """
    try:
        session = connect()
        logging.info(f"consulta SQL: {sql}")

        # Ejecutar la consulta
        if params:
            result = session.execute(text(sql), params)
        else:
            result = session.execute(text(sql))

        session.commit()

        # Si es SELECT, obtiene los resultados
        if result.returns_rows:
            result_list = []
            column_names = result.keys()
            for row in result:
                row_dict = dict(zip(column_names, row))
                result_list.append(row_dict)
            session.close()
            # Convertir a JSON
            json_result = json.dumps(result_list, ensure_ascii=False, default=str)
            return json_result  # Lista en formato JSON
        else:
            # otras consultas
            affected_rows = result.rowcount
            session.close()
            json_result = json.dumps({"consulta exitosa": affected_rows})
            return json_result
    except Exception as e:
        logging.error(f"Error al ejecutar consulta SQL: {e}")
        # Devolver el error en formato JSON
        json_result = json.dumps({"error": str(e)})
        return json_result


def consultas(sock, content):
    contenido = content.get("content", {})
    query = contenido.get("sql")
    params = contenido.get("params")

    # Ejecutar la consulta y obtener resultados
    json_result = execute_query(query,params)
    logging.info(f"Resultado de la consulta: {json_result}")

    try:
        result_content = json.loads(json_result)

        if isinstance(result_content, list):
            send_to_bus_response(sock, "condb", {"data": result_content})
        elif isinstance(result_content, dict) and "error" in result_content:
            logging.error(f"Error en la consulta: {result_content}")
            send_to_bus_response(sock, "condb", {"data":result_content})
        elif isinstance(result_content, dict) and "error" not in result_content:
            logging.info(f"Consulta exitosa: {result_content}")
            send_to_bus_response(sock, "condb", {"data": result_content})
        else:
            logging.warning(f"Formato de resultado desconocido: {result_content}")
            send_to_bus_response(sock, "condb", {"error": "Formato desconocido en el resultado SQL"})
    except json.JSONDecodeError as e:
        logging.error(f"Error al decodificar JSON: {e}")
        send_to_bus_response(sock, "condb", {"error": "Error al procesar el resultado SQL"})


if __name__ == "__main__":
    logging.info("Iniciando servicio de consultas db...")
    print("Iniciando servicio de gestión de consultas db...")
    sock=register_service("condb")
    try:
        while True:
            message = receive_from_bus(sock)
            action = message.get("action")
            if not message:
                continue
            #ver si es solicitud
            if action == "condb": #solicitud
                consultas(sock,message)
            else:
                logging.error(f"mensaje a otro servidor")
    except Exception as e:
        logging.error(f"Error: {e}")
