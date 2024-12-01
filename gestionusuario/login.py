import os
import logging
import json
import psycopg2
import socket
import time

from dataclasses import dataclass

# Configuración de logging
LOG_DIR = "./logs"
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "gestion_usuarios.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Configuración del BUS
BUS_HOST = os.getenv("BUS_HOST", "localhost")  # Dirección del bus
BUS_PORT = int(os.getenv("BUS_PORT", 5000))    # Puerto del bus por defecto

# Configuración de PostgreSQL
DB_CONFIG = {
    "dbname": os.getenv("POSTGRES_DB", "db"),
    "user": os.getenv("POSTGRES_USER", "user"),
    "password": os.getenv("POSTGRES_PASSWORD", "password"),
    "host": "db",
    "port": 5432
}
def register_service(sock, prefix):
    try:
        prefix = prefix[:5] #asegurar que tenga 5 caracteres
        registration_message = f"{len('sinit' + prefix):05}sinit{prefix}"
        print(f"Mensaje de registro enviado: {registration_message}")
        sock.sendall(registration_message.encode())
        logging.info(f"Registro del servicio enviado al bus: {registration_message}")

        # Confirmar registro con el bus
        response_length = int(sock.recv(5).decode())
        response = sock.recv(response_length).decode()
        logging.info(f"Respuesta del bus al: {response}")
        if "OK" not in response:
            raise Exception(f"Registro rechazado por el bus: {response}")
        logging.info(f"Servicio registrado correctamente con prefijo: {prefix}")
    except Exception as e:
        logging.error(f"Error al registrar el servicio en el bus: {e}")
        raise

#enviar mensajes al bus
def send_to_bus_response(sock, action, content):
    """
    Envía una respuesta al bus desde el servidor.
    :param sock: Socket conectado al bus.
    :param action: Acción/prefijo del servicio.
    :param content: Diccionario con el contenido de la respuesta.
    """
    try:
        # Serializar el contenido a JSON
        message_content = json.dumps(content)
        prefix = action[:5].ljust(5)  # Asegura que el prefijo sea de 5 caracteres
        full_message = f"{len(prefix + message_content):05}{prefix}{message_content}"

        # Enviar al bus
        sock.sendall(full_message.encode())
        logging.info(f"Respuesta enviada al bus: {full_message}")
    except Exception as e:
        logging.error(f"Error al enviar respuesta al bus: {e}")



#recibir mensaje del bus
def receive_from_bus(sock):
    """
    Recibe un mensaje del bus de servicios utilizando un socket.
    :param sock: Socket conectado al bus.
    :return: Diccionario con la acción y el contenido del mensaje.
    """
    try:
        # Leer los primeros 5 caracteres como longitud del mensaje
        data_length = int(sock.recv(5).decode())
        data = sock.recv(data_length).decode()

        action = data[:5].strip()  # Prefijo de 5 caracteres, login
        content = json.loads(data[5:])  # JSON del contenido

        logging.info(f"Mensaje recibido del bus: {data}")
        print(f"Mensaje recibido del bus: {data}")

        return {"action": action, "content": content}
    except Exception as e:
        logging.error(f"Error al recibir mensaje del bus: {e}")
        print(f"Error al recibir mensaje del bus: {e}")
        return None

#escucha activa del bus y su proceso
def listen_to_bus():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            # Conectar al bus
            sock.connect((BUS_HOST, BUS_PORT))
            logging.info("Conectado al bus de servicios")

            # Registrar el servicio en el bus con el prefijo "login"
            register_service(sock, "login")

            # Escuchar mensajes del bus
            while True:
                message = receive_from_bus(sock)
                if message:
                    action = message["action"]
                    content = message["content"]
                    logging.info(f"Mensaje recibido del bus: {action} - {content}")

                    # Procesar según la acción
                    if action == "login":
                        handle_login(sock, content)
                    else:
                        logging.warning(f"Acción no soportada: {action}")
        except Exception as e:
            logging.error(f"Error al escuchar el bus: {e}")
            print(f"Error al escuchar el bus: {e}")
            time.sleep(5)


 
def handle_login(sock, content):
    try:
        nombre = content.get("nombre")
        user_password = content.get("user_password")

        # Verificar credenciales en la base de datos
        if User.check_user(nombre, user_password):
            logging.info(f"Inicio de sesión exitoso para: {nombre}")
            send_to_bus_response(sock, "login", {"message": "Inicio exitoso"})
        else:
            logging.warning(f"Inicio de sesión fallido para: {nombre}")
            send_to_bus_response(sock, "login", {"message": "Credenciales incorrectas"})
    except Exception as e:
        logging.error(f"Error al manejar inicio de sesión: {e}")
        send_to_bus_response(sock, "login", {"message": "Error en el servidor"})



class User:
    #interaccion con la bd
    @staticmethod
    def check_user(nombre, user_password):
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            cursor = conn.cursor()

            # Consulta al usuario en la base de datos
            cursor.execute(
                "SELECT id FROM usuarios WHERE nombre = %s AND user_password = %s",
                (nombre, user_password)
            )
            user = cursor.fetchone()
            cursor.close()
            conn.close()

            # Si el usuario existe, retorna True
            return user is not None
        except Exception as e:
            logging.error(f"Error en la base de datos: {e}")
            return False


if __name__ == "__main__":
    logging.info("Iniciando servicio de gestion de usuarios...")
    listen_to_bus()
