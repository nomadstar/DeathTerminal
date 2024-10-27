FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
COPY example.py ./usr/src/app

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./example.py" ]