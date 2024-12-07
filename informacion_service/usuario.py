import os
import logging
import json
import socket
from bus_conf import send_to_bus_response,register_service, receive_from_bus
"""
servicio que maneja la informacion del usuario, datos usuario y el nivel en el que se encuentra
"""

# Configuración de logging
LOG_DIR = "./logs"
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "info.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def handle_response(sock, content):
    try:
        cont = content.get("content", {})
        data = cont.get("data", []) #resultado de la consulta
        logging.info(f"datos encontrados {data}")
        

        if data and len(data) == 0: #no se encontraron datos
            logging.info(f"no se encontraron datos")
            send_to_bus_response(sock, "infou", {"message": "no se encontraron los datos"})
        else:
            for d in data:
                id= d.get("id", None)
                nombre= d.get("nombre", None)
                email= d.get("email", None)
                tipo= d.get("Tipo_usuario", None)
                nivel= d.get("nombre_nivel", None)
                dificultad= d.get("dificultad", None)
            logging.info(f"datos encontrados")
            send_to_bus_response(sock, "infou", {"id": id, "nombre": nombre, "email": email, "tipo usuario": tipo, "nivel": nivel, "dificultad": dificultad})
    except Exception as e:
        logging.error(f"Error al manejar respuesta: {e}")
        send_to_bus_response(sock, "infou", {"message": "Error en el servidor"})
        

def handle_solicitud(sock, content):
    try:
        contenido=content.get("content", {})
        id=contenido.get("id", None)

        #preguntar por las caracteristicas del usuario
        sql = f"""SELECT usuarios.id, usuarios.nombre, usuarios.email, usuarios.Tipo_usuario, niveles.nombre_nivel, niveles.dificultad
                FROM usuarios
                LEFT JOIN progresion ON usuarios.id = progresion.usuario_id
                LEFT JOIN niveles ON progresion.nivel_id = niveles.id
                WHERE usuarios.id = '{id}'
                ORDER BY progresion.fecha_completado DESC
                LIMIT 1"""

        send_to_bus_response(sock, "condb", {"sql": sql})
    except Exception as e:
        logging.error(f"Error al manejar solicitud de información: {e}")
        send_to_bus_response(sock, "infou", {"message": "Error en el servidor"})

if __name__ == "__main__":
    logging.info("Iniciando servicio de información del usuario...")
    print("Iniciando servicio de gestión de información del usuario...")
    sock=register_service("infou")
    try:
        while True:
            message = receive_from_bus(sock)
            action = message.get("action")
            if not message:
                continue
            #ver si es solicitud o respuesta
            if "status" in message: #respuesta
                if action != "infou":
                    handle_response(sock,message)
                else:
                    logging.info(f"Respuesta a cliente")

            elif action == "infou": #solicitud
                handle_solicitud(sock,message)
            else:
                logging.error(f"mensaje a otro servidor")
    except Exception as e:
        logging.error(f"Error: {e}")
