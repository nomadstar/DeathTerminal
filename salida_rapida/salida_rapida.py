import requests

def salida_rapida(usuario_id, nivel_id):
    try:
        # Paso 1: Llamar al Servicio de Guardado
        print(f"Guardando progreso del usuario {usuario_id} en el nivel {nivel_id}...")
        url_guardado = "http://localhost:5002/guardar_progreso"  # URL del servicio de guardado
        data = {
            "usuario_id": usuario_id,
            "nivel_id": nivel_id
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
    nivel_id = int(input("Ingrese el ID del nivel: "))
    resultado = salida_rapida(usuario_id, nivel_id)
    print(resultado)
