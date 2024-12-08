import os
import psycopg2
from datetime import datetime
from bus_conf import send_to_bus_response,register_service, receive_from_bus

# Configuración básica de logging
LOG_DIR = "./logs"
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "penalization.log"),
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
            send_to_bus_response(sock, "savee", {"message": "Error en el servidor"})
            return
        
        if isinstance(data, dict): #modificacion o inserccion
            if "consulta exitosa" in data: 
                logging.info(f"Modificación exitosa: {data}")
                send_to_bus_response(sock, "savee", {"message": "Modificación exitosa", "data": data})
            else:
                logging.warning(f"Formato inesperado en el diccionario: {data}")
                send_to_bus_response(sock, "savee", {"message": "Formato inesperado en el resultado"})
        else:
            logging.error(f"Formato desconocido en data: {data}")
            send_to_bus_response(sock, "savee", {"message": "Error al registrar usuario"})
    except Exception as e:
        logging.error(f"Error al manejar respuesta: {e}")
        send_to_bus_response(sock, "savee", {"message": "Error en el servidor"})


def handle_solicitud(sock, content):
    try:
        """ 
        servicio usado para guardar el progreso, recibe el usuario_id y el nivel_id
        """
        contenido=content.get("content", {})
        id_usuario= contenido.get("id_usuario", None)
        id_nivel= contenido.get("id_nivel", None)
        #guardar el progreso
       sql = f"""INSERT INTO progresion (usuario_id, nivel_id, fecha_completado)
                    VALUES ({id_usuario}, {id_nivel}, CURRENT_TIMESTAMP)
                    ON CONFLICT (usuario_id, nivel_id)
                    DO UPDATE SET fecha_completado = CURRENT_TIMESTAMP;"""
        send_to_bus_response(sock, "condb", {"sql": sql})

        
    except Exception as e:
        logging.error(f"Error al manejar solicitud de login: {e}")
        send_to_bus_response(sock, "savee", {"message": "Error en el servidor"})



if __name__ == "__main__":
    # Simulación de entrada de usuario
    usuario_id = int(input("Ingrese el usuario_id: "))
    nivel_id = int(input("Ingrese el nivel_id: "))
    guardar_progreso(usuario_id, nivel_id)

if __name__ == "__main__":
    logging.info("Iniciando servicio de gestión de panel de guardado...")
    print("Iniciando servicio de guardado de instancias...")
    sock=register_service("savee")
    try:
        while True:
            message = receive_from_bus(sock)
            action = message.get("action")
            if not message:
                continue
            #ver si es solicitud o respuesta
            if "status" in message: #respuesta
                if action != "savee":
                    handle_response(sock,message)
                else:
                    logging.info(f"Respuesta a cliente")

            elif action == "savee": #solicitud
                handle_solicitud(sock,message)
            else:
                logging.error(f"mensaje a otro servidor")
    except Exception as e:
        logging.error(f"Error: {e}")

