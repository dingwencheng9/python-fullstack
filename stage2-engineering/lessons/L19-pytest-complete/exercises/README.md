# Exercises — L17 Pytest 完整实战练习

本目录中的练习文件已按当前课程结构展平，文件名统一带 `exercise_` 前缀。

## 文件索引

```text
exercises/
├── exercise_01_write_fixture.py       # fixture + 临时文件
├── exercise_02_parametrize_calc.py    # Calculator + 参数化测试
├── exercise_03_mock_api.py            # mock HTTP API
├── exercise_01_customize_ci.py        # 阅读并解释 CI 工作流
└── exercise_02_add_cache.py           # 设计 uv 缓存步骤
```

## 推荐完成顺序

1. `exercise_01_write_fixture.py`：掌握 fixture 的 setup/yield/teardown。
2. `exercise_02_parametrize_calc.py`：用参数表覆盖多组输入与边界值。
3. `exercise_03_mock_api.py`：用 `patch("requests.get")` 隔离真实网络。
4. `exercise_01_customize_ci.py`：阅读 `.github/workflows/ci.yml` 并回答触发、矩阵、质量门问题。
5. `exercise_02_add_cache.py`：设计可复用的 uv 缓存步骤。

## 自检命令

从仓库根目录执行：

```bash
uv run pytest \
  stage2-engineering/lessons/L17-pytest-complete/exercises/exercise_01_write_fixture.py \
  stage2-engineering/lessons/L17-pytest-complete/exercises/exercise_02_parametrize_calc.py \
  stage2-engineering/lessons/L17-pytest-complete/exercises/exercise_03_mock_api.py \
  -q

uv run python stage2-engineering/lessons/L17-pytest-complete/exercises/exercise_01_customize_ci.py
uv run python stage2-engineering/lessons/L17-pytest-complete/exercises/exercise_02_add_cache.py
```

## 完成标准

- pytest 练习全部通过。
- mock 练习不发起真实网络请求。
- CI/CD 练习能说清楚当前仓库 CI 的触发条件、Python 版本、质量门和缓存策略。
- 能将练习思路迁移到自己的项目测试中。

## 参考答案

完成练习后再查看：`../solutions/`。
