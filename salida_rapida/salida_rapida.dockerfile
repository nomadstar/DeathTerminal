FROM python:3.9

WORKDIR /app
RUN pip install --upgrade pip 
COPY . .

RUN pip install --no-cache-dir -r requeriments.txt
ENV PYTHONPATH=/app

CMD ["python", "salida_rapida.py"]
