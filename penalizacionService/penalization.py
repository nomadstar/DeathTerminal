# Funcion send_to_bus(event): Simula el envío de un evento al bus de servicios.
# Cada penalización genera un evento con los datos relevantes, que se puede usar para integrar otros servicios.
#Hay un archivoo logs donde se guardan los errores

import logging
import os

# Configuración básica de logging
LOG_DIR = "./logs"
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "penalization.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Simulación de comunicación con el bus de servicios
def send_to_bus(event):
    """
    Envía un evento al bus de servicios.
    :param event: Diccionario con la información del evento.
    """
    logging.info(f"Evento enviado al bus: {event}")
    print(f"Evento enviado al bus: {event}")

def penalize_user(user_id, penalty_type):
    """
    Aplica una penalización al usuario.
    :param user_id: ID del usuario a penalizar
    :param penalty_type: Tipo de penalización ("ban", "warning")
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
    print("=== Servicio de Penalización (Mejorado) ===")
    user_id = input("Introduce el ID del usuario: ")
    penalty_type = input("Introduce el tipo de penalización ('ban' o 'warning'): ").lower()

    try:
        penalize_user(user_id, penalty_type)
    except Exception as e:
        logging.error(f"Error procesando penalización: {e}")
        print(f"Error: {e}")
