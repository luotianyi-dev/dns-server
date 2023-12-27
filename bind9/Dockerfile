FROM    alpine:3.18
ARG     IMAGE_VERSION=latest
LABEL   org.opencontainers.image.title=bind9 \
        org.opencontainers.image.url=https://github.com/luotianyi-dev/dns-server/tree/main/bind9 \
        org.opencontainers.image.source=https://github.com/luotianyi-dev/dns-server \
        org.opencontainers.image.documentation=https://github.com/luotianyi-dev/dns-server/blob/main/bind9/README.md \
        org.opencontainers.image.licenses=MPL-2.0 \
        org.opencontainers.image.version=${IMAGE_VERSION}
COPY    conf.py container-entrypoint.sh container-cron.sh /
RUN     apk add --no-cache netcat-openbsd bind python3 && \
        rm -rfv  /etc/bind && \
        install -d -m 755 -o named -g named /var/cache/bind && \
        chmod +x /container-entrypoint.sh /container-cron.sh
ENV     ZONE_UPDATE_INTERVAL_SECONDS=60
COPY    conf     /etc/bind
EXPOSE  53/tcp 53/udp

MAINTAINER   Tianyi Network <support@luotianyi.dev>
HEALTHCHECK  --interval=30s --timeout=15s --start-period=15s --retries=3 CMD \
             nc -zv 127.0.0.1 53
ENTRYPOINT  ["/container-entrypoint.sh"]
