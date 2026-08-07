#!/usr/bin/env python3
"""
Docker 常用命令参考

本文档展示 Docker 的常用命令及其用途。
"""

from dataclasses import dataclass

@dataclass
class DockerCommand:
    """Docker 命令封装"""

    name: str
    description: str
    command: str
    example: str | None = None

    def __str__(self) -> str:
        return f"{self.name}: {self.description}\n  命令: {self.command}"


# 镜像命令
DOCKER_IMAGE_COMMANDS = [
    DockerCommand(
        name="拉取镜像",
        description="从 Docker Hub 拉取镜像",
        command="docker pull <image>:<tag>",
        example="docker pull python:3.13-slim",
    ),
    DockerCommand(
        name="列出镜像",
        description="列出本地所有镜像",
        command="docker images",
        example="docker images python",
    ),
    DockerCommand(
        name="删除镜像",
        description="删除本地镜像",
        command="docker rmi <image>",
        example="docker rmi python:3.13-slim",
    ),
    DockerCommand(
        name="构建镜像",
        description="根据 Dockerfile 构建镜像",
        command="docker build -t <name>:<tag> <path>",
        example="docker build -t myapp:1.0 .",
    ),
    DockerCommand(
        name="推送镜像",
        description="推送镜像到 Registry",
        command="docker push <registry>/<image>:<tag>",
        example="docker push docker.io/myuser/myapp:1.0",
    ),
]

# 容器命令
DOCKER_CONTAINER_COMMANDS = [
    DockerCommand(
        name="运行容器",
        description="创建并运行新容器",
        command="docker run [OPTIONS] <image>",
        example="docker run -d -p 8000:8000 --name myapp myapp:1.0",
    ),
    DockerCommand(
        name="列出容器",
        description="列出运行中的容器",
        command="docker ps",
        example="docker ps -a  # 包含已停止的",
    ),
    DockerCommand(
        name="停止容器",
        description="停止运行中的容器",
        command="docker stop <container>",
        example="docker stop myapp",
    ),
    DockerCommand(
        name="启动容器",
        description="启动已停止的容器",
        command="docker start <container>",
        example="docker start myapp",
    ),
    DockerCommand(
        name="重启容器",
        description="重启容器",
        command="docker restart <container>",
        example="docker restart myapp",
    ),
    DockerCommand(
        name="删除容器",
        description="删除已停止的容器",
        command="docker rm <container>",
        example="docker rm myapp",
    ),
    DockerCommand(
        name="进入容器",
        description="在运行中的容器内执行命令",
        command="docker exec -it <container> <command>",
        example="docker exec -it myapp /bin/bash",
    ),
    DockerCommand(
        name="查看日志",
        description="查看容器日志",
        command="docker logs [OPTIONS] <container>",
        example="docker logs -f myapp  # 实时跟踪",
    ),
]

# Docker Run 常用选项
DOCKER_RUN_OPTIONS = [
    ("-d", "后台运行容器"),
    ("-p <host>:<container>", "端口映射"),
    ("-v <host>:<container>", "卷挂载"),
    ("-e <key>=<value>", "环境变量"),
    ("--name <name>", "容器名称"),
    ("--network <network>", "网络名称"),
    ("--restart <policy>", "重启策略"),
    ("--rm", "容器停止后自动删除"),
    ("-it", "交互模式 + 终端"),
]


def print_command_list(commands: list[DockerCommand], title: str):
    """打印命令列表"""
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)

    for cmd in commands:
        print(f"\n📌 {cmd.name}")
        print(f"   说明: {cmd.description}")
        print(f"   命令: {cmd.command}")
        if cmd.example:
            print(f"   示例: {cmd.example}")


def print_docker_run_options():
    """打印 Docker Run 常用选项"""
    print("\n" + "=" * 70)
    print("Docker Run 常用选项")
    print("=" * 70)

    for option, description in DOCKER_RUN_OPTIONS:
        print(f"\n  {option:25} {description}")


def print_dockerfile_reference():
    """打印 Dockerfile 参考"""
    print("\n" + "=" * 70)
    print("Dockerfile 指令参考")
    print("=" * 70)

    instructions = [
        ("FROM <base>", "基础镜像"),
        ("RUN <command>", "执行命令"),
        ("COPY <src> <dest>", "复制文件"),
        ("WORKDIR <path>", "设置工作目录"),
        ("ENV <key>=<value>", "设置环境变量"),
        ("EXPOSE <port>", "声明端口"),
        ('CMD ["cmd", "arg"]', "容器启动命令"),
        ("ENTRYPOINT", "入口点"),
        ("ARG <name>", "构建参数"),
        ("LABEL", "元数据标签"),
    ]

    for instruction, description in instructions:
        print(f"\n  {instruction:25} {description}")


def demo_dockerfile():
    """演示 Dockerfile 模板"""
    print("\n" + "=" * 70)
    print("Dockerfile 模板")
    print("=" * 70)

    template = """# Python 应用 Dockerfile
FROM python:3.13-slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY requirements.txt .

# 安装依赖（利用缓存）
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 设置环境变量
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# 暴露端口
EXPOSE 8000

# 运行应用
CMD ["python", "main.py"]
"""
    print(template)


def demo_docker_compose():
    """演示 Docker Compose 模板"""
    print("\n" + "=" * 70)
    print("Docker Compose 模板")
    print("=" * 70)

    template = """version: "3.8"

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
    depends_on:
      - db
      - redis
    restart: unless-stopped

  db:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=mydb

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
"""
    print(template)


if __name__ == "__main__":
    print_command_list(DOCKER_IMAGE_COMMANDS, "🖼️ Docker 镜像命令")
    print_command_list(DOCKER_CONTAINER_COMMANDS, "📦 Docker 容器命令")
    print_docker_run_options()
    print_dockerfile_reference()
    demo_dockerfile()
    demo_docker_compose()
