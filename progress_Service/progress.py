# Solicita al usuario un user_id, el level completado, y si fue completado con éxito.
# Registra la acción en un log y confirma la operación.
# Envía un evento al bus cuando el progreso es actualizado.
# Verifica que el nivel sea completado antes de enviar la actualización.

import logging
import os
import json
import socket

# Configuración básica de logging
LOG_DIR = "./logs"
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "progress.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Configuración del bus de servicios
BUS_HOST = os.getenv("BUS_HOST", "localhost")  # Dirección del bus
BUS_PORT = int(os.getenv("BUS_PORT", 5000))   # Puerto del bus por defecto

def send_to_bus(event):
    """
    Envía un evento al bus de servicios utilizando sockets.
    :param event: Diccionario con la información del evento.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((BUS_HOST, BUS_PORT))
            s.sendall(json.dumps(event).encode('utf-8'))
            logging.info(f"Evento enviado al bus: {event}")
            print(f"Evento enviado al bus: {event}")
    except Exception as e:
        logging.error(f"Error al enviar el evento al bus: {e}")
        print(f"Error al enviar el evento al bus: {e}")

def update_progress(user_id, level, completed):
    """
    Actualiza el progreso del usuario en el juego.
    :param user_id: ID del usuario.
    :param level: Nivel que el usuario completó.
    :param completed: Booleano que indica si el nivel fue completado.
    """
    if not completed:
        raise ValueError(f"El usuario {user_id} no completó el nivel {level}.")

    logging.info(f"Usuario {user_id} completó el nivel {level}.")
    print(f"Usuario {user_id} completó el nivel {level}.")

    # Crear el evento de progreso y enviarlo al bus
    event = {
        "action": "progress_update",
        "user_id": user_id,
        "level": level,
        "completed": completed
    }
    send_to_bus(event)

if __name__ == "__main__":
    # MVP: Función simple para probar el progreso
    print("=== Servicio de Progreso (Conectado al Bus) ===")
    user_id = input("Introduce el ID del usuario: ")
    level = input("Introduce el nivel que completó: ")
    completed = input("¿El nivel fue completado? (s/n): ").lower() == "s"

    try:
        update_progress(user_id, level, completed)
    except ValueError as e:
        logging.warning(e)
        print(f"Advertencia: {e}")
    except Exception as e:
        logging.error(f"Error: {e}")
        print(f"Error: {e}")
