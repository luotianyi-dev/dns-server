# BIND9
此镜像为 Tianyi Network 权威 DNS 服务器 Secondary 节点所使用镜像。

镜像以 [Alpine Linux](https://alpinelinux.org/) 为基础镜像，使用 [BIND9](https://www.isc.org/bind/) 作为 DNS 服务器，增加了从 [PowerDNS](https://www.powerdns.com/) API 获取 DNS Zone 列表的功能。

## 基础镜像
此镜像基于 Alpine Linux 3.18 ([`alpine:3.18`](https://hub.docker.com/_/alpine))。

## 标签
 - `latest`: 最新版本
 - `<bind-version>`: 指定 BIND9 版本
 - `<bind-version>-<alpine-version>`: 指定 BIND9 版本和 Alpine Linux 版本

## 运行镜像
运行以下命令以获取镜像：

```bash
docker pull ghcr.io/luotianyi-dev/bind9
```

运行以下命令以启动容器：
```bash
docker run -d --name bind9 \
    -p 53:53/udp \
    -p 53:53/tcp \
    -e UPSTREAM_API_URL=http://your-powerdns-api-server:9000 \
    -e UPSTREAM_API_KEY=your-powerdns-api-key \
    -e NAMED_UPSTREAM_IP=your-powerdns-server-ip \
    ghcr.io/luotianyi-dev/bind9
```

## 配置
### 环境变量
此镜像使用以下环境变量：

Environment Variable           | Default Value                                     | Description
------------------------------ | ------------------------------------------------- | ----------------------------------------------
`UPSTREAM_API_URL`             | `http://127.0.0.1/api/v1/servers/localhost/zones` | PowerDNS Web API 的 URL，用于获取 DNS Zone 列表
`UPSTREAM_API_KEY`             | `password`                                        | PowerDNS Web API 密钥
`NAMED_BANNER_TEXT`            | `BIND9`                                           | BIND9 的 `option.version` 配置项
`NAMED_CLUSTER_CIDR`           | `10.0.0.0/24`                                     | BIND9 所在集群的 CIDR，用于进行内网 AXFR
`NAMED_UPSTREAM_IP`            | `10.0.0.1`                                        | PowerDNS 服务器的 IP 地址，作为 AXFR 请求的上游服务器
`NAMED_RNDC_KEY`               | Random Base64 String                              | RNDC 密钥
`ZONE_UPDATE_INTERVAL_SECONDS` | `60`                                              | 从 PowerDNS API 更新 DNS Zone 的间隔时间

### 卷
此镜像不使用卷。

### 暴露端口
此镜像使用以下端口：
 - `53/udp`: DNS 服务
 - `53/tcp`: DNS 服务
 - `953/tcp`: RNDC 服务
 - `8053/tcp`: XML Statistics Channels

### 配置文件
此镜像无需额外配置文件。

## 使用 Docker Compose 运行
以下为 Docker Compose 配置文件示例：
```yaml
version: '3.8'

networks:
  bind9:
    name: bind9
    driver_opts:
      com.docker.network.bridge.name: cni-br0
    ipam:
      config:
        - subnet: 192.168.18.0/24

services:
  bind9:
    image: ghcr.io/luotianyi-dev/bind9:latest
    container_name: bind9
    restart: always
    networks:
      bind9:
        ipv4_address: 192.168.18.2
    environment:
      - UPSTREAM_API_URL=http://192.168.18.1:9000/api/v1/servers/localhost/zones
      - UPSTREAM_API_KEY=powerdns-api-key
      - NAMED_BANNER_TEXT=TianyiDNS-7.12
      - NAMED_CLUSTER_CIDR=192.168.0.0/16
      - NAMED_UPSTREAM_IP=192.168.18.1
    ports:
      - 53:53/udp
      - 53:53/tcp
    healthcheck:
      test: ["CMD", "nc", "-zv", "127.0.0.1", "53"]
      retries: 3
      timeout: 30s
      interval: 30s
      start_period: 15s
    deploy:
      resources:
        limits:
          memory: 256M
```

## 构建
运行以下命令以构建镜像：
```bash
docker build . -t ghcr.io/luotianyi-dev/bind9:latest
```

## 许可
[BIND9](https://archlinux.org/packages/extra/x86_64/bind/) 基于 [MPL 2.0](https://www.mozilla.org/en-US/MPL/2.0/) 许可。

镜像构建代码基于 [MPL 2.0](https://www.mozilla.org/en-US/MPL/2.0/) 许可。
