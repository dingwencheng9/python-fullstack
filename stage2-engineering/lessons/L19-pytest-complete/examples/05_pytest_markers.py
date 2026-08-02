"""L17 示例 5：pytest markers — 慢速测试与集成测试标记与 CI 分层运行。

本示例演示：
1. 如何定义自定义 markers（slow, integration, smoke）
2. 如何在 pytest.ini 中注册 markers
3. 如何在 CI 中分层运行不同类型的测试
"""

from __future__ import annotations

import time

import pytest

# === Part 1: 自定义 Markers ===


def slow_operation() -> float:
    """模拟耗时操作"""
    time.sleep(0.1)  # 模拟 100ms 延迟
    return 42.0


def external_api_call() -> dict:
    """模拟外部 API 调用"""
    time.sleep(0.05)
    return {"status": "ok", "data": [1, 2, 3]}


# === Part 2: 不同类型的测试标记 ===


@pytest.mark.unit
def test_basic_arithmetic() -> None:
    """单元测试：基础算术运算 — 快速，不依赖外部"""
    assert 1 + 1 == 2
    assert 10 * 5 == 50


@pytest.mark.unit
def test_string_operations() -> None:
    """单元测试：字符串操作"""
    text = "hello world"
    assert text.upper() == "HELLO WORLD"
    assert text.split() == ["hello", "world"]


@pytest.mark.smoke
def test_critical_path() -> None:
    """冒烟测试：关键路径快速验证"""
    # 这类测试覆盖系统最核心的功能
    # 应该始终快速通过，任何失败都是紧急的
    assert True


@pytest.mark.smoke
def test_health_check() -> None:
    """冒烟测试：健康检查"""
    result = slow_operation()
    assert result > 0


@pytest.mark.slow
def test_complex_calculation() -> None:
    """慢速测试：复杂计算（>1 秒）"""
    # 使用 pytest.mark.slow 标记耗时测试
    # 本地开发时可以跳过，CI 中可以并行运行
    time.sleep(0.15)  # 模拟更长的计算
    result = slow_operation()
    assert result == 42.0


@pytest.mark.integration
def test_database_connection() -> None:
    """集成测试：数据库连接"""
    # 集成测试依赖外部服务（数据库、API、文件系统）
    # 应该在隔离环境中运行，或者使用 mock
    pytest.skip("需要数据库环境")  # 实际项目中会真实连接


@pytest.mark.integration
def test_external_api() -> None:
    """集成测试：外部 API 调用"""
    # 依赖真实网络，可能失败或超时
    result = external_api_call()
    assert result["status"] == "ok"


# === Part 3: 组合 Markers ===


@pytest.mark.slow
@pytest.mark.integration
def test_end_to_end_workflow() -> None:
    """端到端测试：既慢又依赖外部服务"""
    time.sleep(0.1)
    data = external_api_call()
    assert len(data["data"]) > 0


# === Part 4: 参数化 + Markers ===


@pytest.mark.unit
@pytest.mark.parametrize(
    "input_val,expected",
    [
        (1, 1),
        (2, 4),
        (3, 9),
        (4, 16),
    ],
)
def test_square_values(input_val: int, expected: int) -> None:
    """参数化单元测试：平方运算"""
    assert input_val**2 == expected


# === Part 5: Fixtures 与 Markers 结合 ===


@pytest.fixture
def mock_data() -> dict:
    """模拟数据 fixture"""
    return {"users": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]}


@pytest.mark.integration
def test_user_service(mock_data: dict) -> None:
    """集成测试：使用 mock 数据"""
    # 集成测试也可以使用 mock 数据减少外部依赖
    assert len(mock_data["users"]) == 2


# === Part 6: 跳过条件 ===


@pytest.mark.skipif(
    True,  # 实际项目中可能是条件判断
    reason="功能开发中",
)
def test_future_feature() -> None:
    """尚未实现的功能测试"""
    pass


# === Part 7: 演示 Marker 过滤 ===


def test_marker_demos() -> None:
    """元测试：展示所有已注册的 markers"""
    print("\n已注册的 markers：")
    print("  - unit: 单元测试，快速，不依赖外部")
    print("  - smoke: 冒烟测试，关键路径")
    print("  - slow: 慢速测试，>1 秒")
    print("  - integration: 集成测试，依赖外部服务")
    assert True


# === 运行指南 ===

"""
## 如何运行不同类型的测试

### 本地开发（快速反馈）

# 只运行单元测试和冒烟测试（跳过慢速和集成测试）
uv run pytest tests/ -m "not slow and not integration" -q

# 只运行冒烟测试
uv run pytest tests/ -m smoke -q

# 只运行单元测试
uv run pytest tests/ -m unit -q


### 本地完整测试（包括慢速）

# 运行所有测试，包括慢速测试
uv run pytest tests/ -m "not integration" -q

# 运行所有测试
uv run pytest tests/ -q


### CI 分层运行

# Stage 1: 快速冒烟测试（< 1 分钟）
uv run pytest tests/ -m "smoke or unit" -q --tb=short

# Stage 2: 完整单元测试（< 5 分钟）
uv run pytest tests/ -m "not integration and not slow" -q --tb=short

# Stage 3: 包含集成测试（< 15 分钟）
uv run pytest tests/ -m "not slow" -q --tb=short

# Stage 4: 完整测试包括慢速测试（< 30 分钟）
uv run pytest tests/ -q --tb=short


### 并行运行加速

# 安装 pytest-xdist 后并行运行
uv run pytest tests/ -n auto -q

# 只并行运行快速测试
uv run pytest tests/ -m "not slow" -n auto -q
"""
