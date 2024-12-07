import logging
from bus_conf import send_to_bus_response,register_service, receive_from_bus

def jugar(sock):
    print("=== Jugar ===")
    print("Falta implementar")

def informacion_usuario(sock, id):
    send_to_bus_response(sock, "infou", {"id": id})
    res= receive_from_bus(sock)
    print(f"Respuesta recibida: {res}")



def registro(sock):
    print("=== Registro de usuario ===")
    nombre = input("Ingrese su nombre: ").strip()
    email = input("Ingrese su correo: ").strip()
    user_password = input("Ingrese su contraseña: ").strip()
    
 
    send_to_bus(sock, "login", {"nombre": nombre, "email": email, "user_password": user_password})

    # Esperar respuesta
    message = receive_from_bus(sock)
    print(f"Respuesta recibida: {message}")

def login(sock):
    print("=== Iniciar sesión ===")
    nombre = input("Ingrese su nombre: ").strip()
    user_password = input("Ingrese su contraseña: ").strip()
    
    # Crear el mensaje para el servicio de login
    send_to_bus_response(sock, "login", {"nombre": nombre, "user_password": user_password})

    # Esperar respuesta
    respuesta = receive_from_bus(sock)
    contenido = respuesta.get("content", {})
    id= contenido.get("id")
    action = respuesta.get("action")
    if "status" in respuesta  and action != "clien":
        print("inicio de sesion exitoso")
        while True:
            print("1. Continuar jugando (falta)")
            print("2. Ver mi información")
            print("3. Cerrar sesión")
            opcion = input("Seleccione una opción: ").strip()
            if opcion == "1":
                print("Continuar jugando")
                jugar(sock)
            elif opcion == "2":
                print("Ver mi información")
                informacion_usuario(sock, id)
                print("Cerrando sesión...")
                break
            else:
                print("Opción inválida")
    else:
        print(f"Error en el inicio de sesión: {respuesta.get('error', 'Error desconocido')}")

def handle_response(sock, message):
    # Aquí procesarás respuestas genéricas recibidas desde otros servicios
    print(f"Respuesta recibida: {message}")

if __name__ == "__main__":
    print("--- Cliente para SOA ---")
    sock = register_service("clien") 
    
    try:
        while True:
            print("1. Registrarse")
            print("2. Iniciar sesión")
            print("3. Salir")
            opcion = input("Seleccione una opción: ").strip()
            
            if opcion == "1":
                registro(sock)
            elif opcion == "2":
                login(sock)
            elif opcion == "3":
                print("Saliendo del cliente...")
                break
            else:
                print("Opción inválida")
    except Exception as e:
        logging.error(f"Error: {e}")
    finally:
        sock.close()
