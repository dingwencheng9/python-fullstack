# ruff: noqa: F821
# 骨架代码：学生填空用教学模板，类型未定义为设计意图

"""

from __future__ import annotations

【骨架代码】健康检查路由

TODO: 按照注释提示，补全代码
"""

from __future__ import annotations

from fastapi import APIRouter

# TODO: 导入 HealthResponse 模型
# from ..models import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check() -> HealthResponse:
    """健康检查端点

    返回：
    - status: "ok"
    - timestamp: 当前时间戳
    - version: "0.1.0"
    """
    # TODO: 实现健康检查
    # ← 你的代码写在这里
