import logging
from bus_conf import send_to_bus_response,register_service, receive_from_bus

def completar_nivel(sock, usuario_id, nivel):
    while True:
        print("1. completar nivel")
        print("2. reiniciar nivel")
        print("3. salir")
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            send_to_bus_response(sock, "progr", {"id": usuario_id, "opcion": 2, "nivel": nivel})
        elif opcion == "2":
            send_to_bus_response(sock, "reini", {"id": usuario_id, "nivel": nivel})
        elif opcion == "3":
            break
        else:
            print("Opción inválida")
        respuesta = receive_from_bus(sock)
        contenido = respuesta.get("content", {})
        mensaje = contenido.get("message", None)
        print(f"Respuesta recibida: {mensaje}")

def jugar(sock,id):
    print("=== Jugar ===")
    #de acuerdo al nivel en que me encuentre voy a poder jugar
    # en_proceso -> nivel actual
    # completado -> nivel actual + 1
    #logica del juego (por implementar)
    nivel_actual = obtener_nivel_actual(sock, id)
    while True:
        print("1. Jugar solitiario")
        print("2. Jugar multijugador")
        print("3. Salir")
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            print("Jugando...")
            print("Nivel actual: ", nivel_actual)
            completar_nivel(sock, id, nivel_actual)
            # Aquí va la lógica del juego
            # Por ahora solo se muestra un mensaje

        elif opcion == "2":
            print("Jugando multijugador...")
            print("Nivel actual: ", nivel_actual)
            # encontrar un usuario el cual tenga el mismo nivel actual
            send_to_bus_response(sock, "busca", {"id": id, "nivel": nivel_actual})
            res = receive_from_bus(sock)
            contenido = res.get("content", {})
            usuario_encontrado = contenido.get("usuario_encontrado", None)
            id_encontrado = contenido.get("id_encontrado", None)
            if usuario_encontrado:
                print(f"Usuario encontrado: {usuario_encontrado}")
                # logica del juego
                #suponiendo que ya se paso de nivel
                send_to_bus_response(sock, "multi", {"id_usuario": id, "id_encontrado": id_encontrado, "id_nivel": nivel_actual})
                print("Logica para jugar")
            else:
                print("No se encontró un usuario con el mismo nivel actual")

        elif opcion == "3":
            print("Saliendo del juego...")
            salida_rapida(sock, id)
            break
        else:
            print("Opción inválida")
    

def informacion_usuario(sock, id):
    send_to_bus_response(sock, "infou", {"id": id})
    res= receive_from_bus(sock)
    contenido = res.get("content", {})
    data = contenido.get("data", None)
    print(f"Respuesta recibida: {data}")
    print(f"Respuesta recibida: {res}")

#modificacion de cristoher para obtener el nivel actual
def obtener_nivel_actual(sock, usuario_id):
    """
    Consulta el último nivel completado del usuario (nivel actual).
    """
    send_to_bus_response(sock, "progr", {"id": usuario_id, "opcion": 1})
    res = receive_from_bus(sock)
    contenido = res.get("content", {})
    nivel_actual = contenido.get("nivel_actual", None)
    nivel_id = contenido.get("id_nivel", None)
    if nivel_actual:
        print(f"Nivel actual recuperado: {nivel_actual}")
    else:
        print("El usuario no ha jugado en un nivel.")
    return nivel_id

def sistema_foro(sock, id):
    #ver todas las publicaciones, publicar una publicación
    while True:
        print("=== Sistema de foro ===")
        print("1. Ver mis publicaciones")
        print("2. Realizar una publicación")
        print("3. Ver todas las publicaciones")
        print("4. Salir")
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            send_to_bus_response(sock, "foros", {"opcion":1, "id": id})
        elif opcion == "2":
            tema = input("Ingrese el tema: (máx 10 carácteres) ").strip()[:10]
            mensaje = input("Ingrese el mensaje de la publicación: ").strip()
            send_to_bus_response(sock, "foros", {"opcion":2, "id": id, "tema": tema, "mensaje": mensaje})
        elif opcion == "3":
            send_to_bus_response(sock, "foros", {"opcion":3})
        else:
            print("Saliendo del sistema de foro...")
            break
        respuesta = receive_from_bus(sock)
        contenido = respuesta.get("content", {})
        mensaje = contenido.get("message", None)
        print(f"Respuesta recibida: {mensaje}")

def registro(sock):
    print("=== Registro de usuario ===")
    nombre = input("Ingrese su nombre: ").strip()
    email = input("Ingrese su correo: ").strip()
    user_password = input("Ingrese su contraseña: ").strip()
    
 
    send_to_bus_response(sock, "regis", {"nombre": nombre, "email": email, "user_password": user_password})

    # Esperar respuesta
    message = receive_from_bus(sock)
    print(f"Respuesta recibida: {message}")

def salida_rapida(sock, usuario_id):
    """
    Llama al servicio de salida rápida para guardar el nivel actual del usuario.
    """
    print("=== Salida rápida ===")
    send_to_bus_response(sock, "salir", {"id": usuario_id})
    res = receive_from_bus(sock)
    contenido = res.get("content", {})
    mensaje = contenido.get("message", None)
    print(f"Respuesta recibida: {mensaje}")

def login(sock):
    print("=== Iniciar sesión ===")
    nombre = input("Ingrese su nombre: ").strip()
    user_password = input("Ingrese su contraseña: ").strip()
    
    # Crear el mensaje para el servicio de login
    send_to_bus_response(sock, "login", {"nombre": nombre, "user_password": user_password})

    # Esperar respuesta
    respuesta = receive_from_bus(sock)
    contenido = respuesta.get("content", {})
    id = contenido.get("id")
    message = contenido.get("message")
    if "credenciales correctas" in message:
        print("Inicio de sesión exitoso")
        while True:
            print("1. Continuar jugando (falta)")
            print("2. Ver mi información")
            print("3. Ver el sistema de foro")
            print("4. Cerrar sesión")
            opcion = input("Seleccione una opción: ").strip()
            if opcion == "1":
                print("Continuar jugando")
                jugar(sock,id)
            elif opcion == "2":
                print("Ver mi información")
                informacion_usuario(sock, id)
            elif opcion == "3":
                print("Ver el sistema de foro")
                sistema_foro(sock, id)
            elif opcion == "4":
                print("Cerrando sesión...")
                salida_rapida(sock, id)
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
