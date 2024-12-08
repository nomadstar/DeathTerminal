# Usa una imagen base de ollama/ollama
FROM ollama/ollama:latest
# Instala Python
RUN apt-get update && apt-get install -y python3 python3-pip && apt-get clean && rm -rf /var/lib/apt/lists/*

# Configura el punto de montaje para /root/.ollama
WORKDIR /root/data
# Expone el puerto 11434
EXPOSE 11434

# Comando por defecto para ejecutar cuando se inicie el contenedor
CMD ["python3", "comukey.py"]
