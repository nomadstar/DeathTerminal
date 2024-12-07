FROM python:3

WORKDIR /usr/src/app

# Copiar los archivos necesarios
COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Cambiar CMD para evitar que se inicie automáticamente
CMD ["tail", "-f", "/dev/null"]
