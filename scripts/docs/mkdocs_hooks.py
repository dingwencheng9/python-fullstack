"""MkDocs hooks - 抑制第三方插件的无意义日志输出。

当前用于抑制 git-revision-date-localized-plugin 的 "First revision timestamp"
伪报，该日志由插件上游 quirk 导致（不走 mkdocs logger），不影响 build 质量。
"""

from __future__ import annotations

import logging

# 获取 root logger 并设置级别，抑制第三方插件的无意义日志
root_logger = logging.getLogger()
if root_logger.level == logging.NOTSET:
    root_logger.setLevel(logging.WARNING)
