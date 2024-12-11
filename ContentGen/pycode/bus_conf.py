import os
import logging
import json
import psycopg2
import socket

# Configuración del BUS
BUS_HOST = os.getenv("BUS_HOST", "localhost")  # Dirección del bus
BUS_PORT = int(os.getenv("BUS_PORT", 5000))    # Puerto del bus por defecto


def recv_exact(sock, n):
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            raise Exception("Conexión cerrada mientras se leía el socket")
        data += packet
    return data

#recibir mensaje del bus
def receive_from_bus(sock):
    """
    Recibe un mensaje del bus de servicios utilizando un socket.
    :param sock: Socket conectado al bus.
    :return: Diccionario con la acción y el contenido del mensaje.
    estructura: formato 1: xxxxxaaaaa{content}
                formato 2: xxxxxaaaaaff{datos} -> nk o ok
    """
    try:
        # Leer los primeros 5 caracteres como longitud del mensaje
        length_bytes = recv_exact(sock, 5)
        if not length_bytes:
            ptint("no hay datos aun")
            return None
        response_length = int(length_bytes.decode())
        
        # Leer el resto del mensaje
        response_bytes = recv_exact(sock, response_length)
        response = response_bytes.decode()
        
        # Extraer prefijo del servicio
        action = response[:5]
        status_or_content = response[5:]
        
        # Determinar el formato basado en el status
        if status_or_content[:2] in ('OK', 'NK'):
            status = status_or_content[:2]
            content_json = status_or_content[2:]
            content = json.loads(content_json)
            print(f"Mensaje recibido: {response_length:05}{action} {status} {content}")
            logging.info(f"Mensaje recibido: {response_length:05}{action} {status} {content}")
            return {"action": action, "status": status, "content": content}
        else:
            content = json.loads(status_or_content)
            print(f"Mensaje recibido: {response_length:05}{action} {content}")
            logging.info(f"Mensaje recibido: {response_length:05}{action} {content}")
            return {"action": action, "content": content}
    except Exception as e:
        logging.error(f"Error al recibir mensaje del bus: {e}")
        print(f"Error al recibir mensaje del bus: {e}")
        return None

def register_service(prefix):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((BUS_HOST, BUS_PORT))
        logging.info(f"Conectado al bus")

        # registrar el servicio
        prefix = prefix[:5]
        registration_message = f"{len('sinit' + prefix):05}sinit{prefix}"
        print(f"Mensaje registro: {registration_message}")
        sock.sendall(registration_message.encode())
        logging.info(f"Mensaje de registro: {registration_message}")

        response_length = int(sock.recv(5).decode())
        response = sock.recv(response_length).decode()
        logging.info(f"Respuesta ceribida: {response}")
        print(f"Mensaje recibido: {response}")

        if "OK" not in response:
            logging.error(f"Servicio rechazado por el bus: {response}")
            sock.close()
            raise Exception(f"Servicio rechazado por el bus: {response}")

        logging.info(f"Servicio registrado con prefijo: {prefix}")
        return sock  # Devolver el socket para uso futuro
    except Exception as e:
        logging.error(f"Error al registrar servicio: {e}")
        raise
#enviar mensajes al bus
def send_to_bus_response(sock,action,content):
    """
    Envía una respuesta al bus desde el servidor.
    :param sock: Socket conectado al bus.
    :param action: servicio a quien se envia la respuesta.
    :param content: Diccionario con el contenido de la respuesta.
    estructura: xxxxxaction{content}
    """
    try:
        # Serializar el contenido y calcular la longitud
        message_content = json.dumps(content)
        prefix = f"{action[:5]}"
        full_message = f"{len(prefix + message_content):05}{prefix}{message_content}"

        # Enviar al bus
        print (f"mensaje enviado: {full_message}")
        sock.sendall(full_message.encode())
        logging.info(f"mensaje enviado: {full_message}")
    except Exception as e:
        logging.error(f"Error al enviar respuesta al bus: {e}")