from __future__ import annotations

import pytest

from providers import (
    AudioInput,
    ImageInput,
    MockSpeechProvider,
    MockVisionProvider,
    MultiModalAgent,
)


def test_vision_describe_returns_string() -> None:
    provider = MockVisionProvider()
    result = provider.describe(ImageInput(data=b"fake", format="png"))
    assert isinstance(result, str)
    assert len(result) > 20


def test_vision_analyze_returns_scene() -> None:
    provider = MockVisionProvider()
    result = provider.analyze(ImageInput(data=b"fake", format="png"))
    assert "scene" in result
    assert "objects" in result


def test_speech_transcribe_returns_string() -> None:
    provider = MockSpeechProvider()
    result = provider.transcribe(AudioInput(data=b"fake", format="wav"))
    assert isinstance(result, str)
    assert len(result) > 0


def test_speech_detect_language_returns_zh() -> None:
    provider = MockSpeechProvider()
    assert provider.detect_language(AudioInput(data=b"fake", format="wav")) == "zh"


def test_speech_detect_language_returns_unknown_for_empty_audio() -> None:
    provider = MockSpeechProvider()
    assert provider.detect_language(AudioInput(data=b"", format="wav")) == "unknown"


def test_vision_describe_includes_prompt_when_provided() -> None:
    provider = MockVisionProvider()
    result = provider.describe(ImageInput(data=b"fake", format="png"), prompt="请关注课堂场景")
    assert "请关注课堂场景" in result


def test_image_input_frozen() -> None:
    with pytest.raises(AttributeError):
        ImageInput(data=b"x", format="png").data = b"y"


def test_audio_input_frozen() -> None:
    with pytest.raises(AttributeError):
        AudioInput(data=b"x", format="wav").format = "mp3"


def test_agent_process_image() -> None:
    agent = MultiModalAgent(MockVisionProvider(), MockSpeechProvider())
    result = agent.process_image(ImageInput(data=b"fake", format="png"))
    assert "图片描述" in result


def test_agent_process_audio() -> None:
    agent = MultiModalAgent(MockVisionProvider(), MockSpeechProvider())
    result = agent.process_audio(AudioInput(data=b"fake", format="wav"))
    assert "今天" in result


def test_agent_process_both() -> None:
    agent = MultiModalAgent(MockVisionProvider(), MockSpeechProvider())
    result = agent.process_both(
        ImageInput(data=b"fake", format="png"),
        AudioInput(data=b"fake", format="wav"),
    )
    assert "image_description" in result
    assert "transcription" in result
