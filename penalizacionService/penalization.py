# Ejecuta el archivo penalization.py dentro del contenedor correspondiente o localmente con Python.
# Introduce un ID de usuario cuando se solicite.
# Selecciona el tipo de penalización: ban (baneado) o warning (advertencia).
# El servicio:
# Registra la penalización en el archivo penalization.log dentro de la carpeta logs.
# Muestra un mensaje en consola confirmando la penalización aplicada.
# Si introduces un tipo de penalización no válido, mostrará un error claro.

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

if __name__ == "__main__":
    # MVP: Función simple para probar la penalización
    print("=== Servicio de Penalización (MVP) ===")
    user_id = input("Introduce el ID del usuario: ")
    penalty_type = input("Introduce el tipo de penalización ('ban' o 'warning'): ").lower()

    try:
        penalize_user(user_id, penalty_type)
    except Exception as e:
        print(f"Error: {e}")
