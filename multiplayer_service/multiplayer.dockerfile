FROM python:3

WORKDIR /usr/src/app

COPY pluginlist.txt .
RUN pip install --no-cache-dir -r pluginlist.txt
ENV PYTHONPATH=/app
COPY . .

CMD [ "python", "multiplayer.py" ] 
# Remplaza example.py por el archivo que tu quieras ;D