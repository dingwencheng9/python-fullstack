"""L09 示例3: JSON 文件处理。

使用临时目录演示 JSON 读写，避免在课程目录留下 user.json/users.json。
"""

import json
from pathlib import Path
from tempfile import TemporaryDirectory

with TemporaryDirectory() as tmpdir:
    workspace = Path(tmpdir)
    user_path = workspace / "user.json"
    users_path = workspace / "users.json"

    # 1. 写入 JSON
    data = {"name": "Alice", "age": 25, "city": "Beijing", "hobbies": ["reading", "coding"]}

    with user_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ JSON 已写入: {user_path.name}")

    # 2. 读取 JSON
    with user_path.open(encoding="utf-8") as f:
        loaded = json.load(f)
    print(f"读取: {loaded}")

    # 3. 处理 JSON 列表
    users = [{"name": "Alice", "age": 25}, {"name": "Bob", "age": 30}]

    with users_path.open("w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)
    print(f"✅ 用户列表已保存: {users_path.name}")

print("示例结束后，临时目录会自动清理。")
