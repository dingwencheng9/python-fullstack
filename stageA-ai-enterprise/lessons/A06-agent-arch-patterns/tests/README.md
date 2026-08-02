# A06 测试用例

本目录包含 A06 课程的测试文件，验证学生练习实现的正确性和完整性。

## 测试文件说明
- `test_agent_patterns.py` - 主测试文件，验证架构模式实现
- `conftest.py` - 测试配置和 fixtures

## 快速测试
```bash
# 使用 pytest 运行所有测试
pytest tests/test_agent_patterns.py -v

# 运行单个测试用例
pytest tests/test_agent_patterns.py::test_agent_router_pattern -v
```

## 覆盖范围
- ✅ 架构模式正确性验证
- ✅ 代码质量检查
- ✅ 边界条件测试
- ✅ 错误处理验证

## 相关目录
- [lesson.md](../lesson.md) - 课程教学内容
- [exercises/](../exercises) - 练习题
- [solutions/](../solutions/) - 参考答案
