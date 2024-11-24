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
    filename=os.path.join(LOG_DIR, "registro_usuarios.log"),
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
    "password": os.getenv("POSTGRES_password", "password"),
    "host": "db",
    "port": 5432
}

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

        action = data[:5].strip()  # Prefijo de 8 caracteres, registro
        content = json.loads(data[5:])  # JSON del contenido

        logging.info(f"Mensaje recibido del bus: {data}")
        print(f"Mensaje recibido del bus: {data}")

        return {"action": action, "content": content}
    except Exception as e:
        logging.error(f"Error al recibir mensaje del bus: {e}")
        print(f"Error al recibir mensaje del bus: {e}")
        return None
#registrar el servicio con el bus
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
def send_to_bus_response(sock, action ,content):
    """
    Envía una respuesta al bus desde el servidor.
    :param sock: Socket conectado al bus.
    :param action: Acción/prefijo de la respuesta
    :param content: Diccionario con el contenido de la respuesta.
    status : ok o nk
    """
    try:
        # Serializar el contenido y calcular la longitud
        message_content = json.dumps(content)
        prefix = action[:5]
        full_message = f"{len(prefix + message_content):05}{prefix}{message_content}"

        # Enviar al bus
        sock.sendall(full_message.encode())
        logging.info(f"Respuesta enviada al bus: {full_message}")
    except Exception as e:
        logging.error(f"Error al enviar respuesta al bus: {e}")


#escucha activa del bus y su proceso
def listen_to_bus():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            # Conectar al bus
            sock.connect((BUS_HOST, BUS_PORT))
            logging.info("Conectado al bus de servicios")

            #registrar el servicio
            register_service(sock, "regis")

            while True:
                # Recibir mensaje del bus
                message = receive_from_bus(sock)
                if message:
                    action = message["action"]
                    content = message["content"]

                    # Procesar según la acción
                    if action == "regis":
                        handle_registro(sock, content)
                    else:
                        logging.warning(f"Comunicacion con otro servicio: {action}")
        except Exception as e:
            logging.error(f"Error al escuchar el bus: {e}")
            print(f"Error al escuchar el bus: {e}")
            time.sleep(5)

#funcion propia del servicio
def handle_registro(sock, content):
    """
    Maneja la acción de registro de usuario.
    :param sock: Socket conectado al bus.
    :param content: Contenido del mensaje recibido (diccionario).
    """
    try:
        nombre = content.get("nombre")
        email = content.get("email")
        user_password = content.get("user_password")


        # Verificar si el usuario ya existe
        if User.check_user(nombre)==True:
            logging.info(f"Usuario ya registrado: {nombre}")
            send_to_bus_response(sock, "regis",{"status": "error", "message": "El usuario ya está registrado"})
            return

        # Registrar el usuario
        if User.register_user(nombre, email, user_password):
            logging.info(f"Usuario registrado exitosamente: {nombre}")
            send_to_bus_response(sock, "regis", {"status": "success", "message": "Registro exitoso"})
        else:
            logging.error(f"Error al registrar usuario: {nombre}")
            send_to_bus_response(sock, "regis",{"status": "error", "message": "Error al registrar usuario"})
    except Exception as e:
        logging.error(f"Error en el manejo de registro: {e}")
        send_to_bus_response(sock, "regis",{"status": "error", "message": "Error interno del servidor"})



class User:
    @staticmethod
    def check_user(nombre):
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            cursor = conn.cursor()

            # Consulta al usuario en la base de datos por el nombre
            cursor.execute("SELECT id FROM usuarios WHERE nombre = %s", (nombre,))
            user = cursor.fetchone()
            cursor.close()
            conn.close()

            # Si el usuario existe, retorna True
            return user is not None
        except Exception as e:
            logging.error(f"Error en la base de datos al verificar usuario: {e}")
            return False

    @staticmethod
    def register_user(nombre, email, user_password):
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            cursor = conn.cursor()
            tipo_usuario = "usuario"

            # Insertar el nuevo usuario y obtener el ID generado
            cursor.execute(
                """
                INSERT INTO usuarios (nombre, email, user_password, Tipo_usuario)
                VALUES (%s, %s, %s, %s) RETURNING id
                """,
                (nombre, email, user_password, tipo_usuario)
            )
            user_id = cursor.fetchone()[0]
            conn.commit()
            cursor.close()
            conn.close()
            return {"status": "success", "id": user_id}
        except psycopg2.errors.UniqueViolation:
            logging.error(f"Error: El nombre ya está registrado")
            return {"status": "error", "message": "El nombre ya está registrado"}
        except Exception as e:
            logging.error(f"Error en la base de datos al registrar usuario: {e}")
            return {"status": "error", "message": "Error interno en el servidor"}


if __name__ == "__main__":
    logging.info("Iniciando servicio de registro de usuarios...")
    listen_to_bus()
