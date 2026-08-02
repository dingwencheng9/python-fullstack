"""示例代码：Frida Hook 脚本生成器"""
from dataclasses import dataclass


@dataclass
class FridaHook:
    target_class: str
    target_method: str
    hook_code: str


def generate_hook(class_name: str, method_name: str, overloads: list[str]) -> FridaHook:
    """生成 Frida Hook 代码。
    
    示例输出：
    Java.perform(function() {
        var target = Java.use("com.example.App");
        target.getAuthToken.implementation = function() {
            return "fake_token";
        };
    });
    """
    hook_code = f"""Java.perform(function() {{
    var cls = Java.use("{class_name}");
    cls.{method_name}.implementation = function({', '.join(f'arg{i}' for i in range(len(overloads)))}) {{
        console.log("[Frida] {method_name} called");
        // TODO: 实现 Hook 逻辑
        return this.{method_name}({', '.join(f'arg{i}' for i in range(len(overloads)))});
    }};
}});
"""
    return FridaHook(
        target_class=class_name,
        target_method=method_name,
        hook_code=hook_code,
    )


if __name__ == "__main__":
    hook = generate_hook("com.example.App", "getAuthToken", ["String", "int"])
    print(hook.hook_code)
