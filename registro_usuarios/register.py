import os
import logging
import json
import socket
from bus_conf import send_to_bus_response, register_service, receive_from_bus
# Configuración de logging
LOG_DIR = "./logs"
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "registro_usuarios.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
pending_requests = {}
#funcion que procesa las respuestas recibidas
def handle_response(sock, content):
    try:
        status = content.get("status")
        action = content.get("action")
        contenido = content.get("content", {}) #sentencia sql
        data = contenido.get("data", []) #resultado de la consulta                

        #recuperar datos del diccionario
        lista_rec= pending_requests.pop(sock)
        nombre = lista_rec.get("nombre")
        email = lista_rec.get("email")
        user_password = lista_rec.get("user_password")

        #verificar si el usuario existe o no
        if data and len(data) >0: #el usuario existe
            logging.info(f"el usuario ya existe")
            send_to_bus_response(sock, "regis", {"message": "Usuario ya existe"})
        elif isinstance(data,list) and len(data)==0:#registrar el usuario
            sql= f"INSERT INTO usuarios (nombre, email, user_password, Tipo_usuario) VALUES ('{nombre}', '{email}', '{user_password}', 'usuario')"
            send_to_bus_response(sock, "condb", {"sql": sql})
        elif action == "condb" and status == "OK":
            logging.info(f"registro exitoso")
            send_to_bus_response(sock, "regis", {"message": "Usuario registrado exitosamente"})
        else:
            logging.info(f"Error al registrar usuario")
            send_to_bus_response(sock, "regis", {"message": "Error al registrar usuario"})
    except Exception as e:
        logging.error(f"Error al manejar respuesta: {e}")
        send_to_bus_response(sock, "regis", {"message": "Error en el servidor"})

def handle_registro(sock, content):
    try:
        contenido=content.get("content", {})
        nombre = contenido.get("nombre")
        email = contenido.get("email")
        user_password = contenido.get("user_password")
        # Agregar a la lista s
        pending_requests[sock] = {"nombre": nombre, "email": email, "user_password": user_password}

        # Construir y enviar la consulta SQL
        sql = f"SELECT * FROM usuarios WHERE nombre = '{nombre}'"
        send_to_bus_response(sock, "condb", {"sql": sql})
     
    except Exception as e:
        print(f"Error al manejar solicitud de registro: {e}")
        logging.error(f"Error al manejar solicitud de registro: {e}")
        send_to_bus_response(sock, "regis", {"message": "Error interno del servidor"})

      
if __name__ == "__main__":
    logging.info("Iniciando servicio de registro de usuarios...")
    print("Iniciando servicio de registro de usuarios...")
    sock=register_service("regis")
    try:
        while True:
            message = receive_from_bus(sock)
            action = message.get("action")
            if not message:
                continue
            #ver si es solicitud o respuesta
            if "status" in message: #respuesta
                if action != "regis":
                    handle_response(sock,message)
                else:
                    logging.info(f"Respuesta a cliente")
            elif action == "regis": #solicitud
                handle_registro(sock,message)
            else:
                logging.error(f"mensaje a otro servidor")
    except Exception as e:
        logging.error(f"Error: {e}")
