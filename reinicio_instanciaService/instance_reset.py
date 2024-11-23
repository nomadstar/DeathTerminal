# Solicita al usuario un user_id, instance_id y si cumple las condiciones para reiniciar.
# Registra la acción en un log y confirma la operación.
# Envía un evento al bus cuando se reinicia una instancia.
# Verifica que se cumplan las condiciones antes de realizar el reinicio.

import logging
import os
import json
import socket

# Configuración básica de logging
LOG_DIR = "./logs"
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "instance_reset.log"),
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

def reset_instance(user_id, instance_id, condition_met):
    """
    Reinicia una instancia de juego si se cumplen las condiciones.
    :param user_id: ID del usuario solicitando el reinicio.
    :param instance_id: ID de la instancia a reiniciar.
    :param condition_met: Booleano que indica si se cumple la condición para reiniciar.
    """
    if not condition_met:
        raise PermissionError(f"El usuario {user_id} no cumple las condiciones para reiniciar la instancia {instance_id}.")

    logging.info(f"Usuario {user_id} reinició la instancia {instance_id}.")
    print(f"Usuario {user_id} reinició la instancia {instance_id}.")

    # Crear el evento de reinicio y enviarlo al bus
    event = {
        "action": "instance_reset",
        "user_id": user_id,
        "instance_id": instance_id
    }
    send_to_bus(event)

if __name__ == "__main__":
    # MVP: Función simple para probar el reinicio de instancias
    print("=== Servicio de Reinicio de Instancias (Conectado al Bus) ===")
    user_id = input("Introduce el ID del usuario: ")
    instance_id = input("Introduce el ID de la instancia a reiniciar: ")
    condition_met = input("¿Se cumple la condición para reiniciar? (s/n): ").lower() == "s"

    try:
        reset_instance(user_id, instance_id, condition_met)
    except PermissionError as e:
        logging.warning(e)
        print(f"Advertencia: {e}")
    except Exception as e:
        logging.error(f"Error: {e}")
        print(f"Error: {e}")
