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
    git \
    build-essential \
    scons \
    pkg-config \
    libx11-dev \
    libxcursor-dev \
    libxinerama-dev \
    libgl1-mesa-dev \
    libglu-dev \
    libasound2-dev \
    libpulse-dev \
    libudev-dev \
    libxi-dev \
    libxrandr-dev \
    yasm \
    mingw-w64 \
    && rm -rf /var/lib/apt/lists/*

RUN wget https://github.com/godotengine/godot/archive/3.2.3-stable.zip
RUN unzip 3.2.3-stable.zip
WORKDIR "/godot-3.2.3-stable/modules"
# A modo de testeo se instalara godot_voxel 
RUN git clone https://github.com/Zylann/godot_voxel.git
RUN mv godot_voxel voxel

# Remove the encoding argument from voxel_version.py (Thank you Copilot)
RUN sed -i 's/open(head_path, "r", encoding="utf8")/open(head_path, "r")/' /godot-3.2.3-stable/modules/voxel/voxel_version.py


WORKDIR "/godot-3.2.3-stable"
RUN echo 1 | update-alternatives --config x86_64-w64-mingw32-gcc
RUN echo 1 | update-alternatives --config x86_64-w64-mingw32-g++
# IMPORTANTE: Se debe cambiar el comando de scons para que se compile en windows.
# Cada maquina es distinta, por ende los parametros pueden variar. Ojo con eso.
RUN scons -j6 platform=windows tools=yes target=release_debug bits=64