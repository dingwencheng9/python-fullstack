from __future__ import annotations

import sys
from pathlib import Path

# Add parent directory to sys.path for imports (directory name has hyphen)
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from providers import (
    AudioInput,
    MockSpeechProvider,
    MockVisionProvider,
    MultiModalAgent,
)


def main() -> None:
    """音频转录示例。"""
    # 生成假的 WAV 字节（不需要是有效音频，Mock Provider 不会解析它）
    fake_wav_bytes = b"fake-wav-bytes-1234567890-abcdef"

    # 创建输入
    audio_input = AudioInput(data=fake_wav_bytes, format="wav")

    # 创建 Agent
    agent = MultiModalAgent(
        vision=MockVisionProvider(),
        speech=MockSpeechProvider(),
    )

    # 转录音频
    transcription = agent.process_audio(audio_input)
    print("音频转录:")
    print(f"  {transcription}")
    print()

    # 检测音频语言
    language = agent.speech.detect_language(audio_input)
    print("音频语言检测:")
    print(f"  检测到的语言: {language}")


if __name__ == "__main__":
    main()
