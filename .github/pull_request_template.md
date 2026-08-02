## Summary

-

## Scope

- [ ] 课程内容 / lesson / README
- [ ] 示例 / 练习 / 参考答案
- [ ] 测试
- [ ] CI / 工具链 / 配置
- [ ] 文档 / 导航 / 归档

## Verification

- [ ] `make ci-local`
- [ ] `uv run ruff check .`
- [ ] `uv run mypy .`
- [ ] `NO_MKDOCS_2_WARNING=1 uv run --extra docs mkdocs build --strict`
- [ ] 相关 lesson / project 的定向 pytest：

```bash
# paste commands here
```

## Python version facts

- [ ] 未把 `--disable-gil` 写成 Python 运行时参数
- [ ] Free-threading 使用 `python3.13t` / `python3.14t` 独立构建
- [ ] PEP 695 标为 Python 3.12 引入，PEP 703 标为 3.13，PEP 779/649/750 标为 3.14
- [ ] 性能数字标注了“在本课程基准下”或等价限定

## Notes for reviewers

-
