"""

from __future__ import annotations

测试基础功能

验证 freelance-demo 的基础结构和功能。
"""

import pytest


def test_project_structure(project_root):
    """测试项目结构完整性"""
    # 验证关键目录和文件存在
    assert (project_root / "README.md").exists()
    assert (project_root / "pyproject.toml").exists()

    # 验证可能的模板目录
    possible_dirs = [
        project_root / "templates",
        project_root / "demo",
        project_root / "examples",
    ]

    # 至少有一个目录存在
    assert any(d.exists() and d.is_dir() for d in possible_dirs), "应该至少有一个内容目录"


def test_readme_content(project_root):
    """测试 README 包含必要信息"""
    readme = project_root / "README.md"
    content = readme.read_text()

    # README 应该不是空的
    assert len(content) > 100, "README 内容应该充实"

    # 应该包含项目相关关键词
    keywords = ["freelance", "demo", "工具", "toolkit"]
    assert any(kw.lower() in content.lower() for kw in keywords), "README 应包含项目相关关键词"


def test_pyproject_toml(project_root):
    """测试 pyproject.toml 配置正确"""
    pyproject = project_root / "pyproject.toml"
    content = pyproject.read_text()

    # 验证包含必要字段
    assert 'name = "freelance-demo"' in content
    assert 'requires-python = ">=3.13"' in content
    assert "[build-system]" in content


def test_output_directory_creation(output_dir):
    """测试输出目录创建"""
    # fixture 已经创建了目录
    assert output_dir.exists()
    assert output_dir.is_dir()

    # 可以在输出目录创建文件
    test_file = output_dir / "test.txt"
    test_file.write_text("test content")

    assert test_file.exists()
    assert test_file.read_text() == "test content"


@pytest.mark.parametrize(
    "filename",
    [
        "quote.txt",
        "contract.txt",
        "faq.md",
        "playbook.md",
    ],
)
def test_demo_file_generation(output_dir, filename):
    """测试演示文件生成（占位符测试）"""
    # 这是一个占位符测试，展示如何测试文件生成
    # 实际项目应该有具体的生成逻辑

    demo_file = output_dir / filename

    # 模拟文件生成
    demo_file.write_text(f"# {filename}\n\nDemo content")

    assert demo_file.exists()
    content = demo_file.read_text()
    assert filename in content or "Demo" in content
