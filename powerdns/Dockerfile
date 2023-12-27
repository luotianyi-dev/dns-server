FROM    debian:11-slim
ARG     IMAGE_VERSION=latest
LABEL   org.opencontainers.image.title=powerdns \
        org.opencontainers.image.url=https://github.com/luotianyi-dev/dns-server/tree/main/powerdns \
        org.opencontainers.image.source=https://github.com/luotianyi-dev/dns-server \
        org.opencontainers.image.documentation=https://github.com/luotianyi-dev/dns-server/blob/main/powerdns/README.md \
        org.opencontainers.image.licenses=GPL-2.0 \
        org.opencontainers.image.version=${IMAGE_VERSION}
RUN     apt update && \
        apt install -y curl dnsutils pdns-server pdns-backend-mysql && \
        mkdir -p /conf && \
        cp -v /etc/powerdns/pdns.conf /conf
ENV     MYSQL_PASSWORD=powerdns \
        POWERDNS_API_KEY=password
EXPOSE  53/tcp 53/udp 80/tcp

MAINTAINER   Tianyi Network <support@luotianyi.dev>
HEALTHCHECK  --interval=30s --timeout=15s --start-period=15s --retries=3 CMD \
             curl -sfvo /dev/null localhost
ENTRYPOINT   pdns_server --config-dir=/conf --api-key=$POWERDNS_API_KEY --gmysql-password=$MYSQL_PASSWORD
