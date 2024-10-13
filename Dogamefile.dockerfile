FROM debian:buster

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    python3-setuptools \
    python3-wheel \
    python3-venv \
    vim \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*

RUN wget https://github.com/godotengine/godot/archive/3.2.3-stable.zip
RUN unzip 3.2.3-stable.zip