"""L05 示例2: pathlib 使用。

示例自带临时文件，不依赖其他示例先生成 test.txt。
"""

from pathlib import Path
from tempfile import TemporaryDirectory

with TemporaryDirectory() as tmpdir:
    workspace = Path(tmpdir)

    # 1. 创建路径对象
    p = workspace / "test.txt"
    p.write_text("Hello from pathlib!\n这是 pathlib 示例。\n", encoding="utf-8")

    # 2. 检查存在
    print(f"文件存在: {p.exists()}")

    # 3. 读写
    if p.exists():
        content = p.read_text(encoding="utf-8")
        print(f"内容: {content[:50]}...")

    # 4. 路径操作
    print(f"文件名: {p.name}")
    print(f"后缀: {p.suffix}")
    print(f"绝对路径: {p.absolute()}")

    # 5. 遍历目录
    print("\n临时目录文件:")
    for item in workspace.iterdir():
        print(f"  {item.name}")

print("\n示例结束后，临时目录会自动清理。")
