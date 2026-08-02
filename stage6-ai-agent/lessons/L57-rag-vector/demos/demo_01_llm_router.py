"""Demo 01: 异步云本双轨路由演示

from __future__ import annotations

本演示展示如何使用 LLMRouter 在本地（Ollama + Qwen2.5）和云端（OpenAI）
模式之间进行零成本切换，并演示 FastAPI 异步流式响应（SSE）的实现。

核心要点：
1. 本地开发环境使用 LOCAL 模式（零 API 费用）
2. 生产环境使用 CLOUD 模式（高质量响应）
3. 流式响应支持打字机效果
4. 异步流安全处理，防止连接泄漏

运行方式：
    python demo_01_llm_router.py
"""

import asyncio

from stage4_data_intelligence.core.llm_router import LLMRouter, Message


async def demo_basic_chat() -> None:
    """演示基础聊天功能（非流式）"""
    print("=" * 60)
    print("Demo 1.1: 基础聊天功能")
    print("=" * 60)

    # 初始化路由器（LOCAL 模式）
    router = LLMRouter(mode="LOCAL")
    print(f"✅ 路由器已初始化: {router.get_status()}")

    # 准备消息
    messages: list[Message] = [
        {"role": "system", "content": "你是一个有帮助的 AI 助手。"},
        {"role": "user", "content": "请用一句话介绍 Python 3.12 的新特性。"},
    ]

    try:
        print("\n🤖 正在生成响应...")
        response = await router.chat(messages)
        print(f"\n✅ 响应: {response}")
    except Exception as e:
        print(f"❌ 错误: {type(e).__name__}: {e}")


async def demo_streaming_chat() -> None:
    """演示流式聊天功能（打字机效果）"""
    print("\n" + "=" * 60)
    print("Demo 1.2: 流式聊天（打字机效果）")
    print("=" * 60)

    router = LLMRouter(mode="LOCAL")

    messages: list[Message] = [
        {"role": "user", "content": "请列举 3 个 Python 异步编程的最佳实践。"},
    ]

    try:
        print("\n🤖 流式响应:")
        print("-" * 60)

        # 异步流式迭代，支持取消
        async for chunk in router.chat_stream(messages):
            print(chunk, end="", flush=True)

        print("\n" + "-" * 60)
        print("✅ 流式响应完成")

    except asyncio.CancelledError:
        # 关键：捕获取消异常，防止连接泄漏
        print("\n⚠️  流式响应被取消")
        raise  # 重新抛出，允许上层处理
    except Exception as e:
        print(f"\n❌ 错误: {type(e).__name__}: {e}")


async def demo_mode_switching() -> None:
    """演示运行时模式切换"""
    print("\n" + "=" * 60)
    print("Demo 1.3: 运行时模式切换")
    print("=" * 60)

    router = LLMRouter(mode="LOCAL")
    print(f"✅ 初始模式: {router.get_status()}")

    # 注意：切换到 CLOUD 模式需要设置 OPENAI_API_KEY 环境变量
    print("\n⚠️  切换到 CLOUD 模式需要设置 OPENAI_API_KEY 环境变量")
    print("示例: export OPENAI_API_KEY='sk-...'")

    # 尝试切换（可能失败）
    try:
        router.switch_mode("CLOUD")
        print(f"✅ 切换成功: {router.get_status()}")

        # 测试云端调用
        messages: list[Message] = [{"role": "user", "content": "Hello!"}]
        response = await router.chat(messages)
        print(f"✅ 云端响应: {response}")

    except OSError as e:
        print(f"❌ 切换失败: {e}")
        print("💡 提示: 开发环境可以只使用 LOCAL 模式")


async def demo_error_handling() -> None:
    """演示错误处理最佳实践"""
    print("\n" + "=" * 60)
    print("Demo 1.4: 错误处理最佳实践")
    print("=" * 60)

    router = LLMRouter(mode="LOCAL")

    # 测试空消息列表
    try:
        print("\n🧪 测试 1: 空消息列表")
        response = await router.chat([])
        print(f"✅ 响应: {response}")
    except Exception as e:
        print(f"⚠️  捕获异常: {type(e).__name__}: {e}")

    # 测试无效消息格式（演示类型安全）
    print("\n🧪 测试 2: 类型安全演示")
    print("✅ TypedDict 确保消息格式正确，编译时检查")


async def demo_fastapi_integration() -> None:
    """演示 FastAPI 集成示例（伪代码）"""
    print("\n" + "=" * 60)
    print("Demo 1.5: FastAPI SSE 流式响应集成（伪代码）")
    print("=" * 60)

    code = '''
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import asyncio

app = FastAPI()
router = LLMRouter(mode="LOCAL")

@app.post("/chat/stream")
async def chat_stream(messages: list[Message]):
    """
    流式聊天端点（SSE 协议）

    关键点：
    1. 使用 StreamingResponse
    2. 设置正确的 media_type="text/event-stream"
    3. 异常处理防止连接泄漏
    """
    async def event_generator():
        try:
            async for chunk in router.chat_stream(messages):
                # SSE 格式：data: {content}\\n\\n
                yield f"data: {chunk}\\n\\n"

            # 发送结束标志
            yield "data: [DONE]\\n\\n"

        except asyncio.CancelledError:
            # 浏览器断开连接时触发
            print("⚠️  客户端断开连接")
            raise
        except Exception as e:
            # 发送错误信息
            yield f"data: [ERROR] {str(e)}\\n\\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # 禁用 Nginx 缓冲
        }
    )
'''
    print(code)
    print("\n💡 提示: 完整示例请参考 P4 智能知识库项目")


async def main() -> None:
    """主函数：运行所有演示"""
    print("\n" + "🚀" * 30)
    print("L17 Demo 01: 异步云本双轨路由演示")
    print("🚀" * 30 + "\n")

    # 运行所有演示
    await demo_basic_chat()
    await demo_streaming_chat()
    await demo_mode_switching()
    await demo_error_handling()
    await demo_fastapi_integration()

    print("\n" + "✅" * 30)
    print("所有演示完成！")
    print("✅" * 30 + "\n")

    # 关键学习点总结
    print("📚 关键学习点:")
    print("=" * 60)
    print("1. ✅ LLMRouter 支持 LOCAL/CLOUD 零成本切换")
    print("2. ✅ 流式响应需要正确处理 asyncio.CancelledError")
    print("3. ✅ FastAPI SSE 流式响应使用 StreamingResponse")
    print("4. ✅ 类型安全：使用 TypedDict 定义消息格式")
    print("5. ✅ 异步上下文管理器防止连接泄漏")
    print("=" * 60)


if __name__ == "__main__":
    # 运行异步主函数
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  程序被用户中断")
    except Exception as e:
        print(f"\n\n❌ 未捕获的异常: {type(e).__name__}: {e}")
        raise
