# Usa una imagen base de ollama/ollama
FROM ollama/ollama:latest
# Instala Python
RUN apt-get update && apt-get install -y python3 python3-pip && apt-get clean && rm -rf /var/lib/apt/lists/*
RUN pip3 install ollama
RUN pip3 install psycopg2-binary

# Establece el directorio de trabajo
WORKDIR /root/.ollama
COPY pycode/* .

# Descarga el modelo llama3 usando ollama
RUN python3 comukey.py


# Comando por defecto para ejecutar cuando se inicie el contenedor
