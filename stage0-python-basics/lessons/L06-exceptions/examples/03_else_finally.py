"""示例3: else 和 finally 子句"""


def read_file_content(filepath: str) -> str | None:
    """读取文件内容"""
    try:
        with open(filepath) as file:
            return file.read()
    except FileNotFoundError:
        print(f"错误: 文件 '{filepath}' 不存在")
        return None
    except PermissionError:
        print(f"错误: 没有权限读取 '{filepath}'")
        return None
    finally:
        print("文件已关闭")


def read_file_with_context(filepath: str) -> str | None:
    """使用上下文管理器读取文件"""
    try:
        with open(filepath) as file:
            content = file.read()
    except FileNotFoundError:
        print(f"错误: 文件 '{filepath}' 不存在")
        return None
    else:
        print("文件读取成功！")
        return content
    finally:
        print("无论成功失败都会执行")


# 演示 try-except-else-finally
def divide_with_logging(a: float, b: float) -> float | None:
    """带日志记录的除法"""
    try:
        result = a / b
    except ZeroDivisionError:
        print("除数为零")
        return None
    else:
        print("计算成功")
        return result
    finally:
        print("清理资源")


print("测试正常情况:")
print(divide_with_logging(10, 2))

print("\n测试异常情况:")
print(divide_with_logging(10, 0))
