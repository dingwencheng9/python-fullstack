from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, override


@dataclass(frozen=True)
class ImageInput:
    """图像输入数据。"""

    data: bytes
    format: str


@dataclass(frozen=True)
class AudioInput:
    """音频输入数据。"""

    data: bytes
    format: str


class VisionProvider(ABC):
    """图片理解 Provider 协议。"""

    @abstractmethod
    def describe(self, image: ImageInput, prompt: str | None = None) -> str:
        """描述图片内容。"""

    @abstractmethod
    def analyze(self, image: ImageInput) -> dict[str, Any]:
        """分析图片，返回结构化信息。"""


class SpeechProvider(ABC):
    """语音 Provider 协议。"""

    @abstractmethod
    def transcribe(self, audio: AudioInput) -> str:
        """转写音频为文字。"""

    @abstractmethod
    def detect_language(self, audio: AudioInput) -> str:
        """检测音频语言。"""


class MockVisionProvider(VisionProvider):
    """Mock 图片理解 Provider。"""

    @override
    def describe(self, image: ImageInput, prompt: str | None = None) -> str:
        base = f"图片描述（{len(image.data)} 字节）：一个晴朗的下午，很多学生正在上课。"
        if prompt:
            return f"{base}（提示：{prompt}）"
        return base

    @override
    def analyze(self, image: ImageInput) -> dict[str, Any]:
        return {"scene": "教室", "objects": ["黑板", "书桌"], "estimated_size": len(image.data)}


class MockSpeechProvider(SpeechProvider):
    """Mock 语音 Provider。"""

    @override
    def transcribe(self, audio: AudioInput) -> str:
        return f"今天天气真好。（音频大小：{len(audio.data)} 字节）"

    @override
    def detect_language(self, audio: AudioInput) -> str:
        # 简单模拟：基于数据大小决定返回值（使用参数）
        if len(audio.data) > 0:
            return "zh"
        return "unknown"


class MultiModalAgent:
    """多模态 Agent — 聚合 Vision + Speech Provider。"""

    def __init__(self, vision: VisionProvider, speech: SpeechProvider) -> None:
        self.vision = vision
        self.speech = speech

    def process_image(self, image: ImageInput, question: str | None = None) -> str:
        return self.vision.describe(image, question)

    def process_audio(self, audio: AudioInput) -> str:
        return self.speech.transcribe(audio)

    def process_both(self, image: ImageInput, audio: AudioInput) -> dict[str, Any]:
        return {
            "image_description": self.vision.describe(image),
            "transcription": self.speech.transcribe(audio),
        }
