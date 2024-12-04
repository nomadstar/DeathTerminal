FROM python:3

WORKDIR /usr/src/app

COPY pluginlist.txt .
RUN pip install --no-cache-dir -r pluginlist.txt
COPY . .
ENV PYTHONPATH=/app
CMD [ "python", "register.py" ] 
