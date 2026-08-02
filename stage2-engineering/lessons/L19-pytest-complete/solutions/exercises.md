# L17 CI/CD 练习参考答案

## 练习 1

1. push 到 main 分支 或 向 main 提 PR
2. Python 3.12 和 3.13
3. ruff check, ruff format --check, mypy, pytest
4. 使用已有的 uv.lock 锁定文件，不更新依赖

## 练习 2

在 setup-uv 步骤之后、install 步骤之前添加：

```yaml
- name: Cache uv cache
  uses: actions/cache@v4
  with:
    path: ~/.cache/uv
    key: uv-${{ runner.os }}-${{ hashFiles('uv.lock') }}
```
