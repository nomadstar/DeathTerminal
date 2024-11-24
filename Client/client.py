import socket
import json
import os

# Configuración del BUS
BUS_HOST = os.getenv("BUS_HOST", "localhost")  # Dirección del bus
BUS_PORT = int(os.getenv("BUS_PORT", 5000))    # Puerto del bus por defecto

def send_request(action, nombre, user_password, email=None):
    request_data = {
        "action": action,
        "nombre": nombre,
        "user_password": user_password
    }

    if action == "registro":
        if not email:
            print("El email es obligatorio para el registro.")
            return
        request_data["email"] = email
        prefix = "regis" 
    elif action == "login":
        prefix = "login"  
    else:
        print("Acción no soportada")
        return

    # Crear el mensaje a enviar
    message_content = json.dumps(request_data)
    full_message = f"{len(prefix + message_content):05}{prefix}{message_content}"
    print(f"Mensaje a enviar: {full_message}")

    try:
        # Conectar al bus y enviar el mensaje
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((BUS_HOST, BUS_PORT))
            sock.sendall(full_message.encode())

            # Recibir la respuesta del bus
            response = receive_response(sock)
            if response:
                handle_response(response)
    except Exception as e:
        print(f"Error al enviar solicitud al bus: {e}")

def receive_response(sock):
    try:
        response_length = int(sock.recv(5).decode())
        response = sock.recv(response_length).decode()
        print(f"Respuesta completa del bus: {response}")

        # Extraer prefijo y contenido
        prefix = response[5:7].strip()  # Prefijo como "OK" o "NK"
        content = json.loads(response[7:])  # El contenido como JSON

        return {"prefix": prefix, "content": content}
    except Exception as e:
        print(f"Error al recibir respuesta del bus/formato invalido: {e}")
        return None

def handle_response(response):
    """
    Procesa la respuesta del bus.
    :param response: Diccionario con el prefijo y el contenido de la respuesta.
    """
    prefix = response["prefix"]
    content = response["content"]

    if prefix == "OK":
        print(f"Éxito: {content.get('message', 'Operación completada')}")
    elif prefix == "NK":
        print(f"Error: {content.get('message', 'Operación fallida')}")
    else:
        print(f"Respuesta inesperada del bus: {response}")

def registro():
    """
    Solicita los datos necesarios para registrar un usuario y envía la solicitud.
    """
    nombre = input("Introduce tu nombre de usuario: ").strip()
    user_password = input("Introduce tu contraseña: ").strip()
    email = input("Introduce tu email: ").strip()

    send_request("registro", nombre, user_password, email)

def login():
    """
    Solicita los datos necesarios para iniciar sesión y envía la solicitud.
    """
    nombre = input("Introduce tu nombre de usuario: ").strip()
    user_password = input("Introduce tu contraseña: ").strip()

    send_request("login", nombre, user_password)

if __name__ == "__main__":
    print("--- Cliente para Login SOA ---")
    while True:
        print("1. Registrarse")
        print("2. Iniciar sesión")
        print("3. Salir")
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            registro()
        elif opcion == "2":
            login()
        elif opcion == "3":
            print("Saliendo del cliente.")
            break
        else:
            print("Opción inválida")
