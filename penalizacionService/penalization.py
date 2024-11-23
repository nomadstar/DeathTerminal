# Funcion send_to_bus(event): Simula el envío de un evento al bus de servicios.
# Cada penalización genera un evento con los datos relevantes, que se puede usar para integrar otros servicios.
#Hay un archivoo logs donde se guardan los errores

import logging
import os
import json
import socket

# Configuración básica de logging
LOG_DIR = "./logs"
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "penalization.log"),
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

def penalize_user(user_id, penalty_type):
    """
    Aplica una penalización al usuario y envía un evento al bus.
    :param user_id: ID del usuario a penalizar.
    :param penalty_type: Tipo de penalización ("ban", "warning").
    """
    if penalty_type not in ["ban", "warning"]:
        raise ValueError("Tipo de penalización no válido. Use 'ban' o 'warning'.")

    logging.info(f"Usuario {user_id} penalizado con: {penalty_type}.")
    print(f"Usuario {user_id} penalizado con: {penalty_type}.")

    # Crear el evento de penalización y enviarlo al bus
    event = {
        "action": "penalization",
        "user_id": user_id,
        "penalty_type": penalty_type
    }
    send_to_bus(event)

if __name__ == "__main__":
    # MVP: Función simple para probar la penalización
    print("=== Servicio de Penalización (Conectado al Bus) ===")
    user_id = input("Introduce el ID del usuario: ")
    penalty_type = input("Introduce el tipo de penalización ('ban' o 'warning'): ").lower()

    try:
        penalize_user(user_id, penalty_type)
    except Exception as e:
        logging.error(f"Error procesando penalización: {e}")
        print(f"Error: {e}")
