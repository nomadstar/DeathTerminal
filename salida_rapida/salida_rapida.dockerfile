# Usar la imagen base de Python 3
FROM python:3

# Establecer el directorio de trabajo
WORKDIR /usr/src/app

# Copiar el archivo de requerimientos y las dependencias
COPY requirements.txt . 

# Instalar las dependencias necesarias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código al contenedor
COPY . .

# Comando para ejecutar el script de salida rápida
CMD ["python", "salida_rapida.py"]
