import os
import logging

from bus_conf import send_to_bus_response,register_service, receive_from_bus

# Configuración de logging
LOG_DIR = "./logs"
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "permisos.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
pending_requests = {}
def handle_response(sock, content):
    try:
        cont = content.get("content", {})
        data = cont.get("data", []) #resultado de la consulta
        tipo= data[0].get("tipo_usuario", None) #tipo de usuario
        logging.info(f"El tipo de usuario es: {tipo}")

        if tipo == "admin": #es administrador
            logging.info(f"el usuario es administrador")
            send_to_bus_response(sock, "permi", {"message": True})
        else:
            logging.info(f"el usuario no es administrador")
            send_to_bus_response(sock, "permi", {"message": False})


    except Exception as e:
        logging.error(f"Error al manejar respuesta: {e}")
        send_to_bus_response(sock, "permi", {"message": "Error en el servidor"})
        
def permisos(sock, content):
    try:
        #recibo el id para ver si el usuario es de tipo administrador
        contenido=content.get("content", {})
        id= contenido.get("id")

        sql= f"SELECT Tipo_usuario FROM usuarios WHERE id = {id}"
        send_to_bus_response(sock, "condb", {"sql": sql})

    except Exception as e:
        logging.error(f"Error al manejar solicitudes: {e}")
        send_to_bus_response(sock, "permi", {"message": "Error en el servidor"})

if __name__ == "__main__":
    logging.info("Iniciando servicio de permisos...")
    print("Iniciando servicio de gestión de permisos...")
    sock=register_service("permi")
    try:
        while True:
            message = receive_from_bus(sock)
            action = message.get("action")
            if not message:
                continue
            #ver si es solicitud o respuesta
            if "status" in message: #respuesta de la base
                if action != "permi":
                    handle_response(sock,message)
                else:
                    logging.info(f"Respuesta a cliente")

            elif action == "permi": #solicitud
                permisos(sock,message)
            else:
                logging.error(f"mensaje a otro servidor")
    except Exception as e:
        logging.error(f"Error: {e}")

