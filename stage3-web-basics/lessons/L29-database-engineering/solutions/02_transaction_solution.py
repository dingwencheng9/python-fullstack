"""练习 2 答案。"""

from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock


async def test_commit():
    mock = AsyncMock()
    await mock.commit()
    mock.commit.assert_awaited_once()


if __name__ == "__main__":
    asyncio.run(test_commit())
    print("OK")
