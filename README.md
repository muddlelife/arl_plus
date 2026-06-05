# ARL 资产侦察灯塔系统

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)
[![Github Issues](https://img.shields.io/github/issues/Aabyss-Team/ARL.svg)](https://github.com/Aabyss-Team/ARL/issues)
[![Github Stars](https://img.shields.io/github/stars/Aabyss-Team/ARL.svg)](https://github.com/Aabyss-Team/ARL/stargazers)

ARL(Asset Reconnaissance Lighthouse) 用于快速发现、整理和监控目标关联的互联网资产，帮助安全团队建立基础资产信息库。

本仓库基于已下线的 `TophantTechnology/ARL` 开源版本维护，ARL-NPoC 依赖使用 [Aabyss-Team/ARL-NPoC](https://github.com/Aabyss-Team/ARL-NPoC)。使用前请阅读并同意 [免责声明](Disclaimer.md)。

## 功能

1. 域名资产发现、爆破和解析
2. IP/IP 段资产整理
3. 端口扫描和服务识别
4. Web 站点指纹识别、截图和爬虫
5. 资产分组、搜索和周期监控
6. 任务策略、计划任务和周期任务
7. GitHub 关键字监控
8. 文件泄露风险检测
9. nuclei PoC 调用
10. WebInfoHunter 调用和监控

## 系统要求

| 项目 | 建议配置 |
| --- | --- |
| 操作系统 | Linux，推荐 Debian 12 / Ubuntu 20.04+ / Rocky 8+ |
| CPU | 4 核以上 |
| 内存 | 8 GB 以上 |
| 带宽 | 10 Mbps 以上 |
| Docker | Docker Engine 24+ |
| Compose | Docker Compose v2+ |

目前不支持 Windows 生产部署。资产发现会产生大量网络请求，建议在云服务器或独立测试环境运行。

## Docker 部署

Docker 是当前推荐部署方式。应用镜像基于 `python:3.11-slim-bookworm` 构建，MongoDB 和 RabbitMQ 使用独立官方镜像。

```bash
cd docker/
cp .env.example .env
# 必须编辑 .env，设置管理员、MongoDB、RabbitMQ 密码
docker volume create arl_db
ARL_VERSION=local docker compose up -d --build
```

首次构建通常需要 5 到 10 分钟。启动完成后访问：

```text
https://<服务器IP>:5003/
```

登录账号由 `docker/.env` 中的 `ARL_ADMIN_USERNAME` 和 `ARL_ADMIN_PASSWORD` 决定，容器启动时会自动创建或更新管理员账号。公网部署前请务必使用强密码。

Web 默认对外暴露 HTTPS 端口 `5003`。如需修改宿主机端口，请在 `docker/.env` 中设置 `ARL_WEB_PORT`，例如：`ARL_WEB_PORT=8443`。
MongoDB 和 RabbitMQ 仅在 Docker 内部网络中访问，不会发布到宿主机端口。

## Docker 配置

`docker/.env.example` 提供可配置项模板，复制为 `docker/.env` 后生效。

| 变量 | 默认值 | 说明 |
| --- | --- | --- |
| ARL_WEB_PORT | 5003 | Web HTTPS 宿主机端口 |
| ARL_ADMIN_USERNAME | admin | Web 登录用户名 |
| ARL_ADMIN_PASSWORD | 必填 | Web 登录密码 |
| CELERY_ARLTASK_CONCURRENCY | 2 | 主任务队列 Worker 并发数 |
| CELERY_ARLGITHUB_CONCURRENCY | 2 | GitHub 队列 Worker 并发数 |
| MONGO_INITDB_ROOT_USERNAME | admin | MongoDB root 用户 |
| MONGO_INITDB_ROOT_PASSWORD | 必填 | MongoDB root 密码 |
| MONGO_INITDB_DATABASE | arl | MongoDB 初始化数据库 |
| RABBITMQ_DEFAULT_USER | arl | RabbitMQ 用户 |
| RABBITMQ_DEFAULT_PASS | 必填 | RabbitMQ 密码 |
| RABBITMQ_DEFAULT_VHOST | arlv2host | RabbitMQ vhost |
| ARL_VERSION | local | 本地构建镜像 tag |
| GITHUB_TOKEN | 空 | GitHub 关键字监控 Token |

如需启用 GitHub 关键字监控，请设置：

```bash
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
```

修改 `.env` 后重启服务：

```bash
docker compose up -d --build
```

## 服务验证

```bash
cd docker/
docker compose ps
curl -k https://127.0.0.1:5003/
docker compose logs -f --tail=50 web
docker compose logs -f --tail=50 worker
```

正常情况下，`web`、`worker`、`scheduler`、`mongodb`、`rabbitmq` 都应为 `Up`，首页请求返回 `200`。

## 常用操作

```bash
cd docker/
docker compose up -d --build
docker compose restart web
docker compose restart worker
docker compose logs -f --tail=50
docker compose down
```

## 卸载与清理（Docker）

在 `docker/` 目录执行。

1. 全部卸载（包含数据，危险：会删除 MongoDB 数据卷）

```bash
cd docker/
ARL_VERSION=local docker compose down --rmi all --volumes --remove-orphans

# 如果你使用的是 external volume（默认 arl_db），上面的 --volumes 不会删除它，需要手动删：
docker volume rm -f arl_db
```

2. 仅卸载镜像（不删除数据卷）

```bash
cd docker/
ARL_VERSION=local docker compose down --rmi all --remove-orphans

# 可选：如果还有残留的本地 tag（例如 arl:local），手动删除：
docker image rm -f arl:local 2>/dev/null || true
```

持久化数据库卷为 `arl_db`。删除该卷会清空 MongoDB 数据。

## 本地开发

本地开发需要 Python 3.11。建议只用 Docker 启动 MongoDB 和 RabbitMQ，然后在宿主机运行 Flask。

```bash
cd docker/
docker compose up -d mongodb rabbitmq
cd ..
```

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/pip install -e 'git+https://github.com/Aabyss-Team/ARL-NPoC#egg=xing'
cp app/config.yaml.example app/config.yaml
```

开发环境中请确认 `app/config.yaml` 连接本地依赖服务：

```yaml
MONGO:
  URI: mongodb://admin:admin@127.0.0.1:27017/
CELERY:
  BROKER_URL: amqp://arl:arlpassword@127.0.0.1:5672/arlv2host
```

启动 Web：

```bash
.venv/bin/python -m flask --app app.main:arl_app run --debug
```

## 测试

```bash
.venv/bin/python -m unittest discover -s test -p 'test_*.py' -v
```

测试中依赖外部凭证、GeoLite2 数据库、固定 DB fixture 或外部二进制的用例，在缺少依赖时会自动 skip。

## 配置文件

运行时配置从 `app/config.yaml` 加载。Docker 部署时，`docker/config-docker.yaml` 会挂载为容器内的 `/code/app/config.yaml`。

| 配置项 | 说明 |
| --- | --- |
| MONGO | MongoDB 连接信息 |
| CELERY.BROKER_URL | RabbitMQ 连接信息 |
| QUERY_PLUGIN | 域名查询插件 Token |
| GEOIP | GeoLite2 数据库路径 |
| FOFA | FOFA API 配置 |
| GITHUB.TOKEN | GitHub 搜索 Token，Docker 下可由 `GITHUB_TOKEN` 环境变量覆盖 |
| DINGDING / FEISHU / WXWORK / EMAIL | 消息推送配置 |
| ARL.AUTH | 是否开启认证 |
| ARL.API_KEY | 后端 API 调用 key |
| ARL.BLACK_IPS | SSRF 防护黑名单 |
| ARL.PORT_TOP_10 | 自定义端口测试选项 |
| ARL.DOMAIN_DICT | 域名爆破字典 |
| ARL.FILE_LEAK_DICT | 文件泄漏字典 |

## 升级说明

本仓库已将运行环境升级到 Python 3.11，并使用 Debian 12(bookworm) 官方基础镜像构建 Docker 镜像。

主要收益如下：

1. 性能与稳定性：Python 3.11 在解释器层面带来整体性能提升，长期运行的 worker/scheduler 更稳定。
2. 依赖生态：新版本依赖更容易安装与维护，减少旧版依赖(如老 PyYAML)在新系统上的构建问题。
3. 安全与可维护性：Debian 12 官方镜像具备更及时的安全更新，减少过时系统组件带来的风险。
4. Docker 体验：统一 `docker/Dockerfile` 构建应用镜像，`docker compose` 一键启动，管理员账号、worker 并发、GitHub Token 等都可在 `.env` 配置。

已做的关键改进包括：修复 3.11 下的弃用用法、解决循环导入问题、Docker 构建自包含(构建时拉取 ARL-NPoC/GeoLite2/nuclei 等)、测试在缺少外部依赖时自动 skip。

## 忘记密码

Docker 部署推荐直接修改 `docker/.env` 中的 `ARL_ADMIN_USERNAME` 和 `ARL_ADMIN_PASSWORD`，然后重启 `web` 服务：

```bash
cd docker/
docker compose up -d web
```

如需手动重置 MongoDB 中的账号：

```bash
docker exec -ti arl_mongodb mongo -u admin -p admin
use arl
db.user.drop()
db.user.insert({ username: 'admin', password: hex_md5('arlsalt!@#' + 'admin123') })
```

重置后可使用 `admin` / `admin123` 登录。

## 项目结构

| 路径 | 说明 |
| --- | --- |
| app/ | Flask 后端、Celery 任务和业务逻辑 |
| app/tools/ | 内置工具和脚本 |
| docker/ | Dockerfile、Compose、Nginx、前端静态资源和容器配置 |
| test/ | 单元测试和集成测试 |
| requirements.txt | Python 3.11 依赖 |

## 相关链接

1. ARL-NPoC: [https://github.com/Aabyss-Team/ARL-NPoC](https://github.com/Aabyss-Team/ARL-NPoC)
2. FAQ: [https://tophanttechnology.github.io/ARL-doc/faq/](https://tophanttechnology.github.io/ARL-doc/faq/)
3. 原始项目说明: [https://github.com/TophantTechnology/ARL](https://github.com/TophantTechnology/ARL)

## 免责声明

本工具仅用于合法授权的资产梳理和安全测试。使用者应自行承担使用本项目产生的全部风险，并遵守所在地区的法律法规。
