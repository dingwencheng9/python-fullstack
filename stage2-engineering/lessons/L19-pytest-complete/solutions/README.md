# Solutions — L17 Pytest 完整实战参考答案

> 建议先独立完成 `../exercises/`，再查看本目录。

## 当前目录结构

```text
solutions/
├── README.md
├── __init__.py
├── exercises.md
├── solution_01_write_fixture.py
├── solution_02_parametrize_calc.py
├── solution_03_mock_api.py
├── solution_01_customize_ci.py
└── solution_02_add_cache.py
```

## 答案说明

- `solution_01_write_fixture.py`：使用 `TemporaryDirectory` 与 fixture 管理临时文件。
- `solution_02_parametrize_calc.py`：使用 `@pytest.mark.parametrize` 覆盖加法、除法、幂运算和除零异常。
- `solution_03_mock_api.py`：使用 `patch("requests.get")` mock HTTP 请求，并验证调用参数。
- `solution_01_customize_ci.py`：演示如何读取 CI 配置、识别矩阵版本并插入示例步骤。
- `solution_02_add_cache.py`：给出 uv 缓存步骤示例。
- `exercises.md`：CI/CD 练习的文字参考答案。

## 验证命令

从仓库根目录执行：

```bash
uv run pytest stage2-engineering/lessons/L17-pytest-complete/solutions/*.py -q
uv run python stage2-engineering/lessons/L17-pytest-complete/solutions/solution_01_customize_ci.py
```

## 学习提示

参考答案不是唯一正确实现。对比时重点关注：

1. 测试是否覆盖正常路径、边界路径、异常路径。
2. fixture 是否负责清晰的资源创建与清理。
3. mock 是否真正隔离了外部依赖。
4. CI 配置是否可读、可复现、能快速失败。
