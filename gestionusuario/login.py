import os
import logging
import json
import socket
from bus_conf import send_to_bus_response,register_service, receive_from_bus

# Configuración de logging
LOG_DIR = "./logs"
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "gestion_usuarios.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
pending_requests = {}
def handle_response(sock, content):
    try:
        cont = content.get("content", {})
        data = cont.get("data", []) #resultado de la consulta
        for d in data:
            id= d.get("id", None)
    
        #datos de la lista
        lista_rec = pending_requests.pop(sock)
        nombre = lista_rec.get("nombre")
        user_password = lista_rec.get("user_password")

        if data and len(data) > 0: #credendiales correctas
            logging.info(f"credenciales correctas")
            #ver si es administrador
            send_to_bus_response(sock, "login", {"message": "credenciales correctas"})
            send_to_bus_response(sock, "permi", {"id":id})
            respuesta= receive_from_bus(sock)
            if respuesta.get("content", {}).get("data", {}).get("tipo") != "admin":
                #send_to_bus_response(sock, "login", {"message": "permisos de usuario"})
            else:
                logging.info(f"el usuario no es administrador")
                #send_to_bus_response(sock, "login", {"message": "permisos de administrador"})
            
        else:
            logging.info(f"el usuario no existe o credenciales invalidas")
            send_to_bus_response(sock, "login", {"message": "Usuario no existe"})

    except Exception as e:
        logging.error(f"Error al manejar respuesta: {e}")
        send_to_bus_response(sock, "login", {"message": "Error en el servidor"})
        

def handle_login(sock, content):
    try:
        """
        formato del mensaje: {"sql": "SELECT * FROM tabla" ..}

        usado para saber el servicio que envia la consulta y poder responderle
        """
        contenido=content.get("content", {})
        nombre = contenido.get("nombre")
        user_password = contenido.get("user_password")
        pending_requests[sock] = {"nombre": nombre, "user_password": user_password}

        #verificar credenciales en la base de datos
        sql = f"SELECT * FROM usuarios WHERE nombre = '{nombre}' AND user_password = '{user_password}'"
        send_to_bus_response(sock, "condb", {"sql": sql})
    except Exception as e:
        logging.error(f"Error al manejar solicitud de login: {e}")
        send_to_bus_response(sock, "login", {"message": "Error en el servidor"})

if __name__ == "__main__":
    logging.info("Iniciando servicio de gestión de usuarios...")
    print("Iniciando servicio de gestión de usuarios...")
    sock=register_service("login")
    try:
        while True:
            message = receive_from_bus(sock)
            action = message.get("action")
            if not message:
                continue
            #ver si es solicitud o respuesta
            if "status" in message: #respuesta
                if action != "login":
                    handle_response(sock,message)
                else:
                    logging.info(f"Respuesta a cliente")

            elif action == "login": #solicitud
                handle_login(sock,message)
            else:
                logging.error(f"mensaje a otro servidor")
    except Exception as e:
        logging.error(f"Error: {e}")
