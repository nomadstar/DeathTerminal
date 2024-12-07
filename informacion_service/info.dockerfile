FROM python:3

WORKDIR /usr/src/app

RUN pip install --upgrade pip  # Actualizar pip
COPY pluginlist.txt .
RUN pip install --no-cache-dir -r pluginlist.txt
ENV PYTHONPATH=/app
COPY . .

CMD [ "python", "usuario.py" ]
