import os
import logging
import json
import socket
from bus_conf import send_to_bus_response,register_service, receive_from_bus
"""
servicio que buscar si un usuario esta en mi mismo nivel
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
            send_to_bus_response(sock, "busca", {"message": "Error en el servidor"})
            return
            
        # lista, ver usuarios o los niveles
        if isinstance(data, list): 
            id_encontrado= data[0].get("id", None)
            nombre_compañero= data[0].get("nombre", None)

            if len(data) > 0: 
                logging.info(f"datos encontrados: {data}")
                send_to_bus_response(sock, "busca", {"message": "Datos encontrados", "id_encontrado": id_encontrado, "usuario_encontrado": nombre_compañero})
            else:
                logging.info(f"No se encontraron datos")
                send_to_bus_response(sock, "busca", {"message": "No se encontraron datos"})
        else:
            logging.error(f"Formato desconocido en data: {data}")
            send_to_bus_response(sock, "busca", {"message": "Error al registrar usuario"})
    except Exception as e:
        logging.error(f"Error al manejar respuesta: {e}")
        send_to_bus_response(sock, "busca", {"message": "Error en el servidor"})


def handle_solicitud(sock, content):
    try:
        #recibe id_usuario y el id del nivel
        contenido=content.get("content", {})
        id_usuario=contenido.get("id", None)
        id_nivel=contenido.get("nivel", None)
        sql= f"""SELECT usuarios.id, usuarios.nombre, progresion.nivel_id
                FROM progresion
                JOIN usuarios ON progresion.usuario_id = usuarios.id
                WHERE progresion.nivel_id = {id_nivel}
                AND progresion.estado = 'en_proceso'
                AND usuarios.id != {id_usuario}
                LIMIT 1;
                """
        send_to_bus_response(sock, "condb", {"sql": sql})
    except Exception as e:
        logging.error(f"Error al manejar solicitud de login: {e}")
        send_to_bus_response(sock, "busca", {"message": "Error en el servidor"})

if __name__ == "__main__":
    logging.info("Iniciando servicio de emparejamiento...")
    print("Iniciando servicio de emparejamiento...")
    sock=register_service("busca")
    try:
        while True:
            message = receive_from_bus(sock)
            action = message.get("action")
            if not message:
                continue
            #ver si es solicitud o respuesta
            if "status" in message: #respuesta
                if action != "busca":
                    handle_response(sock,message)
                else:
                    logging.info(f"Respuesta a cliente")

            elif action == "busca": #solicitud
                handle_solicitud(sock,message)
            else:
                logging.error(f"mensaje a otro servidor")
    except Exception as e:
        logging.error(f"Error: {e}")
