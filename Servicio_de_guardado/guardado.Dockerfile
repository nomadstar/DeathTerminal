FROM python:3

WORKDIR /usr/src/app

# Copiar los archivos necesarios
COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt
ENV PYTHONPATH=/app

COPY . .

CMD [ "python", "guardado.py" ] 
