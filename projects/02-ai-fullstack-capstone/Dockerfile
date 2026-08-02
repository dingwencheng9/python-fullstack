# ==============================================================================
# Stage 1: Build Stage（构建阶段）
# ==============================================================================
FROM python:3.13-slim AS builder

# 安装 uv（快速 Python 包管理器）
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# 设置工作目录
WORKDIR /app

# 复制项目依赖文件
COPY pyproject.toml ./

# 创建虚拟环境并安装依赖（仅生产依赖）
RUN uv venv /app/.venv && \
    uv pip install --no-cache-dir -r pyproject.toml

# ==============================================================================
# Stage 2: Runtime Stage（运行时阶段）
# ==============================================================================
FROM python:3.13-slim

# 安装运行时依赖（如果需要）
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 创建非 root 用户
RUN useradd -m -u 1000 appuser

# 设置工作目录
WORKDIR /app

# 从构建阶段复制虚拟环境
COPY --from=builder /app/.venv /app/.venv

# 复制应用代码
COPY app /app/app

# 创建数据目录
RUN mkdir -p /app/data && chown -R appuser:appuser /app

# 切换到非 root 用户
USER appuser

# 设置环境变量
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    APP_ENV=production

# 暴露端口
EXPOSE 8000

# 健康检查
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# 启动应用
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
