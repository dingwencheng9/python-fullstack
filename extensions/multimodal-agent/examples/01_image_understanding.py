from __future__ import annotations

import sys
from pathlib import Path

# Add parent directory to sys.path for imports (directory name has hyphen)
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from providers import (
    ImageInput,
    MockSpeechProvider,
    MockVisionProvider,
    MultiModalAgent,
)


def main() -> None:
    """图片理解示例。"""
    # 生成假的 PNG 字节（不需要是有效图片，Mock Provider 不会解析它）
    fake_png_bytes = b"fake-png-bytes-1234567890"

    # 创建输入
    image_input = ImageInput(data=fake_png_bytes, format="png")

    # 创建 Agent
    agent = MultiModalAgent(
        vision=MockVisionProvider(),
        speech=MockSpeechProvider(),
    )

    # 描述图片
    description = agent.process_image(image_input)
    print("图片描述:")
    print(f"  {description}")
    print()

    # 带提示的描述
    prompted_description = agent.process_image(image_input, question="图片里有几个人？")
    print("带提示的图片描述:")
    print(f"  {prompted_description}")
    print()

    # 分析图片（结构化信息）
    analysis = agent.vision.analyze(image_input)
    print("图片分析:")
    for key, value in analysis.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
