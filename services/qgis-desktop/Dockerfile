# Base image with Xpra support
FROM ubuntu:22.04

# Avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    software-properties-common \
    xpra \
    python3-pip \
    curl \
    jq \
    dbus \
    dbus-x11 \
    xterm \
    xauth \
    python3-xdg \
    supervisor

# Add QGIS repository
RUN wget -O - https://qgis.org/downloads/qgis-2022.gpg.key | gpg --dearmor > /etc/apt/trusted.gpg.d/qgis-archive.gpg
RUN echo "deb https://qgis.org/ubuntu-ltr jammy main" >> /etc/apt/sources.list.d/qgis.list

# Install QGIS and processing packages
RUN apt-get update && apt-get install -y \
    qgis \
    python3-qgis \
    qgis-plugin-grass \
    grass

# Install Python dependencies for SSO and processing
RUN pip3 install \
    requests \
    gdal \
    numpy \
    pandas \
    geopandas \
    rasterio

# Create qgis user
RUN useradd -m -s /bin/bash qgis
RUN mkdir -p /run/user/1000
RUN chown -R qgis:qgis /run/user/1000

# Set up Xpra configuration
RUN mkdir -p /etc/xpra
COPY xpra.conf /etc/xpra/xpra.conf

# Copy authentication and startup scripts
COPY sso_auth.py /home/qgis/sso_auth.py
COPY start-qgis.sh /start-qgis.sh
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

RUN chmod +x /start-qgis.sh /home/qgis/sso_auth.py
RUN chown -R qgis:qgis /home/qgis

# Expose Xpra port
EXPOSE 14500

# Set environment variables
ENV DISPLAY=:100
ENV XPRA_PORT=14500
ENV XPRA_START_VIA_PROXY=1

CMD ["/usr/bin/supervisord"]