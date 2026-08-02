# mypy: disable-error-code="untyped-decorator"
"""健康检查路由。

from __future__ import annotations

注：FastAPI 装饰器在 mypy strict 下被视为 untyped（上游已知问题），
这里文件级关闭 ``untyped-decorator`` 规则即可，其他 strict 检查保留。
"""

from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/ready")
async def ready() -> dict[str, str]:
    return {"status": "ready"}
