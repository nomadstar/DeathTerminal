import requests

def obtener_nivel_actual(usuario_id):
    """
    Consulta el nivel actual del usuario desde el servicio de progreso.
    """
    try:
        url_nivel_actual = "http://localhost:5003/nivel_actual"  # URL del servicio de progreso
        response = requests.post(url_nivel_actual, json={"usuario_id": usuario_id})
        
        if response.status_code == 200:
            nivel_actual = response.json().get("nivel_actual")
            print(f"Nivel actual recuperado: {nivel_actual}")
            return nivel_actual
        else:
            print(f"Error al obtener el nivel actual: {response.json().get('message')}")
            return None
    except Exception as e:
        print(f"Error al comunicarse con el servicio de progreso: {e}")
        return None

def salida_rapida(usuario_id):
    """
    Guarda automáticamente el nivel actual del usuario en la tabla progresion.
    """
    try:
        # Paso 1: Obtener el nivel actual del usuario
        nivel_actual = obtener_nivel_actual(usuario_id)
        if not nivel_actual:
            return {
                "status": "error",
                "message": "No se pudo obtener el nivel actual. No se guardó el progreso."
            }

        # Paso 2: Llamar al Servicio de Guardado
        print(f"Guardando progreso del usuario {usuario_id} en el nivel {nivel_actual}...")
        url_guardado = "http://localhost:5002/guardar_progreso"  # URL del servicio de guardado
        data = {
            "usuario_id": usuario_id,
            "nivel_id": nivel_actual
        }
        response = requests.post(url_guardado, json=data)
        
        # Validar la respuesta del Servicio de Guardado
        if response.status_code == 200:
            print("Progreso guardado exitosamente.")
            return {
                "status": "success",
                "message": "Progreso guardado exitosamente. Puedes salir del juego."
            }
        else:
            print(f"Error al guardar el progreso: {response.json().get('error')}")
            return {
                "status": "error",
                "message": f"Error al guardar el progreso: {response.json().get('error')}"
            }

    except Exception as e:
        print(f"Error en el servicio de salida rápida: {e}")
        return {
            "status": "error",
            "message": f"Error en el servicio de salida rápida: {e}"
        }

if __name__ == "__main__":
    usuario_id = int(input("Ingrese el ID del usuario: "))
    resultado = salida_rapida(usuario_id)
    print(resultado)
