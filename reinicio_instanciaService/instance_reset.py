# Solicita al usuario un user_id, instance_id y si cumple las condiciones para reiniciar.
# Registra la acción en un log y confirma la operación.
# Envía un evento al bus cuando se reinicia una instancia.
# Verifica que se cumplan las condiciones antes de realizar el reinicio.
#usado si esta en un nivel y quiere reiniciar el nivel

import logging
import os
import json
import socket
from bus_conf import send_to_bus_response, register_service, receive_from_bus
# Configuración básica de logging
LOG_DIR = "./logs"
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "instance_reset.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
def handle_response(sock, content):
    try:
        cont = content.get("content", {})
        data = cont.get("data", None) #resultado de la consulta
        logging.info(f"datos encontrados {data}")

        if isinstance(data, dict):
            datos_actualizados = data.get("consulta exitosa", None)
            if "consulta exitosa" in data and datos_actualizados>0:  # Registro exitoso
                logging.info(f"reinicio exitoso: {data}")
                send_to_bus_response(sock, "reini", {"message": "nivel reiniciado exitosamente"})
            else:
                logging.warning(f"No se actualizo ningun dato: {data}")
                send_to_bus_response(sock, "reini", {"message": "No se cumple con las condiciones para reiniciar"})
        else:
            logging.error(f"Formato desconocido en data: {data}")
            send_to_bus_response(sock, "reini", {"message": "Error al reiniciar el nivel"})
    except Exception as e:
        logging.error(f"Error al manejar respuesta: {e}")
        send_to_bus_response(sock, "reini", {"message": "Error en el servidor"})
        

def handle_solicitud(sock, content):
    try:
        "id usuario y id del nivel"
        contenido=content.get("content", {})
        id_usuario=contenido.get("id", None)
        id_nivel=contenido.get("nivel", None)

        if id_nivel:
            #consiciones para reiniciar
            # consulta sql para volver a mi nivel actual
            sql = f"""UPDATE progresion
                    SET estado = 'en_proceso', fecha_inicio = CURRENT_TIMESTAMP
                    WHERE usuario_id = {id_usuario} AND nivel_id = {id_nivel} AND estado = 'finalizado';
                    """
            send_to_bus_response(sock, "condb", {"sql": sql})
        else:
            logging.error(f"Error al obtener el nivel")
            send_to_bus_response(sock, "reini", {"message": "Error al obtener el nivel"})


    except Exception as e:
        logging.error(f"Error al manejar solicitud de información: {e}")
        send_to_bus_response(sock, "reini", {"message": "Error en el servidor"})

if __name__ == "__main__":
    logging.info("Iniciando servicio de reinicio de instancia...")
    print("Iniciando servicio de gestión de reinicio de instancia...")
    sock=register_service("reini")
    try:
        while True:
            message = receive_from_bus(sock)
            action = message.get("action")
            if not message:
                continue
            #ver si es solicitud o respuesta
            if "status" in message: #respuesta
                if action != "reini":
                    handle_response(sock,message)
                else:
                    logging.info(f"Respuesta a cliente")

            elif action == "reini": #solicitud
                handle_solicitud(sock,message)
            else:
                logging.error(f"mensaje a otro servidor")
    except Exception as e:
        logging.error(f"Error: {e}")
