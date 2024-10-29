FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt .
COPY ./workfiles/ ./usr/src/app
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "example.py" ] 
# Remplaza example.py por el archivo que tu quieras ;D