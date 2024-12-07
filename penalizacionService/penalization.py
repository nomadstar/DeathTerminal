# Funcion send_to_bus(event): Simula el envío de un evento al bus de servicios.
# Cada penalización genera un evento con los datos relevantes, que se puede usar para integrar otros servicios.
#Hay un archivoo logs donde se guardan los errores

import logging
import os
import json
import socket
from bus_conf import send_to_bus_response,register_service, receive_from_bus

# Configuración básica de logging
LOG_DIR = "./logs"
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "penalization.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def handle_response(sock, content):
    contenido = content.get("content", {}) #sentencia sql
    data = contenido.get("data", None) #resultado de la consulta
    #respuesta de la base de datos
    if isinstance(data, dict):
        if "consulta exitosa" in data:
            logging.info(f"Modificación exitosa: {data}")
            send_to_bus_response(sock, "elimi", {"data": "consulta exitosa"})
        else:
            logging.warning(f"Formato inesperado en el diccionario: {data}")
            send_to_bus_response(sock, "elimi", {"data": "Formato inesperado en el resultado"})
    else:
        logging.error(f"Formato desconocido en data: {data}")
        send_to_bus_response(sock, "elimi", {"data": "Error al registrar usuario"})
       

def penalize_user(sock, content):
    """
    Aplica una penalización al usuario y envía un evento al bus.
    :param user_id: ID del usuario a penalizar.
    :param penalty_type: Tipo de penalización ("ban", "warning").
    """
    contenido=content.get("content", {})
    user_id = contenido.get("user_id")
    sql= f"DELETE FROM usuarios WHERE id = {user_id}"
    send_to_bus_response(sock,"condb", {"sql": sql})
    
if __name__ == "__main__":
    logging.info("Iniciando servicio de penalización...")
    print("Iniciando servicio de penalización...")
    sock=register_service("elimi")
    try:
        while True:
            message = receive_from_bus(sock)
            action = message.get("action")
            if not message:
                continue
            #ver si es solicitud o respuesta
            if "status" in message: #respuesta
                if action != "elimi":
                    handle_response(sock,message)
                else:
                    logging.info(f"Respuesta a cliente")

            elif action == "elimi": #solicitud
                penalize_user(sock,message)
            else:
                logging.error(f"mensaje a otro servidor")
    except Exception as e:
        logging.error(f"Error: {e}")
