export DEBIAN_FRONTEND=noninteractive

    apt-get update 
    apt-get install -y --no-install-recommends \
       wget \
       ca-certificates \
       gnupg \
       software-properties-common \
       p7zip-full \
       xvfb \
       curl \
       dotnet-sdk-8.0 \
    # Install Microsoft package feed
    wget -q https://packages.microsoft.com/config/ubuntu/20.04/packages-microsoft-prod.deb -O packages-microsoft-prod.deb \
    dpkg -i packages-microsoft-prod.deb \
    rm packages-microsoft-prod.deb

    # Install .NET
    apt-get update \
    && apt-get install -y --no-install-recommends \
        apt-transport-https \
        dotnet-sdk-5.0 \
        dotnet-sdk-3.1 \
        libpng16-16 \
        libnvtt-dev

    dpkg --add-architecture i386
#    && apt-get install  --no-install-recommends -y gnupg software-properties-common p7zip-full xvfb curl

    wget -qO- https://dl.winehq.org/wine-builds/winehq.key | apt-key add - \
    && apt-add-repository 'deb http://dl.winehq.org/wine-builds/ubuntu/ focal main' \
    && wget -qO- https://download.opensuse.org/repositories/Emulators:/Wine:/Debian/xUbuntu_18.04/Release.key | apt-key add - \
    && sh -c 'echo "deb https://download.opensuse.org/repositories/Emulators:/Wine:/Debian/xUbuntu_18.04/ ./" > /etc/apt/sources.list.d/obs.list'

    apt-get update \
    && apt-get install --install-recommends -y winehq-stable

    wget -qO- https://raw.githubusercontent.com/MonoGame/MonoGame/develop/Tools/MonoGame.Effect.Compiler/mgfxc_wine_setup.sh | xvfb- sh

    rm -rf /var/lib/apt/lists/*

  

    apt-get remove -y xvfb p7zip-full gnupg curl \
    && apt-get autoremove -y \
    && apt-get autoclean -y
    dotnet new install MonoGame.Templates.CSharp