# L42: 缓存策略与实现

> **课程编号**: L42
> **所属阶段**: Stage 4 - Web 开发进阶
> **课程时长**: 3 小时
> **难度**: ⭐⭐⭐☆☆
> **前置课程**: L36 异步背压机制, L40 消息队列

---

## 📚 课程概述

深入讲解缓存策略的设计与实现，涵盖 Redis 缓存、缓存一致性、缓存失效策略等核心主题。

---

## 🎯 学习目标

1. 理解缓存的核心概念与适用场景
2. 掌握 Redis 缓存设计与实现
3. 理解缓存一致性模型
4. 实现缓存失效与更新策略

---

## 📋 课程大纲

- Part 1: 缓存基础概念
- Part 2: Redis 缓存实现
- Part 3: 缓存一致性
- Part 4: 缓存失效策略

---

## 🔧 环境准备

```bash
uv add redis
```

---

## 📖 详细内容

### Part 1: 缓存基础概念

缓存是提升系统性能的关键技术：

| 策略 | 适用场景 | 复杂度 |
|------|----------|--------|
| Cache-Aside | 读多写少 | 低 |
| Read-Through | 简化应用逻辑 | 中 |
| Write-Through | 数据一致性 | 中 |
| Write-Behind | 高写入性能 | 高 |

### Part 2: Redis 缓存实现

```python
from redis import Redis

redis_client = Redis.from_url("redis://localhost")

async def get_user(user_id: int) -> dict:
    cache_key = f"user:{user_id}"

    # 先查缓存
    cached = await redis_client.get(cache_key)
    if cached:
        return json.loads(cached)

    # 缓存未命中，查数据库
    user = await db.get_user(user_id)

    # 写入缓存
    await redis_client.setex(
        cache_key,
        ttl=3600,  # 1 小时过期
        value=json.dumps(user)
    )

    return user
```

### Part 3: 缓存一致性

```python
async def update_user(user_id: int, data: dict):
    # 更新数据库
    await db.update_user(user_id, data)

    # 删除缓存（而非更新）
    await redis_client.delete(f"user:{user_id}")
```

### Part 4: 缓存失效策略

| 策略 | 描述 | 适用场景 |
|------|------|----------|
| TTL | 定时过期 | 大多数场景 |
| LRU | 最近最少使用 | 内存敏感 |
| LFU | 最不经常使用 | 热点数据 |
| 主动失效 | 数据变更时删除 | 强一致性需求 |

---

## 📝 练习题

### 练习 42.1：实现缓存装饰器

```markdown
目标：实现一个通用的缓存装饰器
难度：⭐⭐⭐
```

---

## ✅ 课后检查

- [ ] 理解四种缓存策略
- [ ] 实现 Redis 缓存
- [ ] 处理缓存一致性问题
- [ ] 选择合适的失效策略

---

**课程版本**: v1.0
**最后更新**: 2026-07-22
