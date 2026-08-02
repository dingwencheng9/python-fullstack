"""项目 1 测试 conftest：把项目根加入 sys.path。

from __future__ import annotations

让从仓库根运行 ``pytest projects/01-web-scraper/`` 时，``from scraper.X import Y`` 也能解析。

模块级 sys.path 修改在 conftest 加载时立即生效，比 pytest_collect_file
钩子更可靠（钩子时序在多 project 同名包场景下不确定）。
"""

from __future__ import annotations

import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    pass
