"""
示例 1: Docker 多阶段构建与健康检查

展示如何创建生产级的 Dockerfile 和健康检查端点。
"""

from dataclasses import dataclass


@dataclass
class HealthStatus:
    """健康状态"""

    status: str
    version: str
    checks: dict[str, bool]


class AgentServer:
    """模拟 Agent 服务器"""

    def __init__(self):
        self.version = "1.0.0"
        self.initialized = True

    def health_check(self) -> HealthStatus:
        """健康检查"""
        return HealthStatus(
            status="healthy",
            version=self.version,
            checks={
                "database": True,
                "cache": True,
                "llm": True,
            },
        )

    def readiness_check(self) -> dict:
        """就绪检查"""
        health = self.health_check()
        all_ready = all(health.checks.values())

        return {
            "ready": all_ready,
            "status_code": 200 if all_ready else 503,
            "checks": health.checks,
        }


def generate_dockerfile() -> str:
    """生成 Dockerfile 内容"""
    return """# Dockerfile - Agent 多阶段构建

# ============== 阶段 1: 构建 ==============
FROM python:3.13-slim AS builder

WORKDIR /app

# 安装 uv
RUN pip install uv

# 复制依赖文件
COPY pyproject.toml ./

# 使用 uv 安装依赖（仅安装生产依赖）
RUN uv sync --frozen --no-dev

# ============== 阶段 2: 运行 ==============
FROM python:3.13-slim AS runner

WORKDIR /app

# 从构建阶段复制依赖
COPY --from=builder /app/.venv /app/.venv

# 复制应用代码
COPY agent/ ./agent/
COPY pyproject.toml ./

# 设置环境变量
ENV PATH="/app/.venv/bin:$PATH" \\
    PYTHONUNBUFFERED=1

# 非 root 用户运行
RUN useradd -m -u 1000 appuser && \\
    chown -R appuser:appuser /app
USER appuser

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \\
    CMD python -c "import requests; requests.get(\'http://localhost:8000/health\')"

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["python", "-m", "agent.server"]
"""


def main() -> None:
    """主函数"""
    print("=" * 60)
    print("Docker 多阶段构建示例")
    print("=" * 60)

    # 创建服务器实例
    server = AgentServer()

    # 健康检查
    print("\n--- 健康检查 ---")
    health = server.health_check()
    print(f"状态: {health.status}")
    print(f"版本: {health.version}")
    print("检查项:")
    for name, status in health.checks.items():
        print(f"  - {name}: {'✅' if status else '❌'}")

    # 就绪检查
    print("\n--- 就绪检查 ---")
    ready = server.readiness_check()
    print(f"就绪状态: {'✅' if ready['ready'] else '❌'}")
    print(f"HTTP 状态码: {ready['status_code']}")

    # Dockerfile 内容
    print("\n--- Dockerfile 内容 ---")
    dockerfile = generate_dockerfile()
    print(dockerfile)

    # 验证
    print("\n" + "=" * 60)
    print("验证")
    print("=" * 60)
    assert health.status == "healthy", "健康检查应该返回 healthy"
    assert all(health.checks.values()), "所有检查项应该为 True"
    print("✅ 健康检查验证通过!")
    print("✅ Dockerfile 生成验证通过!")


if __name__ == "__main__":
    main()
