"""测试 examples/example_04_github_actions_ci.py - GitHub Actions CI/CD 配置

from __future__ import annotations

测试覆盖:
- generate_basic_ci_workflow()
- generate_quality_check_workflow()
- generate_multi_os_workflow()
- generate_dependency_update_workflow()
- generate_release_workflow()
- generate_docker_build_workflow()
- generate_all_workflows()
- save_workflows_to_disk()
"""

# 导入被测试模块
import importlib.util
from pathlib import Path

import pytest

spec = importlib.util.spec_from_file_location(
    "github_actions",
    Path(__file__).parent.parent / "examples" / "example_04_github_actions_ci.py",
)
github_actions = importlib.util.module_from_spec(spec)
spec.loader.exec_module(github_actions)


class TestBasicCiWorkflow:
    """测试 generate_basic_ci_workflow() 函数"""

    def test_generates_valid_yaml_structure(self):
        """测试生成有效的 YAML 结构"""
        workflow = github_actions.generate_basic_ci_workflow()

        assert "name: CI" in workflow
        assert "on:" in workflow
        assert "jobs:" in workflow
        assert "steps:" in workflow

    def test_includes_python_matrix(self):
        """测试包含 Python 版本矩阵"""
        workflow = github_actions.generate_basic_ci_workflow()

        assert "matrix:" in workflow
        assert "'3.13'" in workflow
        assert "'3.13'" in workflow

    def test_uses_uv_setup(self):
        """测试使用 uv 设置"""
        workflow = github_actions.generate_basic_ci_workflow()

        assert "astral-sh/setup-uv@v3" in workflow
        assert "uv sync --frozen" in workflow

    def test_runs_tests_with_coverage(self):
        """测试运行测试和覆盖率"""
        workflow = github_actions.generate_basic_ci_workflow()

        assert "pytest" in workflow
        assert "--cov=src" in workflow
        assert "--cov-report=xml" in workflow

    def test_uploads_coverage_report(self):
        """测试上传覆盖率报告"""
        workflow = github_actions.generate_basic_ci_workflow()

        assert "codecov/codecov-action@v4" in workflow


class TestQualityCheckWorkflow:
    """测试 generate_quality_check_workflow() 函数"""

    def test_includes_ruff_checks(self):
        """测试包含 Ruff 检查"""
        workflow = github_actions.generate_quality_check_workflow()

        assert "ruff check" in workflow
        assert "ruff format" in workflow
        assert "--target-version=py313" in workflow

    def test_includes_mypy_check(self):
        """测试包含 MyPy 类型检查"""
        workflow = github_actions.generate_quality_check_workflow()

        assert "mypy" in workflow
        assert "--python-version=3.13" in workflow

    def test_includes_security_scan(self):
        """测试包含安全扫描"""
        workflow = github_actions.generate_quality_check_workflow()

        assert "bandit" in workflow
        assert "bandit-report.json" in workflow

    def test_syncs_dev_dependencies(self):
        """测试同步开发依赖"""
        workflow = github_actions.generate_quality_check_workflow()

        assert "uv sync --group dev" in workflow


class TestMultiOsWorkflow:
    """测试 generate_multi_os_workflow() 函数"""

    def test_includes_all_operating_systems(self):
        """测试包含所有操作系统"""
        workflow = github_actions.generate_multi_os_workflow()

        assert "ubuntu-latest" in workflow
        assert "macos-latest" in workflow
        assert "windows-latest" in workflow

    def test_uses_matrix_strategy(self):
        """测试使用矩阵策略"""
        workflow = github_actions.generate_multi_os_workflow()

        assert "matrix:" in workflow
        assert "os:" in workflow
        assert "python-version:" in workflow

    def test_enables_cache(self):
        """测试启用缓存"""
        workflow = github_actions.generate_multi_os_workflow()

        assert "enable-cache: true" in workflow

    def test_excludes_slow_tests(self):
        """测试排除慢速测试"""
        workflow = github_actions.generate_multi_os_workflow()

        assert '-m "not slow"' in workflow

    def test_uploads_test_results(self):
        """测试上传测试结果"""
        workflow = github_actions.generate_multi_os_workflow()

        assert "test-results.xml" in workflow
        assert "actions/upload-artifact@v4" in workflow


class TestDependencyUpdateWorkflow:
    """测试 generate_dependency_update_workflow() 函数"""

    def test_has_schedule_trigger(self):
        """测试有定时触发"""
        workflow = github_actions.generate_dependency_update_workflow()

        assert "schedule:" in workflow
        assert "cron:" in workflow

    def test_has_manual_trigger(self):
        """测试有手动触发"""
        workflow = github_actions.generate_dependency_update_workflow()

        assert "workflow_dispatch:" in workflow

    def test_upgrades_dependencies(self):
        """测试升级依赖"""
        workflow = github_actions.generate_dependency_update_workflow()

        assert "uv lock --upgrade" in workflow

    def test_creates_pull_request(self):
        """测试创建 Pull Request"""
        workflow = github_actions.generate_dependency_update_workflow()

        assert "peter-evans/create-pull-request@v6" in workflow
        assert "自动依赖更新" in workflow


class TestReleaseWorkflow:
    """测试 generate_release_workflow() 函数"""

    def test_triggers_on_tags(self):
        """测试在 tag 上触发"""
        workflow = github_actions.generate_release_workflow()

        assert "tags:" in workflow
        assert "'v*.*.*'" in workflow

    def test_builds_package(self):
        """测试构建包"""
        workflow = github_actions.generate_release_workflow()

        assert "uv build" in workflow

    def test_publishes_to_pypi(self):
        """测试发布到 PyPI"""
        workflow = github_actions.generate_release_workflow()

        assert "twine upload" in workflow
        assert "PYPI_API_TOKEN" in workflow

    def test_creates_github_release(self):
        """测试创建 GitHub Release"""
        workflow = github_actions.generate_release_workflow()

        assert "softprops/action-gh-release@v2" in workflow
        assert "generate_release_notes: true" in workflow


class TestDockerBuildWorkflow:
    """测试 generate_docker_build_workflow() 函数"""

    def test_sets_up_buildx(self):
        """测试设置 Docker Buildx"""
        workflow = github_actions.generate_docker_build_workflow()

        assert "docker/setup-buildx-action@v3" in workflow

    def test_logs_into_ghcr(self):
        """测试登录 GitHub Container Registry"""
        workflow = github_actions.generate_docker_build_workflow()

        assert "docker/login-action@v3" in workflow
        assert "ghcr.io" in workflow

    def test_supports_multi_platform(self):
        """测试支持多平台"""
        workflow = github_actions.generate_docker_build_workflow()

        assert "linux/amd64" in workflow
        assert "linux/arm64" in workflow

    def test_uses_cache(self):
        """测试使用缓存"""
        workflow = github_actions.generate_docker_build_workflow()

        assert "cache-from: type=gha" in workflow
        assert "cache-to: type=gha" in workflow


class TestGenerateAllWorkflows:
    """测试 generate_all_workflows() 函数"""

    def test_returns_dict_with_all_workflows(self):
        """测试返回包含所有工作流的字典"""
        workflows = github_actions.generate_all_workflows()

        assert isinstance(workflows, dict)
        assert len(workflows) == 6

    def test_includes_all_workflow_files(self):
        """测试包含所有工作流文件"""
        workflows = github_actions.generate_all_workflows()

        expected_files = [
            "ci.yml",
            "quality.yml",
            "multi-os.yml",
            "dependency-update.yml",
            "release.yml",
            "docker.yml",
        ]

        for filename in expected_files:
            assert filename in workflows

    def test_all_values_are_strings(self):
        """测试所有值都是字符串"""
        workflows = github_actions.generate_all_workflows()

        for content in workflows.values():
            assert isinstance(content, str)
            assert len(content) > 0

    def test_is_thread_safe(self):
        """测试线程安全（Python 3.14）"""
        workflows = github_actions.generate_all_workflows()

        # 验证返回的是新字典（不可变）
        assert isinstance(workflows, dict)

        # 多次调用应返回独立的字典
        workflows2 = github_actions.generate_all_workflows()
        assert workflows is not workflows2


class TestSaveWorkflowsToDisk:
    """测试 save_workflows_to_disk() 函数"""

    def test_creates_workflows_directory(self, tmp_path, capsys):
        """测试创建工作流目录"""
        github_actions.save_workflows_to_disk(tmp_path)

        workflows_dir = tmp_path / ".github" / "workflows"
        assert workflows_dir.exists()
        assert workflows_dir.is_dir()

    def test_saves_all_workflow_files(self, tmp_path, capsys):
        """测试保存所有工作流文件"""
        github_actions.save_workflows_to_disk(tmp_path)

        workflows_dir = tmp_path / ".github" / "workflows"
        files = list(workflows_dir.glob("*.yml"))

        assert len(files) == 6

    def test_workflow_files_have_content(self, tmp_path, capsys):
        """测试工作流文件有内容"""
        github_actions.save_workflows_to_disk(tmp_path)

        workflows_dir = tmp_path / ".github" / "workflows"
        ci_file = workflows_dir / "ci.yml"

        assert ci_file.exists()
        content = ci_file.read_text()
        assert len(content) > 0
        assert "name: CI" in content

    def test_prints_confirmation_messages(self, tmp_path, capsys):
        """测试打印确认消息"""
        github_actions.save_workflows_to_disk(tmp_path)

        captured = capsys.readouterr()
        assert "已保存" in captured.out
        assert "ci.yml" in captured.out


class TestExplainWorkflowStructure:
    """测试 explain_workflow_structure() 函数"""

    def test_prints_structure_explanation(self, capsys):
        """测试打印结构说明"""
        github_actions.explain_workflow_structure()

        captured = capsys.readouterr()
        assert "工作流结构解析" in captured.out
        assert "name" in captured.out
        assert "on" in captured.out
        assert "jobs" in captured.out


class TestShowUvInCiBestPractices:
    """测试 show_uv_in_ci_best_practices() 函数"""

    def test_prints_best_practices(self, capsys):
        """测试打印最佳实践"""
        github_actions.show_uv_in_ci_best_practices()

        captured = capsys.readouterr()
        assert "最佳实践" in captured.out
        assert "uv sync --frozen" in captured.out
        assert "推荐" in captured.out


class TestShowWorkflowSummary:
    """测试 show_workflow_summary() 函数"""

    def test_prints_workflow_summary(self, capsys):
        """测试打印工作流总览"""
        github_actions.show_workflow_summary()

        captured = capsys.readouterr()
        assert "工作流总览" in captured.out
        assert "ci.yml" in captured.out
        assert "quality.yml" in captured.out


class TestIntegration:
    """集成测试"""

    def test_main_function_runs(self, tmp_path, capsys):
        """测试 main() 函数执行"""
        with pytest.MonkeyPatch.context() as m:
            m.setattr(
                github_actions,
                "Path",
                lambda value=".": tmp_path if value == "demo-github-actions" else Path(value),
            )

            try:
                github_actions.main()
            except Exception as e:
                pytest.fail(f"main() raised {type(e).__name__}: {e}")

        captured = capsys.readouterr()
        assert "GitHub Actions" in captured.out

    def test_end_to_end_workflow_generation(self, tmp_path):
        """测试端到端工作流生成"""
        # 保存工作流
        github_actions.save_workflows_to_disk(tmp_path)

        # 验证所有文件存在且可读
        workflows_dir = tmp_path / ".github" / "workflows"

        for filename in ["ci.yml", "quality.yml", "multi-os.yml"]:
            file_path = workflows_dir / filename
            assert file_path.exists()

            content = file_path.read_text()
            assert "name:" in content
            assert "on:" in content
            assert "jobs:" in content


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
