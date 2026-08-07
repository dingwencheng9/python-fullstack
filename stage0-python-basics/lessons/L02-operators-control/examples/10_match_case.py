"""L02 示例10: match-case 模式匹配（Python 3.10+）

本文件演示 Python 3.10 引入的 match-case 结构化模式匹配语法：
- 基本值匹配
- 多值 OR 匹配
- 带守卫的条件模式（Guards）

【注意】本文件需要 Python 3.10+ 才能运行。在旧版本中会报 SyntaxError。

> 📖 **L03 将学到**：本节的列表和字典模式匹配（解包）需要先掌握 list 和 dict 的基础知识。
"""

# ============================================================
# 1. 基本值匹配
# ============================================================
print("=" * 50)
print("1. HTTP 状态码匹配")
print("=" * 50)

status_code = 404

match status_code:
    case 200:
        print("OK - 请求成功")
    case 201:
        print("Created - 资源创建成功")
    case 204:
        print("No Content - 无内容返回")
    case 400:
        print("Bad Request - 请求语法错误")
    case 401:
        print("Unauthorized - 需要认证")
    case 403:
        print("Forbidden - 无权限访问")
    case 404:
        print("Not Found - 资源不存在")
    case 500:
        print("Internal Server Error - 服务器错误")
    case 502:
        print("Bad Gateway - 网关错误")
    case 503:
        print("Service Unavailable - 服务不可用")
    case _:
        print(f"Unknown status: {status_code}")


# ============================================================
# 2. 多值 OR 匹配
# ============================================================
print("\n" + "=" * 50)
print("2. 日期分类（OR 匹配）")
print("=" * 50)

day = "Saturday"

match day:
    case "Monday" | "Tuesday" | "Wednesday" | "Thursday" | "Friday":
        print(f"{day} → 工作日")
    case "Saturday" | "Sunday":
        print(f"{day} → 周末")
    case _:
        print(f"{day} → 无效的日期")


# ============================================================
# 3. 带守卫的条件匹配
# ============================================================
print("\n" + "=" * 50)
print("3. 年龄分类（带守卫）")
print("=" * 50)

age = 25

match age:
    case x if x < 0:
        print(f"{age} 岁 → 无效年龄")
    case x if 0 <= x < 3:
        print(f"{age} 岁 → 婴儿")
    case x if 3 <= x < 12:
        print(f"{age} 岁 → 儿童")
    case x if 12 <= x < 18:
        print(f"{age} 岁 → 青少年")
    case x if 18 <= x < 65:
        print(f"{age} 岁 → 成年人")
    case x if x >= 65:
        print(f"{age} 岁 → 老年人")


# ============================================================
# 4. 颜色分类
# ============================================================
print("\n" + "=" * 50)
print("4. 颜色分类")
print("=" * 50)

color = "red"

match color:
    case "red":
        print("🔴 红色")
    case "green":
        print("🟢 绿色")
    case "blue":
        print("🔵 蓝色")
    case _:
        print("❓ 未知颜色")


# ============================================================
# 5. 简单命令处理
# ============================================================
print("\n" + "=" * 50)
print("5. 简单命令处理")
print("=" * 50)

command = "help"

match command:
    case "start":
        print("🚀 启动程序")
    case "stop":
        print("⏹️ 停止程序")
    case "restart":
        print("🔄 重启程序")
    case "help":
        print("📖 显示帮助信息")
    case "version":
        print("📋 显示版本信息")
    case _:
        print(f"❓ 未知命令: {command}")


# ============================================================
# 6. 简单交通信号
# ============================================================
print("\n" + "=" * 50)
print("6. 交通信号")
print("=" * 50)

signal = "yellow"

match signal:
    case "red":
        print("🚦 停 - 请等待")
    case "yellow":
        print("🚦 慢 - 注意观察")
    case "green":
        print("🚦 行 - 安全通过")
    case _:
        print("❓ 未知信号")


print("\n💡 提示")
print("- match-case 适合处理多个固定值的分支判断")
print("- case _ 是默认分支（类似 else）")
print("- 使用 | 可以匹配多个值")
print("- 使用 if 可以添加额外条件（守卫）")

print("\n🎉 match-case 示例完成！")
