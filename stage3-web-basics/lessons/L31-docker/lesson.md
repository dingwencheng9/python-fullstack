# L31: Docker 容器化部署

> **课程编号**: L31
> **所属阶段**: Stage 3 - Web 开发基础
> **预计时长**: 4-5 小时
> **难度**: ⭐⭐⭐☆☆（中级）
> **前置课程**: L26, L28
> **版本**: v1.0
> **最后更新**: 2026-07-23
> **核心版本**: Python 3.13


---

## 🎯 学习目标

完成本课程后，你将能够：

1. ✅ **Docker 基础**：理解容器概念和核心命令
2. ✅ **镜像管理**：构建、优化、发布 Docker 镜像
3. ✅ **容器编排**：使用 Docker Compose 管理多容器应用
4. ✅ **Python 项目容器化**：将 FastAPI 应用容器化
5. ✅ **开发环境配置**：使用 Docker 构建开发环境

---

## Part 1: Docker 基础概念

### 1.1 容器 vs 虚拟机

```
┌─────────────────────────────────────────────────────────┐
│                    架构对比                            │
├─────────────────────────────────────────────────────────┤
│                                                     │
│  虚拟机架构：              容器架构：                  │
│  ┌──────────────┐        ┌──────────────┐           │
│  │ Guest OS     │        │   App 1      │           │
│  │ ├─ App 1     │        ├──────────────┤           │
│  │ └─ App 2     │        │   App 2      │           │
│  └──────────────┘        ├──────────────┤           │
│  ┌──────────────┐        │   App 3      │           │
│  │ Guest OS     │        ├──────────────┤           │
│  │ └─ App 3     │        │   Docker     │           │
│  └──────────────┘        │   Engine     │           │
│  ┌──────────────┐        ├──────────────┤           │
│  │ Hypervisor   │        │   Host OS    │           │
│  ├──────────────┤        └──────────────┘           │
│  │   Host OS    │                                    │
│  └──────────────┘                                    │
│                                                     │
│  资源占用：更大              资源占用：更小           │
│  启动速度：分钟              启动速度：秒级           │
│  隔离性：完全隔离            隔离性：进程级           │
│                                                     │
└─────────────────────────────────────────────────────────┘
```

### 1.2 Docker 核心概念

| 概念 | 说明 | 类比 |
|------|------|------|
| **Image** | 镜像，只读模板 | 类（Class） |
| **Container** | 容器，镜像的运行实例 | 对象（Object） |
| **Registry** | 镜像仓库 | GitHub |
| **Dockerfile** | 构建镜像的脚本 | 构建配方 |

### 1.3 Docker 安装

```bash
# macOS
brew install --cask docker

# Linux (Ubuntu)
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER  # 添加用户到 docker 组

# 验证安装
docker --version
docker ps
docker images
```

---

## Part 2: Docker 基础命令

### 2.1 镜像操作

```bash
# 拉取镜像
docker pull python:3.13-slim

# 查看本地镜像
docker images
docker images python

# 删除镜像
docker rmi python:3.13-slim

# 构建镜像
docker build -t myapp:1.0 .

# 标记镜像
docker tag myapp:1.0 registry.example.com/myapp:1.0

# 推送镜像
docker push registry.example.com/myapp:1.0

# 清理未使用镜像
docker image prune -a
```

### 2.2 容器操作

```bash
# 运行容器
docker run python:3.13-slim python --version

# 交互式运行
docker run -it python:3.13-slim bash

# 后台运行
docker run -d --name myapp -p 8000:8000 myapp:1.0

# 查看运行中的容器
docker ps

# 查看所有容器
docker ps -a

# 停止/启动容器
docker stop myapp
docker start myapp

# 进入容器
docker exec -it myapp bash

# 查看日志
docker logs -f myapp

# 删除容器
docker rm myapp

# 查看资源使用
docker stats
```

### 2.3 端口映射与数据卷

```bash
# 端口映射
docker run -p 8000:8000 myapp

# 多个端口
docker run -p 8000:8000 -p 5432:5432 myapp

# 绑定数据卷（持久化存储）
docker run -v /host/path:/container/path myapp

# 命名数据卷
docker run -v mydata:/data myapp

# 只读挂载
docker run -v /host/path:/container/path:ro myapp

# 查看数据卷
docker volume ls
docker volume inspect mydata
```

### 2.4 环境变量

```bash
# 设置环境变量
docker run -e DATABASE_URL=postgres://... myapp

# 从文件加载环境变量
docker run --env-file .env myapp

# 查看环境变量
docker exec myapp env
```

---

## Part 3: Dockerfile 编写

### 3.1 基础 Dockerfile

```dockerfile
# Dockerfile
# 基础镜像
FROM python:3.13-slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 暴露端口
EXPOSE 8000

# 环境变量
ENV PYTHONUNBUFFERED=1

# 启动命令
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 3.2 多阶段构建

```dockerfile
# 多阶段构建示例
# Stage 1: 构建阶段
FROM python:3.13-slim AS builder

WORKDIR /app

# 安装构建依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装依赖到虚拟环境
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: 运行阶段
FROM python:3.13-slim

WORKDIR /app

# 从 builder 复制虚拟环境
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# 复制应用代码
COPY . .

# 运行用户
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 3.3 .dockerignore

```dockerignore
# 忽略文件
__pycache__
*.pyc
*.pyo
*.pyd
.Python
*.so
*.egg
*.egg-info
dist
build
.pytest_cache
.coverage
htmlcov
.git
.gitignore
.env
.env.*
*.md
docs
tests
*.log
```

### 3.4 构建优化技巧

```dockerfile
# ❌ 低效：每次修改代码都重新安装依赖
COPY . .
RUN pip install -r requirements.txt

# ✅ 高效：先复制依赖文件，安装后再复制代码
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

# ❌ 低效：使用最新标签
FROM python:latest

# ✅ 高效：使用具体版本
FROM python:3.13-slim

# ❌ 低效：使用 pip 无缓存
RUN pip install package

# ✅ 高效：使用 --no-cache-dir
RUN pip install --no-cache-dir package

# ❌ 低效：分开 RUN 指令
RUN apt-get update
RUN apt-get install -y package
RUN apt-get clean

# ✅ 高效：合并 RUN 指令
RUN apt-get update && \
    apt-get install -y --no-install-recommends package && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```

---

## Part 4: Docker Compose

### 4.1 docker-compose.yml 基础

```yaml
# docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/myapp
      - REDIS_URL=redis://cache:6379
    depends_on:
      - db
      - cache
    volumes:
      - ./app:/app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  db:
    image: postgres:16-alpine
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=myapp
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  cache:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

### 4.2 服务依赖与启动顺序

```yaml
# depends_on 确保启动顺序
services:
  web:
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:16-alpine
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d myapp"]
      interval: 5s
      timeout: 5s
      retries: 5
```

### 4.3 开发与生产配置

```yaml
# docker-compose.yml (基础配置)
version: '3.8'

services:
  web:
    build: .
    environment:
      - ENV=development

# docker-compose.prod.yml (生产覆盖)
version: '3.8'

services:
  web:
    restart: always
    environment:
      - ENV=production
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M

# 使用：docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### 4.4 常用命令

```bash
# 启动服务
docker-compose up
docker-compose up -d  # 后台运行

# 停止服务
docker-compose down
docker-compose down -v  # 删除数据卷

# 重建服务
docker-compose up --build

# 查看日志
docker-compose logs -f web

# 进入容器
docker-compose exec web bash

# 扩展服务
docker-compose up --scale web=3

# 查看服务状态
docker-compose ps
```

---

## Part 5: Python 项目容器化实战

### 5.1 项目结构

```
my_fastapi_app/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── models.py
│   └── ...
├── tests/
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── requirements.txt
├── pyproject.toml
└── .dockerignore
```

### 5.2 requirements.txt

```txt
# requirements.txt
fastapi>=0.115.0
uvicorn[standard]>=0.32.0
pydantic>=2.10.0
sqlalchemy>=2.0.0
psycopg2-binary>=2.9.0
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
```

### 5.3 完整 Dockerfile

```dockerfile
# docker/Dockerfile
# ============ 构建阶段 ============
FROM python:3.13-slim AS builder

WORKDIR /app

# 安装构建依赖
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件并安装
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# ============ 运行阶段 ============
FROM python:3.13-slim

# 安全：创建非 root 用户
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

WORKDIR /app

# 从 builder 复制 Python 包
COPY --from=builder /root/.local /home/appuser/.local
ENV PATH="/home/appuser/.local/bin:$PATH"

# 复制应用代码
COPY --chown=appuser:appgroup app/ ./app/

# 设置用户
USER appuser

# 环境变量
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# 暴露端口
EXPOSE 8000

# 健康检查
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

# 启动命令
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 5.4 Docker Compose 完整配置

```yaml
# docker/docker-compose.yml
version: '3.8'

services:
  api:
    build:
      context: ..
      dockerfile: docker/Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql+asyncpg://taskflow:taskflow@db:5432/taskflow
      - REDIS_URL=redis://cache:6379/0
      - SECRET_KEY=${SECRET_KEY:-change-me-in-production}
      - ENVIRONMENT=development
    depends_on:
      db:
        condition: service_healthy
      cache:
        condition: service_started
    volumes:
      - ..:/app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  db:
    image: postgres:16-alpine
    environment:
      - POSTGRES_USER=taskflow
      - POSTGRES_PASSWORD=taskflow
      - POSTGRES_DB=taskflow
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U taskflow -d taskflow"]
      interval: 10s
      timeout: 5s
      retries: 5

  cache:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"
    command: redis-server --appendonly yes

volumes:
  postgres_data:
  redis_data:
```

### 5.5 环境变量文件

```bash
# .env 文件（不提交到版本控制）
# .env.example 作为模板

# 应用配置
SECRET_KEY=your-super-secret-key-change-in-production
ENVIRONMENT=development

# 数据库配置
DATABASE_URL=postgresql+asyncpg://taskflow:taskflow@db:5432/taskflow

# Redis 配置
REDIS_URL=redis://cache:6379/0
```

```bash
# .env.example
SECRET_KEY=change-me-in-production
ENVIRONMENT=development
DATABASE_URL=postgresql+asyncpg://taskflow:taskflow@db:5432/taskflow
REDIS_URL=redis://cache:6379/0
```

---

## Part 6: 开发环境配置

### 6.1 开发专用配置

```yaml
# docker/docker-compose.dev.yml
version: '3.8'

services:
  api:
    volumes:
      - ..:/app  # 代码热重载
    environment:
      - ENVIRONMENT=development
      - LOG_LEVEL=DEBUG
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  db:
    ports:
      - "5432:5432"  # 暴露端口给本地工具

  pgadmin:
    image: dpage/pgadmin4
    environment:
      - PGADMIN_DEFAULT_EMAIL=admin@example.com
      - PGADMIN_DEFAULT_PASSWORD=admin
    ports:
      - "5050:80"
```

### 6.2 使用 Makefile 简化操作

```makefile
# Makefile
.PHONY: help install dev prod test clean

help:
	@echo "Available commands:"
	@echo "  make install   - Install dependencies"
	@echo "  make dev       - Start development environment"
	@echo "  make prod      - Start production environment"
	@echo "  make test      - Run tests"
	@echo "  make clean     - Clean up containers and volumes"

install:
	uv sync

dev:
	docker-compose -f docker/docker-compose.yml -f docker/docker-compose.dev.yml up

prod:
	docker-compose -f docker/docker-compose.yml -f docker/docker-compose.prod.yml up -d

test:
	docker-compose exec api pytest tests/ -v

clean:
	docker-compose -f docker/docker-compose.yml down -v
	docker image prune -f
```

---

## Part 7: 生产部署最佳实践

### 7.1 安全配置

```dockerfile
# 不要使用 root 用户
RUN groupadd -r appgroup && useradd -r -g appgroup appuser
USER appuser

# 最小化权限
COPY --chown=appuser:appgroup app/ ./app/

# 不暴露敏感信息
# 使用环境变量或 Docker secrets
```

### 7.2 健康检查

```dockerfile
# 健康检查
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"
```

### 7.3 日志配置

```yaml
# Docker Compose 日志配置
services:
  api:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### 7.4 资源限制

```yaml
services:
  api:
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
```

---

## Part 8: 常见问题排查

### 8.1 权限问题

```bash
# 修复权限
docker exec -it myapp chown -R appuser:appgroup /app

# 或在构建时设置
RUN groupadd -r appgroup && useradd -r -g appgroup appuser
```

### 8.2 网络问题

```bash
# 检查网络
docker network ls
docker network inspect bridge

# 创建自定义网络
docker network create mynet
docker run --network mynet myapp
```

### 8.3 存储问题

```bash
# 查看磁盘使用
docker system df

# 清理
docker system prune -a
docker volume prune
```

### 8.4 日志查看

```bash
# 实时日志
docker logs -f myapp

# 查看最后 100 行
docker logs --tail 100 myapp

# 查看错误日志
docker logs myapp 2>&1 | grep -i error
```

---

## 📝 课程总结

### 核心知识点

1. **Docker 基础**
   - 容器 vs 虚拟机
   - 镜像、容器、仓库概念
   - 基础命令

2. **Dockerfile**
   - 多阶段构建
   - 构建优化
   - .dockerignore

3. **Docker Compose**
   - 多容器编排
   - 服务依赖
   - 开发/生产配置

4. **Python 项目容器化**
   - FastAPI 容器化
   - 数据库连接
   - 环境变量管理

5. **最佳实践**
   - 安全配置
   - 健康检查
   - 资源限制

---

## ✅ 完成标准

完成本课程后，你应该能够：

- [ ] 理解 Docker 核心概念
- [ ] 编写 Dockerfile 构建镜像
- [ ] 使用 Docker Compose 管理多容器应用
- [ ] 将 FastAPI 应用容器化
- [ ] 配置开发/生产环境
- [ ] 排查常见容器问题

---

**下一步**: 继续学习 [L32: SSE 服务器推送事件](../L32-sse/lesson.md)
