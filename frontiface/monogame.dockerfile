FROM gmantaos/monogame AS monogame
#Setup Version
ARG MONOGAME_VERSION=3.8.0.1641
WORKDIR /game
COPY ./gamefiles ./game
RUN if [ "$(ls -A /game)" ]; then dotnet new mgdesktool; fi