# Contenedor ATACANTE — la "consola" del pentester.
# Trae las tools ya instaladas: el alumno no ensucia su máquina con nada.
FROM debian:stable-slim
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
      nmap ncat curl wget whois dnsutils iputils-ping netcat-openbsd \
      dirb gobuster whatweb wfuzz \
      python3 python3-pip jq git less vim-tiny ca-certificates \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /loot
COPY motd /etc/motd
RUN echo 'cat /etc/motd' >> /root/.bashrc
CMD ["sleep", "infinity"]
