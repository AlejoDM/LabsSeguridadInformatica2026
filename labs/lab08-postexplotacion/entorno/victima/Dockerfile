# Host comprometido del Lab 08. Caés como 'operador' (sin privilegios).
FROM debian:stable-slim
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
      bash coreutils procps curl python3 findutils iproute2 ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN useradd -m -s /bin/bash operador
COPY setup.sh /setup.sh
RUN chmod +x /setup.sh && /setup.sh && rm /setup.sh
CMD ["sleep", "infinity"]
