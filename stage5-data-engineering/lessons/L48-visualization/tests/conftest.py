"""
L48 Visualization 测试配置

使用 conftest 处理可选依赖，而非顶层 importorskip
"""

import matplotlib  # type: ignore

# 导入后立即关闭任何 backend，避免 CI 环境问题
import matplotlib.pyplot as plt
plt.close("all")

# 验证 matplotlib 已安装
assert matplotlib.__version__, "matplotlib 未正确安装"
