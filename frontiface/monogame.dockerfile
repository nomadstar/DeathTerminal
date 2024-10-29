FROM ubuntu AS gamemono
COPY runme.sh .
RUN sh runme.sh
ENV MGFXC_WINE_PATH=/root/.winemonogame/
WORKDIR /usr/src/app
ARG workdir
COPY ${workdir} /usr/src/app
RUN if [ -z "$(ls .)" ] then dotnet new mgdesktopgl . ; else echo "command not runned" ; fi;