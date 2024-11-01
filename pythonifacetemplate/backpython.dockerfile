FROM python:3

WORKDIR /usr/src/app

COPY pluginlist.txt .
COPY ./workfiles/ ./usr/src/app
RUN pip install --no-cache-dir -r pluginlist.txt

COPY . .

CMD [ "python", "example.py" ] 
# Remplaza example.py por el archivo que tu quieras ;D