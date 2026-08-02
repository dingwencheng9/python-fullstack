"""
练习题 1: Docker Compose 多服务编排

创建 docker-compose.yml 文件，包含以下服务：
1. agent - AI Agent 服务
2. redis - 缓存服务
3. postgres - PostgreSQL 数据库
4. prometheus - 监控服务

要求：
- agent 依赖 redis 和 postgres
- 配置健康检查
- 设置网络和卷
"""

from dataclasses import dataclass


@dataclass
class DockerService:
    """Docker 服务定义"""

    name: str
    image: str
    ports: list[str] = None
    environment: dict = None
    volumes: list[str] = None
    depends_on: list[str] = None
    healthcheck: dict = None
    networks: list[str] = None


def generate_docker_compose() -> dict:
    """生成 Docker Compose 配置"""
    # TODO: 实现这个函数
    # 返回格式应如下：
    # {
    #     "version": "3.8",
    #     "services": {
    #         "agent": {...},
    #         "redis": {...},
    #         "postgres": {...},
    #         "prometheus": {...},
    #     },
    #     "networks": {...},
    #     "volumes": {...},
    # }
    raise NotImplementedError("需要实现 Docker Compose 配置生成")


def main() -> None:
    """主函数"""
    print("=" * 60)
    print("练习题 1: Docker Compose 多服务编排")
    print("=" * 60)

    print("\n任务：")
    print("1. 创建 docker-compose.yml 文件")
    print("2. 配置 4 个服务：agent, redis, postgres, prometheus")
    print("3. agent 依赖 redis 和 postgres")
    print("4. 配置健康检查")
    print("5. 设置网络隔离")

    print("\n提示：")
    print("- agent 端口: 8000")
    print("- redis 端口: 6379")
    print("- postgres 端口: 5432, 默认数据库: agentdb")
    print("- prometheus 端口: 9090")
    print("- 使用自定义网络 agent-network")

    print("\n完成后运行以下命令测试：")
    print("  docker-compose config  # 验证配置")
    print("  docker-compose up -d   # 启动服务")
    print("  docker-compose ps      # 查看状态")


if __name__ == "__main__":
    main()
