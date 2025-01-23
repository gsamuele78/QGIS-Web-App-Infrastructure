# File: services/qgis-desktop/Dockerfile
FROM ubuntu:22.04

# Avoid interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install essential dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    software-properties-common \
    xvfb \
    x11vnc \
    novnc \
    supervisor \
    fonts-liberation \
    libgl1-mesa-glx \
    libglib2.0-0

# Add QGIS repository
RUN wget -O - https://qgis.org/downloads/qgis-2022.gpg.key | gpg --dearmor > /etc/apt/trusted.gpg.d/qgis-archive.gpg
RUN echo "deb https://qgis.org/ubuntu-ltr jammy main" >> /etc/apt/sources.list.d/qgis.list

# Install QGIS and additional processing packages
RUN apt-get update && apt-get install -y \
    qgis \
    python3-qgis \
    qgis-plugin-grass \
    grass \
    python3-pip

# Install Python dependencies for QGIS processing
RUN pip3 install \
    gdal \
    numpy \
    pandas \
    geopandas \
    rasterio

# Create qgis user
RUN useradd -m -s /bin/bash -G sudo qgis
USER qgis
WORKDIR /home/qgis

# Configure NoVNC and VNC
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY start-qgis.sh /start-qgis.sh
RUN chmod +x /start-qgis.sh

# Expose VNC and NoVNC ports
EXPOSE 5901 6080

# Set default command
CMD ["/usr/bin/supervisord"]
