"""全局异常处理器。

from __future__ import annotations

统一的异常响应格式，防止内部错误泄漏到客户端。
"""

from __future__ import annotations

from typing import Any

from fastapi import HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.logging_config import get_logger

logger = get_logger(__name__)


class ErrorResponse:
    """标准化错误响应结构。"""

    def __init__(self, code: str, message: str, details: Any = None) -> None:
        self.code = code
        self.message = message
        self.details = details

    def to_dict(self) -> dict[str, Any]:
        """转换为字典格式。"""
        response: dict[str, Any] = {
            "success": False,
            "error": {
                "code": self.code,
                "message": self.message,
            },
        }
        if self.details is not None:
            response["error"]["details"] = self.details
        return response


async def http_exception_handler(
    request: Request,
    exc: HTTPException,  # noqa: ARG001
) -> JSONResponse:
    """处理 HTTPException（FastAPI 标准异常）。"""
    error = ErrorResponse(
        code=f"HTTP_{exc.status_code}",
        message=str(exc.detail),
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=error.to_dict(),
    )


async def validation_exception_handler(
    request: Request, exc: RequestValidationError | ValidationError
) -> JSONResponse:
    """处理 Pydantic 验证错误。"""
    # 提取验证错误详情
    errors = exc.errors() if hasattr(exc, "errors") else []
    error = ErrorResponse(
        code="VALIDATION_ERROR",
        message="请求数据验证失败",
        details=errors,
    )

    # 结构化日志记录验证错误
    logger.error(
        "Validation error",
        method=request.method,
        url=str(request.url),
        errors=errors,
    )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=error.to_dict(),
    )


async def generic_exception_handler(
    request: Request,
    exc: Exception,  # noqa: ARG001
) -> JSONResponse:
    """处理所有未捕获的异常（最后防线）。"""
    # 结构化日志记录完整异常堆栈
    logger.exception(
        "Unhandled exception",
        method=request.method,
        url=str(request.url),
        exc_type=type(exc).__name__,
    )

    # 返回安全的错误响应（不暴露内部细节）
    error = ErrorResponse(
        code="INTERNAL_ERROR",
        message="服务器内部错误，请稍后重试",
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error.to_dict(),
    )


def register_exception_handlers(app: Any) -> None:
    """注册所有异常处理器到 FastAPI 应用。

    Args:
        app: FastAPI 应用实例
    """
    # HTTPException（FastAPI 标准异常）
    app.add_exception_handler(HTTPException, http_exception_handler)

    # Pydantic 验证错误
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(ValidationError, validation_exception_handler)

    # 兜底：所有未捕获异常
    app.add_exception_handler(Exception, generic_exception_handler)
