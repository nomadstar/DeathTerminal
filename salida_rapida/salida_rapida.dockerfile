FROM python:3.9

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requeriments.txt

CMD ["python", "salida_rapida.py"]
