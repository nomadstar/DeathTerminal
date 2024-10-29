FROM gmantaos/monogame:3 AS monogame

CMD apt install wget curl p7zip-full wine64 && \
wget -qO- https://monogame.net/downloads/net8_mgfxc_wine_setup.sh | bash

