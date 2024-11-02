FROM ubuntu AS gamemono
COPY runme.sh .
RUN sh runme.sh
ENV MGFXC_WINE_PATH=/root/.winemonogame/
WORKDIR /usr/src/app
ARG workdir
COPY ${workdir} /usr/src/app
RUN dotnet new install MonoGame.Templates.CSharp
RUN if [ -z "$(ls .)" ]; then dotnet new mgdesktopgl -o DeathTerminal ; else echo "command not runned" ; fi;