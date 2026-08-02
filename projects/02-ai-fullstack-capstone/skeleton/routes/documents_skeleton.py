# ruff: noqa: F821
# 骨架代码：学生填空用教学模板，类型未定义为设计意图

"""

from __future__ import annotations

【骨架代码】文档导入路由

TODO: 按照注释提示，补全代码
"""

from __future__ import annotations

from fastapi import APIRouter

# TODO: 导入模型和服务
# from ...models import Document, DocumentUploadRequest
# from ...services.storage import DocumentStorage

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/")
def upload_document(request: DocumentUploadRequest) -> Document:
    """上传文档

    步骤：
    1. 验证内容不为空
    2. 生成文档ID
    3. 创建 Document 对象
    4. 存储到文档存储
    5. 返回文档对象
    """
    # TODO: 实现文档上传
    # 提示：使用 uuid.uuid4() 生成文档ID
    # ← 你的代码写在这里


@router.get("/")
def list_documents() -> list[Document]:
    """列出所有文档

    返回存储中的所有文档列表
    """
    # TODO: 实现列表查询
    # ← 你的代码写在这里


@router.get("/{doc_id}")
def get_document(doc_id: str) -> Document:
    """获取单个文档

    如果文档不存在，返回 404
    """
    # TODO: 实现文档查询
    # ← 你的代码写在这里


@router.delete("/{doc_id}")
def delete_document(doc_id: str) -> dict:
    """删除文档

    如果文档不存在，返回 404
    返回: {"status": "ok"}
    """
    # TODO: 实现文档删除
    # ← 你的代码写在这里
