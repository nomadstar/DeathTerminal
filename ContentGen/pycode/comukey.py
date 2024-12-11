import os
import logging
import json
import socket
import ollama
from bus_conf import send_to_bus_response,register_service, receive_from_bus
import subprocess

ollamainstalled = False

def makequestion(nivel,tema):
    try:
        question_data = [{
            "nivel (difficultad)": int(nivel),
            "tema (tematica de pregunta)": tema,
            "Parametros esperados:": {"Pregunta": "Texto de la pregunta", "Respuesta Correcta": " Texto correcta"}
        }]

        for part in ollama.chat(model='llama3', messages=[question_data], stream=True):
            print(part['message']['content'], end='', flush=True)

    except Exception as e:
        logging.error(f"Error al generar pregunta: {e}")
        return None


def main():

    print(makequestion(1,"Matematicas"))

if __name__ == "__main__":
    main()