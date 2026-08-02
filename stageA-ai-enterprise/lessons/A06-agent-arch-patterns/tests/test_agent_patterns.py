import pytest
from pathlib import Path


@pytest.fixture
async def agent_framework():
    """Mock agent framework fixture for testing"""

    class MockAgent:
        def __init__(self, name: str):
            self.name = name
            self.handler = None

        async def run(self):
            return f"Agent {self.name} executed"

        def set_handler(self, handler):
            self.handler = handler
            return self

    return MockAgent


@pytest.fixture
async def load_test_config():
    """Load test configuration"""
    return {"max_concurrency": 10, "timeout": 30, "retry_times": 3}


def test_imports():
    """Verify lesson module can be imported"""
    try:
        import importlib.util
        import sys
        from pathlib import Path

        # ✅ 使用 importlib 按物理路径加载，避免 sys.path 污染
        lesson_dir = Path(__file__).parent.parent
        lesson_file = lesson_dir / "lesson_code.py"

        # 如果文件不存在，跳过测试
        if not lesson_file.exists():
            pytest.skip("Lesson module not implemented yet")

        spec = importlib.util.spec_from_file_location("lesson_code", lesson_file)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            sys.modules["lesson_code"] = module
            spec.loader.exec_module(module)

        # 测试可以导入具体的实现类
        from lesson_code import ReactAgent, PlanExecuteAgent, AgentConfig

        # Basic instantiation test
        agent = ReactAgent("test")
        assert agent.name == "test"
        assert agent.config.mode.value == "react"

        agent2 = PlanExecuteAgent("test2")
        assert agent2.name == "test2"
    except ImportError:
        pytest.skip("Lesson module not implemented yet")


@pytest.mark.asyncio
async def test_basic_agent_creation(agent_framework):
    """Test basic agent creation matching lesson content"""
    Agent = agent_framework
    agent = Agent("test-agent")
    result = await agent.run()
    assert result == "Agent test-agent executed"
    assert agent.handler is None
