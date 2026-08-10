"""L46 WebSocket 高级应用 - 测试配置"""

import pytest

# 确保 fastapi 已安装（WebSocket 模块依赖）
pytest.importorskip("fastapi", reason="需要 FastAPI 来测试 WebSocket")
pytest.importorskip("uvicorn", reason="需要 uvicorn 来测试 WebSocket")
