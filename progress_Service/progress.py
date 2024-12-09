import os
import logging
import json
import socket
from bus_conf import send_to_bus_response,register_service, receive_from_bus
"""
servicio que maneja el progress del usuario, para saber en que nivel se encuentra
"""

# Configuración de logging
LOG_DIR = "./logs"
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "progreso.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def handle_response(sock, content):
    try:
        cont = content.get("content", {})
        data = cont.get("data", None) #resultado de la consulta
        logging.info(f"datos encontrados {data}")

        if not data: #no se encontraron datos
            logging.info(f"no se encontraron datos")
            send_to_bus_response(sock, "progr", {"message": "El usuario no ha completado ningún nivel"})
            return

        elif isinstance(data, list): #[] select
            for d in data:
                nivel= d.get("nombre_nivel", None)
                id_nivel=d.get("id", None)
            send_to_bus_response(sock, "progr", {"message": "Nivel entregado" ,"nivel_actual": nivel, "id_nivel": id_nivel})
        elif isinstance(data, dict): #{} update
            if "consulta exitosa" in data:  # Registro exitoso
                logging.info(f"Nuevo nivel desbloqueado: {data}")
                send_to_bus_response(sock, "progr", {"message": "Nuevo nivel desbloqueado"})
            else:
                logging.warning(f"Formato inesperado en el diccionario: {data}")
                send_to_bus_response(sock, "progr", {"message": "Formato inesperado en el resultado"})
        else:
            logging.error(f"Formato desconocido en data: {data}")
            send_to_bus_response(sock, "progr", {"message": "Error al registrar usuario"})
        

        if not data: #no se encontraron datos
            logging.info(f"no se encontraron datos")
            send_to_bus_response(sock, "progr", {"message": "El usuario no ha completado ningún nivel"})
            return
    except Exception as e:
        logging.error(f"Error al manejar respuesta: {e}")
        send_to_bus_response(sock, "progr", {"message": "Error en el servidor"})
        

def handle_solicitud(sock, content):
    #recibo el id del usuario
    """
    1. Ver el nivel actual del usuario
    2. Actualizar el nivel actual del usuario
    """
    try:
        contenido=content.get("content", {})
        id_user=contenido.get("id")
        opcion=contenido.get("opcion")
        if opcion==1: #preguntar por el nivel actual
            sql= f"""SELECT niveles.nombre_nivel, niveles.id
                    FROM progresion
                    JOIN niveles ON progresion.nivel_id = niveles.id
                    WHERE progresion.usuario_id = '{id_user}'
                    ORDER BY progresion.fecha_completado DESC
                    LIMIT 1;"""
            send_to_bus_response(sock, "condb", {"sql": sql})
        elif opcion==2: #actualizar el nivel actual
            nivel=contenido.get("nivel")
            sql=f"""UPDATE progresion
                    SET estado = 'finalizado', fecha_completado = CURRENT_TIMESTAMP
                    WHERE usuario_id = '{id_user}' AND nivel_id = '{nivel}';"""

            
            send_to_bus_response(sock, "condb", {"sql": sql})
        else:
            logging.error(f"Opción no válida")
            send_to_bus_response(sock, "progr", {"message": "Opción no válida"})
    except Exception as e:
        logging.error(f"Error al manejar solicitud de información: {e}")
        send_to_bus_response(sock, "progr", {"message": "Error en el servidor"})

if __name__ == "__main__":
    logging.info("Iniciando servicio de progreso..")
    print("Iniciando servicio de progreso...")
    sock=register_service("progr")
    try:
        while True:
            message = receive_from_bus(sock)
            action = message.get("action")
            if not message:
                continue
            #ver si es solicitud o respuesta
            if "status" in message: #respuesta
                if action != "progr":
                    handle_response(sock,message)
                else:
                    logging.info(f"Respuesta a cliente")

            elif action == "progr": #solicitud
                handle_solicitud(sock,message)
            else:
                logging.error(f"mensaje a otro servidor")
    except Exception as e:
        logging.error(f"Error: {e}")
