"""数据读取模块。"""

from __future__ import annotations

import json
import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)


def load_json(path: str | Path) -> pd.DataFrame:
    """读取 JSON 列表为 DataFrame。"""
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except FileNotFoundError as e:
        logger.error("JSON 文件不存在: %s", path, exc_info=True)
        raise FileNotFoundError(f"JSON 文件不存在: {path}") from e
    except json.JSONDecodeError as e:
        logger.error("JSON 解析失败: %s — %s", path, e, exc_info=True)
        raise json.JSONDecodeError(f"JSON 解析失败: {path} — {e}", e.doc, e.pos) from e
    except UnicodeDecodeError as e:
        logger.error("文件编码错误: %s — %s", path, e, exc_info=True)
        raise UnicodeDecodeError(
            e.encoding, e.object, e.start, e.end, f"文件编码错误: {path}"
        ) from e

    if not isinstance(data, list):
        raise TypeError("JSON 必须是对象列表")
    return pd.DataFrame(data)


def load_csv(path: str | Path) -> pd.DataFrame:
    """读取 CSV 文件。"""
    try:
        return pd.read_csv(path)
    except FileNotFoundError as e:
        logger.error("CSV 文件不存在: %s", path, exc_info=True)
        raise FileNotFoundError(f"CSV 文件不存在: {path}") from e
    except Exception as e:
        logger.error("CSV 读取失败: %s — %s", path, e, exc_info=True)
        raise


def load_data(path: str | Path) -> pd.DataFrame:
    """根据后缀自动读取数据。"""
    p = Path(path)
    if p.suffix == ".json":
        return load_json(p)
    if p.suffix == ".csv":
        return load_csv(p)
    raise ValueError(f"不支持的文件类型: {p.suffix}")
