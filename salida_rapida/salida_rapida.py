import os
import logging
import json
import socket
from bus_conf import send_to_bus_response,register_service, receive_from_bus
 
#si se detecta una falla repentina, se llama al servicio de salida rápida para guardar el nivel actual del usuario.

# Configuración de logging
LOG_DIR = "./logs"
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "salida_rapida.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def handle_solicitud(sock, content):
    #recibo el id del usuario
    try:
        contenido=content.get("content", {})
        id_usuario=contenido.get("usuario_id", None)

        #realizar un guardado en el nivel que se quedo, sin importar si lo completó o no
        #consultar al servico de progreso
        send_to_bus_response(sock, "progr", {"id": id_usuario})
        respuesta=receive_from_bus(sock)
        contenido=respuesta.get("content", {})
        id_nivel=contenido.get("id_nivel", None)
        if id_nivel:
            #guardar en el sistema con el servicio de guardado
            send_to_bus_response(sock, "savee", {"id_usuario": id_usuario, "id_nivel": id_nivel})
            res=receive_from_bus(sock)
            content=res.get("content", {})
            data=content.get("data", None)
            if data:
                logging.info(f"Guardado exitoso")
                send_to_bus_response(sock, "salir", {"message": "Guardado exitoso"})
            else:
                logging.error(f"Error al guardar")
                send_to_bus_response(sock, "salir", {"message": "Error al guardar"})
        else:
            logging.error(f"Error al obtener el nivel")
            send_to_bus_response(sock, "salir", {"message": "Error al obtener el nivel"})
    except Exception as e:
        logging.error(f"Error al manejar solicitud de información: {e}")
        send_to_bus_response(sock, "salir", {"message": "Error en el servidor"})
if __name__ == "__main__":
    logging.info("Iniciando servicio de salida repentina..")
    print("Iniciando servicio de salida repentina...")
    sock=register_service("salir")
    try:
        while True:
            message = receive_from_bus(sock)
            action = message.get("action")
            if not message:
                continue
            if action == "salir": #solicitud
                handle_solicitud(sock,message)
            else:
                logging.error(f"mensaje a otro servidor")
    except Exception as e:
        logging.error(f"Error: {e}")