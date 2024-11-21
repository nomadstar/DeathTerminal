FROM ubuntu:20.04 AS gamemono

# Configuración básica e instalación de dependencias iniciales
RUN export DEBIAN_FRONTEND=noninteractive \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
       wget \
       ca-certificates \
       gnupg \
       software-properties-common \
       p7zip-full \
       xvfb \
       curl

# Agregar el repositorio de Microsoft y .NET SDK
RUN wget -q https://packages.microsoft.com/config/ubuntu/20.04/packages-microsoft-prod.deb -O packages-microsoft-prod.deb \
    && dpkg -i packages-microsoft-prod.deb \
    && rm packages-microsoft-prod.deb \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
       apt-transport-https \
       dotnet-sdk-9.0 \
       libpng16-16 \
       libnvtt-dev

# Agregar arquitectura de 32 bits para Wine
RUN dpkg --add-architecture i386

# Configurar repositorio de WineHQ
RUN mkdir -p /etc/apt/keyrings \
    && wget -qO /etc/apt/keyrings/winehq-archive.key https://dl.winehq.org/wine-builds/winehq.key \
    && echo "deb [signed-by=/etc/apt/keyrings/winehq-archive.key] https://dl.winehq.org/wine-builds/ubuntu/ focal main" > /etc/apt/sources.list.d/winehq.list \
    && apt-get update \
    && apt-get install -y --install-recommends winehq-stable

# Instalar Wine32 y Wine64 para mejorar la compatibilidad
RUN apt-get install -y --install-recommends \
    wine32 \
    wine64 \
    winbind

# Inicializar Wine
RUN wineboot --init && sleep 10

# Configurar RpcSs en Wine sin preguntar por confirmación
RUN wine reg add "HKLM\\System\\CurrentControlSet\\Services\\RpcSs" /v Start /t REG_DWORD /d 2 /f

# Descargar el script de instalación de MonoGame y ejecutarlo con xvfb
ADD https://raw.githubusercontent.com/MonoGame/MonoGame/develop/Tools/MonoGame.Effect.Compiler/mgfxc_wine_setup.sh /tmp/mgfxc_wine_setup.sh

# Configurar y ejecutar xvfb correctamente para que Wine pueda usarlo
RUN chmod +x /tmp/mgfxc_wine_setup.sh \
    && xvfb-run --server-args="-screen 0 1024x768x24" sh /tmp/mgfxc_wine_setup.sh

# Limpiar cache y eliminar dependencias no necesarias
RUN apt-get remove -y xvfb p7zip-full gnupg curl \
    && apt-get autoremove -y \
    && apt-get autoclean -y \
    && rm -rf /var/lib/apt/lists/* /tmp/mgfxc_wine_setup.sh

# Definir variables de entorno
ENV MGFXC_WINE_PATH=/root/.winemonogame/

WORKDIR /usr/src/app
RUN dotnet new install MonoGame.Templates.CSharp

