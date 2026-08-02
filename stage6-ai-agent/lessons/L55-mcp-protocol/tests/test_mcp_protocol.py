"""L56 MCP 协议测试。"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

LESSON_DIR = Path(__file__).parent.parent


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    # 关键：注册到 sys.modules，解决 dataclass 的 __module__ 查找问题
    sys.modules[name] = module
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module


def test_tool_server_register_and_call():
    mod = load_module(LESSON_DIR / "examples" / "tool_server.py", "tool_server")
    server = mod.ToolServer()
    server.register(
        mod.ToolSpec("echo", "回显", {"type": "object"}),
        lambda text: text,
    )
    result = server.call_tool(mod.ToolCall("echo", {"text": "hello"}))
    assert result.ok is True
    assert result.content == "hello"


def test_tool_server_unknown_tool():
    mod = load_module(LESSON_DIR / "examples" / "tool_server.py", "tool_server")
    server = mod.ToolServer()
    result = server.call_tool(mod.ToolCall("missing", {}))
    assert result.ok is False
    assert "unknown" in result.content


def test_list_tools():
    mod = load_module(LESSON_DIR / "examples" / "tool_server.py", "tool_server")
    server = mod.ToolServer()
    server.register(mod.ToolSpec("a", "A", {}), lambda: "A")
    server.register(mod.ToolSpec("b", "B", {}), lambda: "B")
    assert [tool.name for tool in server.list_tools()] == ["a", "b"]


def test_file_search_tool(tmp_path):
    mod = load_module(LESSON_DIR / "solutions" / "01_file_search_tool.py", "file_search")
    (tmp_path / "a.py").write_text("hello FastAPI")
    (tmp_path / "b.py").write_text("hello LangGraph")
    server = mod.FileSearchServer(tmp_path)
    result = server.search_files("FastAPI")
    assert "a.py" in result
    assert "b.py" not in result


def test_file_search_no_matches(tmp_path):
    mod = load_module(LESSON_DIR / "solutions" / "01_file_search_tool.py", "file_search")
    (tmp_path / "a.py").write_text("hello")
    server = mod.FileSearchServer(tmp_path)
    assert server.search_files("missing") == "no matches"


@pytest.mark.parametrize(
    "query,expected",
    [
        ("FastAPI", "a.py"),
        ("LangGraph", "b.py"),
        ("nothing", "no matches"),
    ],
)
def test_file_search_parametrized(tmp_path, query, expected):
    mod = load_module(LESSON_DIR / "solutions" / "01_file_search_tool.py", "file_search")
    (tmp_path / "a.py").write_text("FastAPI app")
    (tmp_path / "b.py").write_text("LangGraph agent")
    server = mod.FileSearchServer(tmp_path)
    assert expected in server.search_files(query)


def test_file_search_limit(tmp_path):
    mod = load_module(LESSON_DIR / "solutions" / "01_file_search_tool.py", "file_search")
    for i in range(30):
        (tmp_path / f"f{i}.py").write_text("match")
    server = mod.FileSearchServer(tmp_path)
    result = server.search_files("match")
    assert len(result.splitlines()) == 20
