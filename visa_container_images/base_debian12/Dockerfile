# syntax=docker/dockerfile:1

FROM debian:12-slim

LABEL maintainer="ALBA Synchrotron"

ENV DEBIAN_FRONTEND=noninteractive
ENV FILES=/src
ENV HOME=/etc/visa_home_template

## Copy the installation scripts to the image
RUN mkdir ${FILES}
COPY scripts/ ${FILES}/
RUN find ${FILES}/ -name '*.sh' -exec chmod a+x {} +
WORKDIR ${FILES}

# Packages and GUI installation
RUN apt-get update && apt-get install --no-install-recommends -y \
    ca-certificates \    
    dbus-x11 \
    kwin-x11 \
    x11-xserver-utils \
    kde-plasma-desktop \
    qml-module-org-kde-kitemmodels \
    qml-module-org-kde-kquickcontrolsaddons \
    qml-module-qt-labs-platform \    
    xserver-xorg \
    xserver-xorg-core \
    xserver-xorg-video-dummy \
    xorgxrdp \
    xrdp \
    bash \
    policykit-1 \
    supervisor \
    xauth \
    firefox-esr \
    git \
    curl \
    ssh \
    cmake \
    build-essential \
    libpam0g-dev \
    libssl-dev \
    pkg-config \
    check \
    strace \
    rsyslog \
    libpam-cap \
    && apt-get clean \
    && apt-get autoclean -y \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/cache/apt/archives/*

# GUI configuration
RUN mkdir ${HOME}
RUN touch ${HOME}/.Xauthority

## Set wallpaper
COPY files/wall.png ${FILES}/
RUN ${FILES}/configure_wallpaper.sh

# Customize Kiosk mode (restrictions)
RUN mkdir ${HOME}/.config
COPY files/kdeglobals ${HOME}/.config/kdeglobals

# Generate machine-id for dbus
RUN dbus-uuidgen > /etc/machine-id

## Configure XRDP
RUN sed -i 's/^test -x/#test -x/' /etc/init.d/xrdp
RUN sed -i "\   
   s/fork=true/fork=false/g; \
   s/\#tls_ciphers=HIGH/tls_ciphers=HIGH/g; \
   s/^new_cursors=true/new_cursors=false/g \
 " /etc/xrdp/xrdp.ini
# Disable root login and syslog logging for xrdp-sesman
RUN sed -i "\
   s/AllowRootLogin=true/AllowRootLogin=false/g; \
   s/EnableSyslog=1/EnableSyslog=0/g \
 " /etc/xrdp/sesman.ini
# Allow all users to start xserver
RUN echo 'allowed_users=anybody' > /etc/X11/Xwrapper.config
RUN chmod g+w /etc/xrdp
RUN chmod u+s /usr/sbin/xrdp-sesman
RUN chmod u+s /usr/sbin/xrdp
RUN usermod -a -G ssl-cert xrdp
# Logs forwarding
RUN ln -sf /dev/stdout /var/log/xrdp.log
RUN ln -sf /dev/stdout /var/log/xrdp-sesman.log
# Custom configuration
RUN cp ${FILES}/startwm.sh /etc/xrdp/startwm.sh

## Configure VISA PAM
RUN git clone https://github.com/ILLGrenoble/visa-pam.git
RUN cd visa-pam && cmake . && make && make install
RUN rm -rf visa-pam
RUN rm /etc/pam.d/xrdp-sesman
COPY --chmod=644 files/xrdp-sesman /etc/pam.d/xrdp-sesman

## Install VISA CUPS driver
RUN apt-get update \
    && apt-get install cups -y \
    && git clone https://github.com/ALBA-Synchrotron/visa-cups.git
RUN chmod +x ./visa-cups/install.sh
RUN cd visa-cups && ./install.sh
RUN cp visa-cups/visa.ppd /etc/cups/ppd/visa.ppd
COPY files/printers.conf /etc/cups/printers.conf

## Add SSH known hosts
COPY files/known_hosts ${FILES}/known_hosts
RUN chmod 666 ${FILES}/known_hosts
COPY files/99-known-hosts-and-identity-file.conf /etc/ssh/ssh_config.d/99-known-hosts-and-identity-file.conf

# Suport a UIDs alts
RUN sed -i '/^UID_MAX/d' /etc/login.defs && \
    sed -i '/^SUB_UID_MAX/d' /etc/login.defs && \
    echo "UID_MAX 1000000000" >> /etc/login.defs && \
    echo "SUB_UID_MAX 1000000000" >> /etc/login.defs

## Expose RDP port
EXPOSE 3389

## supervisord configurarion
RUN mkdir -p /var/log/supervisor
COPY files/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

CMD ["/usr/bin/supervisord", "-n", "-c", "/etc/supervisor/conf.d/supervisord.conf"]

