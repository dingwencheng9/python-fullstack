"""项目 2 测试 conftest：把项目根加入 sys.path。

from __future__ import annotations

让从仓库根运行 ``pytest projects/02-ai-fullstack-capstone/`` 时，
``from app.X import Y`` 也能解析。
"""

from __future__ import annotations

import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))
