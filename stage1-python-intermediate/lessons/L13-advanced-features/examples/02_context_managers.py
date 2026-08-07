"""L13: 进阶特性 - 上下文管理器"""

import sys
import io
from contextlib import contextmanager, suppress
from pathlib import Path
from tempfile import TemporaryDirectory

# === Part 1: 协议基础 ===


class ManagedResource:
    """资源管理类"""

    def __init__(self, name: str):
        self.name = name

    def __enter__(self):
        print(f"获取资源: {self.name}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"释放资源: {self.name}")
        if exc_type:
            print(f"  异常: {exc_val}")
        return False  # 不吞掉异常

    def process(self):
        print(f"处理 {self.name}")
        return f"处理结果: {self.name}"


# 使用 with 语句
with ManagedResource("数据库连接") as resource:
    result = resource.process()
    print(result)

print("-" * 40)

# === Part 2: contextmanager 装饰器 ===


@contextmanager
def timer(name: str):
    """计时上下文管理器"""
    import time

    start = time.perf_counter()
    print(f"开始: {name}")
    try:
        yield name
    finally:
        elapsed = time.perf_counter() - start
        print(f"结束: {name}, 耗时: {elapsed:.4f}秒")


with timer("数据处理"):
    import time

    time.sleep(0.1)
    print("  正在处理...")

# === Part 3: redirect_stdout ===


def capture_output(func):
    """捕获标准输出的上下文管理器"""
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        func()
        output = sys.stdout.getvalue()
    finally:
        sys.stdout = old_stdout
    return output


def print_numbers():
    for i in range(3):
        print(i)


output = capture_output(print_numbers)
print(f"捕获的输出: {output.strip()}")

# === Part 4: suppress 忽略异常 ===


def risky_divide(a: float, b: float) -> float | None:
    """可能失败的除法"""
    with suppress(ZeroDivisionError, ValueError):
        if b == 0:
            raise ZeroDivisionError("除数不能为零")
        return a / b
    return None


print(f"10 / 2 = {risky_divide(10, 2)}")
print(f"10 / 0 = {risky_divide(10, 0)}")

# === Part 5: 文件操作上下文 ===


def read_config_file(filepath: Path) -> dict[str, str]:
    """安全读取配置文件"""
    config: dict[str, str] = {}
    if not filepath.exists():
        return config

    with filepath.open() as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                if "=" in line:
                    key, value = line.split("=", 1)
                    config[key.strip()] = value.strip()
    return config


# 创建临时配置文件，避免污染仓库或固定 /tmp 路径
with TemporaryDirectory() as temp_dir:
    temp_config = Path(temp_dir) / "test_config.txt"
    temp_config.write_text("""
# 配置文件
host=localhost
port=8080
debug=true
""")

    config = read_config_file(temp_config)
    print(f"配置: {config}")

# === Part 6: 嵌套上下文 ===


class Transaction:
    """事务管理器"""

    def __init__(self, name: str):
        self.name = name
        self.committed = False

    def __enter__(self):
        print(f"  [事务 {self.name}] 开始")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print(f"  [事务 {self.name}] 回滚")
            return False
        print(f"  [事务 {self.name}] 提交")
        self.committed = True
        return False


with Transaction("主事务") as t1:
    print("    执行主事务操作...")
    with Transaction("子事务") as t2:
        print("    执行子事务操作...")
        # 子事务失败
        # raise RuntimeError("子事务失败")

    print("    子事务完成后继续...")

# === Part 7: ExitStack 动态管理 ===

from contextlib import ExitStack

resources = ["数据库", "文件", "网络连接"]


def acquire(name: str):
    print(f"获取 {name}")
    return name


def release(name: str):
    print(f"释放 {name}")


with ExitStack() as stack:
    acquired = []
    for name in resources:
        acquired.append(acquire(name))
        stack.callback(release, name)  # 注册清理回调

print("所有资源已自动释放")

# === Part 8: nullcontext ===

from contextlib import nullcontext


def process(data: str, ctx: object | None = None):
    """使用可选上下文"""
    with ctx or nullcontext():
        print(f"处理数据: {data}")
        return data.upper()


print(process("hello"))
print(process("world", timer("处理")))

print("\n=== 上下文管理器示例完成 ===")
