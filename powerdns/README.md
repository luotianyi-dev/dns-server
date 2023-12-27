# PowerDNS
此镜像为 Tianyi Network 权威 DNS 服务器 Primary 节点所使用镜像。

镜像以 [Debian](https://www.debian.org/) 为基础镜像，使用 [PowerDNS](https://www.powerdns.com/) 作为 DNS 权威服务器，仅支持 MySQL Backend。

## 基础镜像
此镜像基于 Debian 11 Slim 版本 ([`debian:11-slim`](https://hub.docker.com/_/debian))。

## 标签
 - `latest`: 最新版本
 - `<powerdns-version>`: 指定 PowerDNS 版本

## 运行镜像
运行以下命令以获取镜像：

```bash
docker pull ghcr.io/luotianyi-dev/powerdns
```

运行以下命令以启动容器：
```bash
docker run -d --name powerdns \
    -p 53:53/udp \
    -p 53:53/tcp \
    -p 127.0.0.1:8000:80 \
    -e MYSQL_PASSWORD=your-mysql-password \
    -e POWERDNS_API_KEY=your-powerdns-api-key \
    -v /etc/pdns.conf:/conf/pdns.conf:ro \
    ghcr.io/luotianyi-dev/powerdns
```

## 配置
### 环境变量
此镜像使用以下环境变量：

Environment Variable | Default Value | Description
-------------------- | ------------- | -------------------
`MYSQL_PASSWORD`     | `powerdns`    | PowerDNS 数据库密码
`POWERDNS_API_KEY`   | `password`    | PowerDNS API 密钥

### 卷
此镜像使用以下卷：

Host Path                     | Mount Point       | Description
------------------------------|-------------------|-----------------
Your `powerdns` configuration | `/conf/pdns.conf` | PowerDNS 配置文件

### 暴露端口
此镜像使用以下端口：
 - `53/udp`: DNS 服务
 - `53/tcp`: DNS 服务
 - `80/tcp`: PowerDNS Web API

以上端口为默认端口，配置文件可能覆盖以上端口。

### 配置文件
配置文件应被挂载到 `/conf/pdns.conf`，以下为配置文件示例：

```conf
webserver=yes
webserver-port=80
webserver-address=0.0.0.0
webserver-allow-from=127.0.0.1,10.0.0.0/24
api=yes

launch=gmysql
gmysql-host=host
gmysql-dbname=powerdns
gmysql-user=powerdns
gmysql-dnssec=yes

default-soa-edit=INCEPTION-INCREMENT
default-soa-edit-signed=INCEPTION-INCREMENT

allow-axfr-ips=127.0.0.1,10.0.0.0/24
also-notify=10.0.0.54,10.0.0.55
only-notify=10.0.0.0/24
master=yes
```

此配置是一个 **Hidden Primary** 服务器的配置，只允许 `10.0.0.54` 和 `10.0.0.55` 两个 DNS 服务器进行 AXFR，以防止主服务器被直接暴露给用户。此配置同时在 `80` 端口暴露 API，并仅允许 `10.0.0.0/24` 访问 API。

## 使用 Docker Compose 运行
以下为 Docker Compose 配置文件示例：
```yaml
version: '3.8'

networks:
  powerdns:
    name: powerdns
    driver_opts:
      com.docker.network.bridge.name: cni-br0
    ipam:
      config:
        - subnet: 192.168.18.0/24

services:
  powerdns:
    image: ghcr.io/luotianyi-dev/powerdns:latest
    container_name: powerdns
    restart: always
    networks:
      powerdns:
        ipv4_address: 192.168.18.2
    environment:
      - MYSQL_PASSWORD=powerdns
      - POWERDNS_API_KEY=password
    ports:
      - 53:53/udp
      - 53:53/tcp
      - 127.0.0.1:8000:80
    volumes:
      - /etc/pdns.conf:/conf/pdns.conf:ro
    healthcheck:
      test: ["CMD", "curl", "-sfvo", "/dev/null", "localhost"]
      retries: 3
      timeout: 30s
      interval: 30s
      start_period: 15s
    deploy:
      resources:
        limits:
          memory: 512M
```

## 构建
运行以下命令以构建镜像：
```bash
docker build . -t ghcr.io/luotianyi-dev/powerdns:latest
```

## 许可
[PowerDNS](https://www.powerdns.com/) 基于 [GPLv2](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html) 许可。

镜像构建代码基于 [MPL 2.0](https://www.mozilla.org/en-US/MPL/2.0/) 许可。
