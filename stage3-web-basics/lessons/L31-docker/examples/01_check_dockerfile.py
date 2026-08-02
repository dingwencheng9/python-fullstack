"""L31 示例: Dockerfile 静态检查。

from __future__ import annotations

不需要本机安装 Docker，也能检查 Dockerfile 基础结构。
"""

from pathlib import Path


def check_dockerfile(path: str | Path) -> list[str]:
    """检查 Dockerfile 是否包含关键指令。"""
    text = Path(path).read_text()
    errors: list[str] = []
    for keyword in ["FROM", "WORKDIR", "COPY"]:
        if keyword not in text:
            errors.append(f"missing {keyword}")
    if "CMD" not in text and "ENTRYPOINT" not in text:
        errors.append("missing CMD or ENTRYPOINT")
    return errors


if __name__ == "__main__":
    dockerfile = Path(__file__).parent / "Dockerfile.fastapi"
    errors = check_dockerfile(dockerfile)
    print("Dockerfile OK" if not errors else f"Errors: {errors}")
