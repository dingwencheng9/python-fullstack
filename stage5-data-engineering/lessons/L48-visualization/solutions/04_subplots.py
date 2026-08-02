"""L49 练习4 参考：多子图"""

from __future__ import annotations

import numpy as np


def plot_four(axes: list) -> None:
    for i, ax in enumerate(axes):
        ax.plot(np.cumsum(np.random.randn(30)))
        ax.set_title(f"Series {i + 1}")
