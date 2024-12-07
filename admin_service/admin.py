import os
import logging
import json
import socket
from bus_conf import send_to_bus_response,register_service, receive_from_bus
"""
servicio que maneja el panel de administrador: gestionar permisos, ver progreso de los usuarios,
eliminar usuarios, inscribir usuarios administradores
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
            send_to_bus_response(sock, "iadmi", {"message": "Error en el servidor"})
            return
            
        # lista, ver usuarios o los niveles
        if isinstance(data, list): 
            if len(data) > 0: 
                logging.info(f"datos encontrados: {data}")
                send_to_bus_response(sock, "iadmi", {"message": "Datos encontrados", "data": data})
            else:
                logging.info(f"No se encontraron datos")
                send_to_bus_response(sock, "iadmi", {"message": "No se encontraron datos"})
        elif isinstance(data, dict): #modificacion o eliminacion
            if "consulta exitosa" in data: 
                logging.info(f"Modificación exitosa: {data}")
                send_to_bus_response(sock, "iadmi", {"message": "Modificación exitosa", "data": data})
            else:
                logging.warning(f"Formato inesperado en el diccionario: {data}")
                send_to_bus_response(sock, "iadmi", {"message": "Formato inesperado en el resultado"})
        else:
            logging.error(f"Formato desconocido en data: {data}")
            send_to_bus_response(sock, "iadmi", {"message": "Error al registrar usuario"})
    except Exception as e:
        logging.error(f"Error al manejar respuesta: {e}")
        send_to_bus_response(sock, "iadmi", {"message": "Error en el servidor"})


def handle_solicitud(sock, content):
    try:
        """ recibe en contenido la opcion
        1- ver usuarios
        2- eliminar usuarios
        3- ver todos los niveles
        4- modificar niveles
        5- eliminar niveles
        """
        contenido=content.get("content", {})
        opcion= contenido.get("opcion", None)

        if opcion == "1":
            sql= "SELECT * FROM usuarios"
            send_to_bus_response(sock, "condb", {"sql": sql})
        elif opcion == "2": #servicio de penalizacion
            id_eliminar= contenido.get("id", None)
            send_to_bus_response(sock, "elimi", {"user_id": id_eliminar})
        elif opcion == "3":
            sql= "SELECT * FROM niveles"
            send_to_bus_response(sock, "condb", {"sql": sql})
        elif opcion == "4":
            id_modificar= contenido.get("id", None)
            nivel= contenido.get("nivel", None)
            dificultad= contenido.get("dificultad", None)
            sql= f"UPDATE progresion SET nivel_id = {nivel}, dificultad = {dificultad} WHERE usuario_id = {id_modificar}"
            send_to_bus_response(sock, "condb", {"sql": sql})
        elif opcion == "5":
            id_eliminar= contenido.get("id", None)
            sql= f"DELETE FROM niveles WHERE id = {id_eliminar}"
            send_to_bus_response(sock, "condb", {"sql": sql})
    except Exception as e:
        logging.error(f"Error al manejar solicitud de login: {e}")
        send_to_bus_response(sock, "iadmi", {"message": "Error en el servidor"})

if __name__ == "__main__":
    logging.info("Iniciando servicio de gestión de panel de administradores...")
    print("Iniciando servicio de gestión de panel de administradores...")
    sock=register_service("iadmi")
    try:
        while True:
            message = receive_from_bus(sock)
            action = message.get("action")
            if not message:
                continue
            #ver si es solicitud o respuesta
            if "status" in message: #respuesta
                if action != "iadmi":
                    handle_response(sock,message)
                else:
                    logging.info(f"Respuesta a cliente")

            elif action == "iadmi": #solicitud
                handle_solicitud(sock,message)
            else:
                logging.error(f"mensaje a otro servidor")
    except Exception as e:
        logging.error(f"Error: {e}")
