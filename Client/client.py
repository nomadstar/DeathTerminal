import socket
import json
import os

#servicio de prueba para ver si funciona el inicio de seción


BUS_HOST = os.getenv("BUS_HOST", "localhost")  # Dirección del bus
BUS_PORT = int(os.getenv("BUS_PORT", 5000))   # Puerto del bus por defecto


def send_request(action, nombre, contraseña):
    
    # Crear el mensaje en formato JSON
    request_data = {
        "action":action,
        "nombre":nombre,
        "contraseña":contraseña
    }
    message_content = json.dumps(request_data)
    full_message = f"{len(message_content) + 5:05}login{message_content}"

    # Conectar al bus y enviar la solicitud
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((BUS_HOST, BUS_PORT))
            print(f"Enviando: {full_message}")
            sock.sendall(full_message.encode())

            # Leer la respuesta del bus
            response_length = int(sock.recv(5).decode())
            response = sock.recv(response_length).decode()
            print(f"Respuesta del bus: {response}")
    except Exception as e:
        print(f"Error al enviar solicitud al bus: {e}")

if __name__ == "__main__":
    print("--- Cliente para Login SOA ---")
    nombre = input("Introduce tu nombre de usuario: ")
    contraseña = input("Introduce tu contraseña: ")

    send_request("login", nombre, contraseña)
