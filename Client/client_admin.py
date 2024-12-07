import logging
from bus_conf import send_to_bus_response,register_service, receive_from_bus

def informacion_admin(sock):
    while True:
        print("1. Ver información de los usuarios")
        print("2. Eliminar usuario, segun id")
        print("3. Ver los niveles")
        print("4. Modificar niveles")
        print("5. Eliminar niveles")
        print("6. Salir")
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            send_to_bus_response(sock,"iadmi",{"opcion":opcion}) 
        elif opcion == "2":
            id_eliminar = input("Ingrese el ID del usuario a eliminar: ").strip()
            send_to_bus_response(sock, "iadmi", {"opcion":opcion, "id": id_eliminar})
        elif opcion == "3":
            send_to_bus_response(sock,"iadmi",{"opcion":opcion})
        elif opcion == "4":
            id_modificar = input("Ingrese el ID del nivel a modificar: ").strip()
            nivel = input("Ingrese el nuevo nivel: ").strip()
            dificultad = input("Ingrese la nueva dificultad: ").strip()
            send_to_bus_response(sock, "iadmi", {"opcion":opcion, "id": id_modificar, "nivel": nivel, "dificultad": dificultad})
        elif opcion == "5":
            id_eliminar = input("Ingrese el ID del nivel a eliminar: ").strip()
            send_to_bus_response(sock, "iadmi", {"opcion":opcion, "id": id_eliminar})
        elif opcion == "6":
            break
        else:
            print("Opción inválida")
        respuesta = receive_from_bus(sock)
        print(f"Respuesta recibida: {respuesta}")
        print("enter para continuar")

def admin(sock):
    print("=== Iniciar sesión ===")
    nombre = input("Ingrese su nombre: ").strip()
    user_password = input("Ingrese su contraseña: ").strip()
    
    send_to_bus_response(sock, "login", {"nombre": nombre, "user_password": user_password})

   
    respuesta = receive_from_bus(sock)
    contenido = respuesta.get("content", {})
    id= contenido.get("id")
    action = respuesta.get("action")
    if "status" in respuesta  and action != "clien":
        print("inicio de sesion exitoso")
        send_to_bus_response(sock, "permi", {"id":id})
        res= receive_from_bus(sock)
        cont = res.get("content", {})
        msg= cont.get("message")
        
        if msg == True: #es administrador
            informacion_admin(sock)
        else:
            print("No tiene permisos de administrador")
    else:
        print(f"Error en el inicio de sesión: {respuesta.get('error', 'Error desconocido')}")

def handle_response(sock, message):
    # Aquí procesarás respuestas genéricas recibidas desde otros servicios
    print(f"Respuesta recibida: {message}")

if __name__ == "__main__":
    print("--- Cliente administrador para SOA ---")
    sock = register_service("admin") 
    admin(sock)
