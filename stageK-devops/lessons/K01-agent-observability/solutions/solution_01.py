"""
练习题 1 参考解答: Docker Compose 多服务编排
"""

import yaml


def generate_docker_compose() -> dict:
    """生成 Docker Compose 配置"""
    return {
        "version": "3.8",
        "services": {
            "agent": {
                "build": {
                    "context": ".",
                    "dockerfile": "Dockerfile",
                },
                "ports": ["8000:8000"],
                "environment": {
                    "OPENAI_API_KEY": "${OPENAI_API_KEY}",
                    "DATABASE_URL": "postgresql://postgres:secret@postgres:5432/agentdb",
                    "REDIS_URL": "redis://redis:6379/0",
                },
                "depends_on": {
                    "redis": {"condition": "service_healthy"},
                    "postgres": {"condition": "service_healthy"},
                },
                "healthcheck": {
                    "test": ["CMD", "curl", "-f", "http://localhost:8000/health"],
                    "interval": "30s",
                    "timeout": "10s",
                    "retries": 3,
                    "start_period": "10s",
                },
                "networks": ["agent-network"],
            },
            "redis": {
                "image": "redis:7-alpine",
                "ports": ["6379:6379"],
                "healthcheck": {
                    "test": ["CMD", "redis-cli", "ping"],
                    "interval": "10s",
                    "timeout": "5s",
                    "retries": 3,
                },
                "networks": ["agent-network"],
            },
            "postgres": {
                "image": "postgres:16-alpine",
                "ports": ["5432:5432"],
                "environment": {
                    "POSTGRES_DB": "agentdb",
                    "POSTGRES_USER": "postgres",
                    "POSTGRES_PASSWORD": "secret",
                },
                "volumes": ["postgres-data:/var/lib/postgresql/data"],
                "healthcheck": {
                    "test": ["CMD-SHELL", "pg_isready -U postgres"],
                    "interval": "10s",
                    "timeout": "5s",
                    "retries": 3,
                },
                "networks": ["agent-network"],
            },
            "prometheus": {
                "image": "prom/prometheus:latest",
                "ports": ["9090:9090"],
                "volumes": [
                    "./prometheus.yml:/etc/prometheus/prometheus.yml",
                    "prometheus-data:/prometheus",
                ],
                "command": [
                    "--config.file=/etc/prometheus/prometheus.yml",
                    "--storage.tsdb.path=/prometheus",
                    "--web.enable-lifecycle",
                ],
                "networks": ["agent-network"],
            },
            "grafana": {
                "image": "grafana/grafana:latest",
                "ports": ["3000:3000"],
                "environment": {
                    "GF_SECURITY_ADMIN_USER": "admin",
                    "GF_SECURITY_ADMIN_PASSWORD": "admin",
                },
                "volumes": ["grafana-data:/var/lib/grafana"],
                "depends_on": ["prometheus"],
                "networks": ["agent-network"],
            },
        },
        "networks": {
            "agent-network": {
                "driver": "bridge",
            },
        },
        "volumes": {
            "postgres-data": None,
            "prometheus-data": None,
            "grafana-data": None,
        },
    }


def main() -> None:
    """主函数"""
    print("=" * 60)
    print("练习题 1 参考解答: Docker Compose 多服务编排")
    print("=" * 60)

    # 生成配置
    config = generate_docker_compose()

    # 输出 YAML
    print("\n--- Docker Compose 配置 ---")
    print(yaml.dump(config, default_flow_style=False, sort_keys=False))

    # 验证
    print("\n" + "=" * 60)
    print("验证")
    print("=" * 60)

    assert "services" in config, "应该有 services 配置"
    assert set(config["services"].keys()) == {"agent", "redis", "postgres", "prometheus", "grafana"}
    assert config["services"]["agent"]["depends_on"]["redis"]["condition"] == "service_healthy"
    assert config["services"]["agent"]["depends_on"]["postgres"]["condition"] == "service_healthy"
    assert "agent-network" in config["networks"]

    print("✅ 配置验证通过!")


if __name__ == "__main__":
    main()
