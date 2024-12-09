import os
import logging
import json
import socket
from bus_conf import send_to_bus_response,register_service, receive_from_bus
"""
servicio que maneja el panel de administrador: gestionar permisos, ver progreso de los usuarios,
eliminar usuarios, inscribir usuarios administradores
"""

# Configuración de logging
LOG_DIR = "./logs"
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "admin.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def handle_response(sock, content):
    try:
        contenido = content.get("content", {}) #sentencia sql
        data = contenido.get("data", None) #resultado de la consulta              
        error = contenido.get("error", None) #error en la consulta  

        if error:
            logging.error(f"Error en la consulta SQL: {error}")
            send_to_bus_response(sock, "conte", {"message": "Error en el servidor"})
            return
            
        if isinstance(data, dict): #modificacion o eliminacion
            if "consulta exitosa" in data: 
                logging.info(f"Modificación exitosa: {data}")
                send_to_bus_response(sock, "conte", {"message": "Modificación exitosa", "data": data})
            else:
                logging.warning(f"Formato inesperado en el diccionario: {data}")
                send_to_bus_response(sock, "conte", {"message": "Formato inesperado en el resultado"})
        else:
            logging.error(f"Formato desconocido en data: {data}")
            send_to_bus_response(sock, "conte", {"message": "Error al registrar usuario"})
    except Exception as e:
        logging.error(f"Error al manejar respuesta: {e}")
        send_to_bus_response(sock, "conte", {"message": "Error en el servidor"})


def handle_solicitud(sock, content):
    """
    Recibe una pregunta, respuesta y el id del administrador.
    Inserta un nivel y su trivia asociada.
    """
    try:
        contenido = content.get("content", {})
        pregunta = contenido.get("pregunta", None)
        respuesta = contenido.get("respuesta", None)
        id_admin = contenido.get("id", None)

        sql = f"""
        BEGIN;
        INSERT INTO niveles (nombre_nivel, dificultad, creado_por)
        VALUES ('Nuevo Nivel', 1, {id_admin})
        RETURNING id; -- Obtener el ID del nivel recién creado

        INSERT INTO trivias (nivel_id, pregunta, respuesta, creado_por)
        VALUES (LASTVAL(), '{pregunta}', '{respuesta}', {id_admin});
        COMMIT;
        """
        send_to_bus_response(sock, "condb", {"sql": sql})
    except Exception as e:
        send_to_bus_response(sock, "conte", {"error": f"Error al procesar la solicitud: {e}"})

if __name__ == "__main__":
    logging.info("Iniciando servicio de gestión de panel de administradores...")
    print("Iniciando servicio de gestión de panel de administradores...")
    sock=register_service("conte")
    try:
        while True:
            message = receive_from_bus(sock)
            action = message.get("action")
            if not message:
                continue
            #ver si es solicitud o respuesta
            if "status" in message: #respuesta
                if action != "conte":
                    handle_response(sock,message)
                else:
                    logging.info(f"Respuesta a cliente")

            elif action == "conte": #solicitud
                handle_solicitud(sock,message)
            else:
                logging.error(f"mensaje a otro servidor")
    except Exception as e:
        logging.error(f"Error: {e}")
