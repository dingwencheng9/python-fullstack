# examples/ - L13 示例代码

这些示例用于演示描述符协议、`property`、属性访问优先级和高级描述符模式。每个文件都可独立运行。

```bash
cd stage1-python-intermediate/lessons/L13-descriptors
python examples/01_descriptor_basics.py
```

## 文件清单

| 文件 | 主题 | 建议关注 |
| ---- | ---- | -------- |
| `01_descriptor_basics.py` | 描述符协议、数据/非数据描述符、`property`、范围验证、懒加载 | `__get__`/`__set__` 何时触发，实例字典如何参与查找 |
| `02_descriptor_advanced.py` | 自定义 property、访问日志、描述符优先级、验证描述符 | 描述符如何组合验证器和属性访问逻辑 |

## 批量运行

```bash
for f in examples/*.py; do
  echo "== $f =="
  python "$f"
done
```
