"""L09 示例1: 文件读写。

使用临时目录演示读写，避免在课程目录留下 test.txt。
"""

from tempfile import TemporaryDirectory
from pathlib import Path

with TemporaryDirectory() as tmpdir:
    path = Path(tmpdir) / "test.txt"

    # 1. 写入文件
    with path.open("w", encoding="utf-8") as f:
        f.write("Hello, World!\n")
        f.write("这是第二行\n")

    # 2. 读取全部
    with path.open(encoding="utf-8") as f:
        content = f.read()
        print("全部内容:")
        print(content)

    # 3. 逐行读取
    print("\n逐行读取:")
    with path.open(encoding="utf-8") as f:
        for line in f:
            print(line.strip())

    # 4. 追加
    with path.open("a", encoding="utf-8") as f:
        f.write("追加的一行\n")

    print(f"\n临时文件路径: {path}")
    print("示例结束后，临时目录会自动清理。")
