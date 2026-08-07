"""练习 1 参考答案: Dockerfile 校验。"""

from __future__ import annotations


def validate_dockerfile(text: str) -> list[str]:
    errors: list[str] = []
    required = ["FROM", "WORKDIR", "COPY"]
    for keyword in required:
        if keyword not in text:
            errors.append(f"missing {keyword}")
    if "CMD" not in text and "ENTRYPOINT" not in text:
        errors.append("missing CMD or ENTRYPOINT")
    return errors
