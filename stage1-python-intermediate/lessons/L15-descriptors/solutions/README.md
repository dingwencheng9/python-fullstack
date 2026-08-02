# solutions/ - L13 参考答案

本目录提供描述符练习的参考实现。建议先独立完成 `exercises/`，遇到困难再阅读。

## 文件清单

| 文件 | 说明 |
| ---- | ---- |
| `solution_01_descriptors.py` | `Validator`、`Positive`、`Range`、`Lazy`、`Upper` 的参考实现 |
| `solution_02_property.py` | `SimpleProperty` 描述符、类级/实例级访问、描述符优先级与继承 |
| `__init__.py` | 参考答案包入口 |

## 实现要点

- `Validator` 将通用存储逻辑集中在基类，子类只需重写 `validate()`。
- `Positive` 在赋值前拒绝负数，并使用 `__set_name__()` 获得属性名以生成清晰错误信息。
- `Range` 使用闭区间校验，越界时抛出 `ValueError`。
- `Lazy` 通过 `_load_<属性名>()` 约定延迟加载，并把结果缓存到实例私有属性。
- `Upper` 展示描述符也可以做自动转换，而不仅是验证。
- `SimpleProperty` 揭示 `@property` 的底层协议机制，类级访问返回描述符对象本身。
