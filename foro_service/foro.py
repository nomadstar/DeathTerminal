import os
import logging
import json
import socket
from bus_conf import send_to_bus_response,register_service, receive_from_bus
"""
servcio de sistemas de foros
"""

# Configuración de logging
LOG_DIR = "./logs"
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "foro.log"),
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
            send_to_bus_response(sock, "foros", {"message": "Error en el servidor"})
            return
            
        if isinstance(data, list): #lista: ver mis publicaciones, o todas las publicaciones
            if len(data)>0:
                logging.info(f"Consulta exitosa: {data}")
                send_to_bus_response(sock, "foros", {"message": "Consulta exitosa", "data": data})
            else:
                logging.info(f"No hay publicaciones")
                send_to_bus_response(sock, "foros", {"message": "No hay publicaciones"})

        elif isinstance(data, dict): #insertar una publicacion
            if "consulta exitosa" in data: 
                logging.info(f"Inserción exitosa: {data}")
                send_to_bus_response(sock, "foros", {"message": "Modificación exitosa", "data": data})
            else:
                logging.warning(f"Formato inesperado en el diccionario: {data}")
                send_to_bus_response(sock, "foros", {"message": "Formato inesperado en el resultado"})
        else:
            logging.error(f"Formato desconocido en data: {data}")
            send_to_bus_response(sock, "foros", {"message": "Error al registrar usuario"})
    except Exception as e:
        logging.error(f"Error al manejar respuesta: {e}")
        send_to_bus_response(sock, "foros", {"message": "Error en el servidor"})


def handle_solicitud(sock, content):
    try:
        """ recibe en contenido la opcion
        1- ver mis publicaciones
        2- realizar una publicación
        3- ver todos las publicaciones
        """
        contenido=content.get("content", {})
        opcion= contenido.get("opcion", None)

        if opcion == 1:
            id_usuario= contenido.get("id", None)
            sql= f"SELECT * FROM publicaciones WHERE usuario_id = {id_usuario}"
            send_to_bus_response(sock, "condb", {"sql": sql})
        elif opcion == 2: 
            id_usuario= contenido.get("id", None)
            tema= contenido.get("tema", None)
            mensaje= contenido.get("mensaje", None)
            sql= f"INSERT INTO publicaciones (usuario_id, tema, mensaje) VALUES ({id_usuario}, '{tema}', '{mensaje}')"
            send_to_bus_response(sock, "condb", {"sql": sql})
        elif opcion == 3:
            sql= "SELECT * FROM publicaciones LIMIT 5"
            send_to_bus_response(sock, "condb", {"sql": sql})
        else:
            logging.error(f"Opcion no válida")
            send_to_bus_response(sock, "foros", {"message": "Opcion no válida"})
    except Exception as e:
        logging.error(f"Error al manejar solicitud de login: {e}")
        send_to_bus_response(sock, "foros", {"message": "Error en el servidor"})

if __name__ == "__main__":
    logging.info("Iniciando servicio de foro...")
    print("Iniciando servicio de foro...")
    sock=register_service("foros")
    try:
        while True:
            message = receive_from_bus(sock)
            action = message.get("action")
            if not message:
                continue
            #ver si es solicitud o respuesta
            if "status" in message: #respuesta
                if action != "foros":
                    handle_response(sock,message)
                else:
                    logging.info(f"Respuesta a cliente")

            elif action == "foros": #solicitud
                handle_solicitud(sock,message)
            else:
                logging.error(f"mensaje a otro servidor")
    except Exception as e:
        logging.error(f"Error: {e}")
