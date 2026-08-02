from __future__ import annotations

import sys
from pathlib import Path

# Add parent directory to sys.path for imports (directory name has hyphen)
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from providers import (
    AudioInput,
    ImageInput,
    MockSpeechProvider,
    MockVisionProvider,
    MultiModalAgent,
)


def main() -> None:
    """多模态 Agent 综合示例：同时处理图片和音频。"""
    # 生成假数据
    fake_png_bytes = b"fake-png-bytes-for-multimodal-test"
    fake_wav_bytes = b"fake-wav-bytes-for-multimodal-test"

    # 创建输入
    image_input = ImageInput(data=fake_png_bytes, format="png")
    audio_input = AudioInput(data=fake_wav_bytes, format="wav")

    # 创建 Agent
    agent = MultiModalAgent(
        vision=MockVisionProvider(),
        speech=MockSpeechProvider(),
    )

    # 同时处理图片和音频
    print("=== 多模态综合处理 ===")
    result = agent.process_both(image_input, audio_input)
    print()

    # 打印结果
    print("返回结果的键:")
    for key in result:
        print(f"  - {key}")
    print()

    print("返回结果的值:")
    for key, value in result.items():
        print(f"  {key}:")
        print(f"    {value}")
    print()

    print("=== 成功完成多模态综合处理 ===")


if __name__ == "__main__":
    main()
