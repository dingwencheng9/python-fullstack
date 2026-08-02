"""示例代码：反调试检测与绕过"""
import re


class AntiDebugBypass:
    """反调试技术绕过工具。"""
    
    KNOWN_TRAPS = [
        (r"debugger", "空函数替换 debugger 语句"),
        (r"Object\.defineProperty.*console", "重置 console 对象"),
        (r"setInterval.*console", "清除定时器"),
        (r"Function\.prototype\.constructor", "阻止构造函数劫持"),
        (r"navigator\.webdriver", "修改 webdriver 标识"),
    ]
    
    def patch(self, js_code: str) -> str:
        """修补反调试陷阱。"""
        patched = js_code
        
        # 替换 debugger
        patched = re.sub(r";?\s*debugger\s*;", ";", patched)
        
        # 替换 console 检测
        patched = re.sub(
            r'Object\.defineProperty\s*\(\s*window,\s*[\'"]console[\'"]\s*,.*?\)',
            "// Anti-debug bypass: removed console override",
            patched,
            flags=re.DOTALL,
        )
        
        return patched


if __name__ == "__main__":
    print("反调试绕过示例")
