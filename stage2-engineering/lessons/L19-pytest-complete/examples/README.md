# Examples — L17 Pytest 完整实战示例

本目录包含两类示例：pytest 测试示例和 CI/CD 辅助脚本。当前文件均位于 `examples/` 根部，没有额外子目录。

## 文件索引

```text
examples/
├── 01_basic_test.py        # pytest 基础：AAA、异常、approx
├── 02_fixture_demo.py      # fixture 与作用域
├── 03_parametrize_demo.py  # 参数化测试
├── 04_mock_demo.py         # mock HTTP 请求
├── 05_pytest_markers.py    # 自定义 markers 与 CI 分层运行
├── 01_validate_ci.py       # 读取并验证 GitHub Actions 配置
├── 02_matrix_report.py     # 模拟矩阵测试报告
├── ci_basic.yml            # 基础 CI 示例
└── ci_matrix.yml           # 矩阵 CI 示例
```

## 运行方式

从仓库根目录执行：

```bash
# 运行 pytest 示例
uv run pytest \
  stage2-engineering/lessons/L17-pytest-complete/examples/01_basic_test.py \
  stage2-engineering/lessons/L17-pytest-complete/examples/02_fixture_demo.py \
  stage2-engineering/lessons/L17-pytest-complete/examples/03_parametrize_demo.py \
  stage2-engineering/lessons/L17-pytest-complete/examples/04_mock_demo.py \
  stage2-engineering/lessons/L17-pytest-complete/examples/05_pytest_markers.py \
  -q

# 运行 CI/CD 示例脚本
uv run python stage2-engineering/lessons/L17-pytest-complete/examples/01_validate_ci.py
uv run python stage2-engineering/lessons/L17-pytest-complete/examples/02_matrix_report.py

# 演示 markers 过滤
uv run pytest stage2-engineering/lessons/L17-pytest-complete/examples/05_pytest_markers.py -m "unit or smoke" -v
uv run pytest stage2-engineering/lessons/L17-pytest-complete/examples/05_pytest_markers.py -m "not integration" -v
```

## 学习建议

1. 先运行 pytest 示例，观察测试收集与断言输出。
2. 修改参数化用例，体会一个测试函数如何覆盖多组数据。
3. 在 mock 示例中添加超时、404 等分支。
4. 阅读两个 YAML 示例，再对照仓库根目录 `.github/workflows/ci.yml`。

## 相关资源

- 课程正文：`../lesson.md`
- 练习题：`../exercises/`
- 参考答案：`../solutions/`
- 课程测试：`../tests/`
