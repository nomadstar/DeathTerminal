# Usa una imagen base de ollama/ollama
FROM ollama/ollama

# Configura el punto de montaje para /root/.ollama
WORKDIR /root/data

# Expone el puerto 11434
EXPOSE 11434

RUN apt-get update && apt-get install -y \
    # Instala paquetes necesarios
    gcc \
    g++ \
    make \
    cmake \
    libstdc++-dev \
    libboost-all-dev \
    nlohmann-json3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
    


# Comando por defecto para ejecutar cuando se inicie el contenedor
CMD ["ok_api.exe"]
