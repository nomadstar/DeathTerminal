import os
import logging
import json
import psycopg2
import socket
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

@dataclass
class Request:
    msg: str
    addr: str = ""
    content: dict = None

    def __post_init__(self):
        self.addr = self.msg[:5]  # Extrae el identificador del servicio
        self.content = json.loads(self.msg[5:])  # Decodifica el JSON restante


@dataclass
class Response: #respuestas del servicio
    addr: str
    content: dict
    msg: str = ""

    def __post_init__(self):
        content_string = json.dumps(self.content)  
        length = len(self.addr + content_string)  
        self.msg = f'{length:05}{self.addr}{content_string}'  


class User:
    #interaccion con la bd
    def check_user(self, nombre, contraseña):
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            cursor = conn.cursor()

            # Consulta al usuario en la base de datos
            cursor.execute(
                "SELECT id FROM usuarios WHERE nombre = %s AND contraseña = %s",
                (nombre, contraseña)
            )
            user = cursor.fetchone()
            cursor.close()
            conn.close()

            # Si el usuario existe, retorna True
            return user is not None
        except Exception as e:
            logging.error(f"Error en la base de datos: {e}")
            return False


class UserService:
    def __init__(self):
        self.sock = None

    def connect_bus(self):
        """
        Conecta el servicio al bus y realiza la inicialización.
        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((BUS_HOST, BUS_PORT))
        init_message = "sinitlogin"
        message = f"{len(init_message):05}{init_message}"
        self.sock.sendall(message.encode())
        logging.info(f"Mensaje enviado al bus: {message}")

        # Leer la respuesta del bus
        response_length = int(self.sock.recv(5).decode())
        response = self.sock.recv(response_length).decode()
        logging.info(f"Respuesta del bus: {response}")
        if "OK" not in response:
            logging.error("Error al conectar con el bus")
            raise Exception("Error al conectar con el bus")
        logging.info("Conexión con el bus establecida correctamente")

    def handle_request(self, req: Request):
        """
        Procesa una solicitud recibida desde el bus.
        """
        action = req.content.get("action")  # Obtener la acción
        if action == "login":
            return self.handle_login(req.content)
        else:
            return Response(addr="login", content={"status": "error", "message": "no soportado"})

    def handle_login(self, data):
        """
        Procesa solicitudes de inicio de sesión.
        """
        try:
            nombre = data.get("nombre")
            contraseña = data.get("contraseña")

            # Validar los campos
            if not nombre or not contraseña:
                logging.warning(f"Solicitud incompleta: {data}")
                return Response(addr="login", content={"status": "error", "message": "Campos incompletos"})

            user = User()
            if user.check_user(nombre, contraseña):
                logging.info(f"Inicio de sesión exitoso para: {nombre}")
                return Response(addr="login", content={"status": "success", "message": "Inicio exitoso"})
            else:
                logging.warning(f"Inicio de sesión fallido para: {nombre}")
                return Response(addr="login", content={"status": "error", "message": "Credenciales erroneas"})
        except Exception as e:
            logging.error(f"Error al procesar solicitud de login: {e}")
            return Response(addr="login", content={"status": "error", "message": "Error interno del servidor"})

    def start(self):
        """
        Inicia el servicio y escucha solicitudes desde el bus.
        """
        self.connect_bus()

        while True:
            try:
                # Recibir mensaje del bus
                data_length = int(self.sock.recv(5).decode())
                data = self.sock.recv(data_length).decode()
                request = Request(msg=data)

                # Procesar solicitud
                response = self.handle_request(request)

                # Enviar respuesta al bus
                self.sock.sendall(response.msg.encode())
                logging.info(f"Respuesta enviada al bus: {response.msg}")
            except Exception as e:
                logging.error(f"Error en el procesamiento de solicitudes: {e}")


if __name__ == "__main__":
    service = UserService()
    service.start()