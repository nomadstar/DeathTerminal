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

def execute_query(sql):
    """
    Ejecuta una consulta SQL en la base de datos.
    :param sql: Consulta SQL a ejecutar.
    :param params: Parámetros para la consulta SQL.
    :return: Resultado de la consulta en formato JSON.
    """
    params = None
    try:
        session = connect()
        logging.info(f"consulta SQL: {sql}")

        # Ejecutar la consulta
        if params is not None:
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
            json_result = json.dumps({"acción realizada"})
            return json_result
    except Exception as e:
        logging.error(f"Error al ejecutar consulta SQL: {e}")
        # Devolver el error en formato JSON
        json_result = json.dumps({"error": str(e)})
        return json_result


def consultas(sock, content):
    contenido = content.get("content", {})
    query = contenido.get("sql")

    # Ejecutar la consulta y obtener resultados
    json_result = execute_query(query)

    logging.info(f"Resultado de la consulta SQL: {json_result}")

    try:
        result_content = json.loads(json_result)

        if isinstance(result_content, list):
            logging.info(f"Consulta exitosa: {result_content}")
            send_to_bus_response(sock, "condb", {"data": result_content})
        elif isinstance(result_content, dict) and "error" in result_content:
            logging.error(f"Error en la consulta: {result_content}")
            ##send_to_bus_response(sock, content["r"], result_content)
            send_to_bus_response(sock, "condb", {result_content})
        else:
            logging.warning(f"Formato de resultado desconocido: {result_content}")
            send_to_bus_response(sock, "condb", {"error": "Formato desconocido en el resultado SQL"})
    except json.JSONDecodeError as e:
        logging.error(f"Error al decodificar JSON: {e}")
        send_to_bus_response(sock, "condb", {"error": "Error al procesar el resultado SQL"})


if __name__ == "__main__":
    logging.info("Iniciando servicio de consultas db...")
    print("Iniciando servicio de consultasdb...")
    sock=register_service("condb")
    try:
        while True:
            try:
                message = receive_from_bus(sock)
                if not message:
                    continue

                action = message.get("action")
                if not action:
                    logging.error(f"Mensaje inválido: {message}")
                    continue

                # Ver si es solicitud o respuesta
                if "status" in message:  # Respuesta
                    if action != "condb":  # Si no es para este servicio
                        logging.info("Respuesta no destinada a este servidor")
                        print("Respuesta no destinada a este servidor")
                    else:
                        logging.info("Respuesta a cliente")
                elif action == "condb":  # Solicitud
                    consultas(sock, message)
                else:
                    logging.error(f"Mensaje a otro servidor: {message}")
                    print(f"Mensaje a otro servidor: {message}")
            except Exception as inner_e:
                logging.error(f"Error interno durante el ciclo: {inner_e}")
                print(f"Error interno durante el ciclo: {inner_e}")
    except Exception as e:
        logging.error(f"Error principal: {e}")

