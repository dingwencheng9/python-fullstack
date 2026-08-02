# solutions/ - 参考答案

**用途**：提供 `01_oop_basics.py` 中各个类的拆分版参考实现。

> ⚠️ 建议先独立完成 exercises，再查看本目录。答案被拆成多个模块，是为了示范真实项目中“一个模块聚焦一个概念/实体”的组织方式。

## 文件清单

| 文件 | 对应练习 | 说明 |
|------|----------|------|
| `person.py` | 练习 1 | `Person`：基础类、实例属性、实例方法 |
| `bank_account.py` | 练习 2 | `BankAccount`：封装、只读 property、存取款校验 |
| `rectangle.py` | 练习 3 | `Rectangle`：参数验证、面积和周长 |
| `animal.py` | 练习 4 | `Animal`、`Dog`、`Cat`：继承与多态 |
| `vector.py` | 练习 5 | `Vector`：特殊方法、向量运算、哈希 |
| `__init__.py` | 汇总导出 | 统一从 `solutions` 包导出全部答案类 |

## 使用方式

从课程目录运行：

```bash
python3 - <<'PY'
from solutions import BankAccount, Vector

account = BankAccount("Alice", 1000)
account.deposit(500)
print(account.balance)

print(Vector(1, 2) + Vector(3, 4))
PY
```

或者直接运行测试：

```bash
uv run pytest tests/ -q
```
