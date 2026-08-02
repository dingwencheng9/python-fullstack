"""示例代码：Native 层 Frida Hook"""


def generate_native_hook(module: str, function: str) -> str:
    """生成 Native 层 Frida Hook 代码。
    
    用于追踪 SO 库中的 C/C++ 函数。
    """
    return f"""
// Native Hook: {module}::{function}
Interceptor.attach(
    Module.findExportByName("{module}", "{function}"),
    {{
        onEnter: function(args) {{
            console.log("[Native] {function} called");
            // 打印参数
            for (let i = 0; i < args.length; i++) {{
                console.log("  arg[" + i + "] = " + args[i]);
            }}
        }},
        onLeave: function(retval) {{
            console.log("[Native] {function} returned: " + retval);
        }}
    }}
);
"""


if __name__ == "__main__":
    hook_code = generate_native_hook("libnative.so", "encrypt")
    print(hook_code)
