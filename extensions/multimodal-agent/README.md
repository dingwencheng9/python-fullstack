# 多模态 Agent 扩展：图片理解 + 语音转写

> 教学型 Mock 多模态输入扩展。无需 API Key，全部本地可运行。

## 适合人群

- 已完成 Stage 5 Agent 课程（L52-L60）
- 想理解多模态 Agent 的架构设计
- 想在未来集成 OpenAI Vision / Whisper / CLIP 等真实 Provider

## 学习目标

完成本扩展后，你将能够：

1. 用协议/抽象类定义多模态 Provider 边界
2. 用 Mock Provider 先把架构跑通
3. 理解图片输入与语音输入的统一封装方式
4. 用 `MultiModalAgent` 组合 Vision + Speech 能力
5. 知道如何替换为真实 API Provider

---

## 目录结构

```text
extensions/multimodal-agent/
├── README.md
├── providers.py              # 数据模型 + Provider 协议 + Mock 实现 + Agent
├── examples/
│   ├── 01_image_understanding.py
│   ├── 02_audio_transcription.py
│   └── 03_multimodal_agent.py
└── tests/
    ├── conftest.py
    └── test_multimodal.py
```

---

## 架构

```text
ImageInput(bytes, format) ──▶ VisionProvider.describe/analyze ─┐
                                                               ├──▶ MultiModalAgent
AudioInput(bytes, format) ──▶ SpeechProvider.transcribe/lang ──┘
```

核心接口：

- `VisionProvider.describe(image, prompt)`：图片转文字描述
- `VisionProvider.analyze(image)`：图片转结构化信息
- `SpeechProvider.transcribe(audio)`：音频转文字
- `SpeechProvider.detect_language(audio)`：语音语言检测
- `MultiModalAgent.process_both(image, audio)`：聚合图片和语音结果

---

## 快速开始

### 运行测试

```bash
uv run pytest extensions/multimodal-agent/tests/ -v
```

### 图片理解示例

```bash
uv run python extensions/multimodal-agent/examples/01_image_understanding.py
```

输出示例：

```text
=== 图片理解示例 ===
描述：图片描述（34 字节）：一个晴朗的下午，很多学生正在上课。
分析：{'scene': '教室', 'objects': ['黑板', '书桌'], 'estimated_size': 34}
```

### 语音转写示例

```bash
uv run python extensions/multimodal-agent/examples/02_audio_transcription.py
```

输出示例：

```text
=== 语音转写示例 ===
转录：今天天气真好。（音频大小：34 字节）
语言：zh
```

### 组合示例

```bash
uv run python extensions/multimodal-agent/examples/03_multimodal_agent.py
```

---

## 为什么先用 Mock Provider？

真实多模态 API 会引入：

- API Key 管理
- 网络失败与重试
- 模型响应不稳定
- 费用控制
- 测试时的 mock 复杂度

本扩展先用 Mock Provider 固定输出，让你先掌握**架构边界**：

```python
agent = MultiModalAgent(MockVisionProvider(), MockSpeechProvider())
result = agent.process_both(image, audio)
```

未来替换真实 Provider 时，只需要实现同样的协议。

---

## 替换为真实 OpenAI Vision（示意）

```python
class OpenAIVisionProvider(VisionProvider):
    def __init__(self, client):
        self.client = client

    def describe(self, image: ImageInput, prompt: str | None = None) -> str:
        # 1. base64 编码 image.data
        # 2. 调用 chat.completions.create(model="gpt-4o", ...)
        # 3. 返回 response.choices[0].message.content
        raise NotImplementedError("真实 Provider 留给生产扩展")

    def analyze(self, image: ImageInput) -> dict[str, object]:
        raise NotImplementedError("真实 Provider 留给生产扩展")
```

## 替换为真实 Whisper（示意）

```python
class OpenAISpeechProvider(SpeechProvider):
    def __init__(self, client):
        self.client = client

    def transcribe(self, audio: AudioInput) -> str:
        # 1. 把 audio.data 写入临时文件或 BytesIO
        # 2. 调用 audio.transcriptions.create(model="whisper-1", ...)
        # 3. 返回 transcription.text
        raise NotImplementedError("真实 Provider 留给生产扩展")

    def detect_language(self, audio: AudioInput) -> str:
        return "unknown"
```

---

## 测试覆盖

当前测试覆盖：

- MockVisionProvider.describe
- MockVisionProvider.analyze
- MockSpeechProvider.transcribe
- MockSpeechProvider.detect_language
- MultiModalAgent.process_image
- MultiModalAgent.process_audio
- MultiModalAgent.process_both
- ImageInput / AudioInput frozen dataclass 不可变
- prompt 分支和 empty audio 分支

```bash
uv run pytest extensions/multimodal-agent/tests/ --no-cov -q
# 11 passed
```

---

## 后续扩展方向

1. `OpenAIVisionProvider`：接入 GPT-4o / GPT-4.1 Vision
2. `OpenAISpeechProvider`：接入 Whisper
3. `LocalCLIPVisionProvider`：本地 CLIP embedding
4. `LocalWhisperProvider`：faster-whisper 本地转写
5. 项目 2 集成：文档 RAG + 图片 RAG + 语音问答

---

## 注意

这不是生产级多模态实现，而是**教学级架构骨架**：

- ✅ 能跑
- ✅ 能测
- ✅ 无 API Key
- ✅ Provider 边界清楚
- ❌ 不调用真实模型
- ❌ 不做图片 OCR / 音频 VAD / 多模态 embedding
