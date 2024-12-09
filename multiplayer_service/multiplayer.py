import os
import logging
import json
import socket
from bus_conf import send_to_bus_response,register_service, receive_from_bus
"""
servicio que tiene la logica para jugar en formato multiplayer
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
            send_to_bus_response(sock, "multi", {"message": "Error en el servidor"})
            return
            
        if isinstance(data, dict): #modificacion o eliminacion
            if "consulta exitosa" in data: 
                logging.info(f"Modificación exitosa: {data}")
                send_to_bus_response(sock, "multi", {"message": "Modificación exitosa", "data": data})
            else:
                logging.warning(f"Formato inesperado en el diccionario: {data}")
                send_to_bus_response(sock, "multi", {"message": "Formato inesperado en el resultado"})
        else:
            logging.error(f"Formato desconocido en data: {data}")
            send_to_bus_response(sock, "multi", {"message": "Error al registrar usuario"})
    except Exception as e:
        logging.error(f"Error al manejar respuesta: {e}")
        send_to_bus_response(sock, "multi", {"message": "Error en el servidor"})


def handle_solicitud(sock, content):
    try:
        """ recibe en id_usuario, id_encontrado y el id_nivel suponiendo que ya paso el nivel

        """
        contenido=content.get("content", {})
        id_usuario = contenido.get("id_usuario", None)
        id_encontrado = contenido.get("id_encontrado", None)
        id_nivel = contenido.get("id_nivel", None)

        sql= f"""UPDATE progresion
                SET estado = 'finalizado', fecha_completado = CURRENT_TIMESTAMP
                WHERE nivel_id = {id_nivel}
                AND usuario_id IN ({id_usuario}, {id_encontrado});"""
        send_to_bus_response(sock, "condb", {"sql": sql})
    except Exception as e:
        logging.error(f"Error al manejar solicitud: {e}")
        send_to_bus_response(sock, "multi", {"message": "Error en el servidor"})
        

if __name__ == "__main__":
    logging.info("Iniciando servicio de multiplayer...")
    print("Iniciando servicio de gestión de multiplayer...")
    sock=register_service("multi")
    try:
        while True:
            message = receive_from_bus(sock)
            action = message.get("action")
            if not message:
                continue
            #ver si es solicitud o respuesta
            if "status" in message: #respuesta
                if action != "multi":
                    handle_response(sock,message)
                else:
                    logging.info(f"Respuesta a cliente")

            elif action == "multi": #solicitud
                handle_solicitud(sock,message)
            else:
                logging.error(f"mensaje a otro servidor")
    except Exception as e:
        logging.error(f"Error: {e}")
